# Copyright (c) 2025, neemus and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now
 
@frappe.whitelist()
def fetch_test_data(docname):
    """Fetch data from Radiation_Test_Data_Entry based on project, subsystem, package, and card."""
    
    doc = frappe.get_doc("Radiation_Shield_Approve", docname)
    
    # Validate required fields
    if not doc.project or not doc.subsystem or not doc.package or not doc.card:
        frappe.throw("Please fill Project, Subsystem, Package, and Card fields before fetching data.")
    
    # Clear existing table entries
    doc.set("table_appr", [])
    
    # Find Radiation_Test_Data_Entry documents matching the criteria
    test_entry_docs = frappe.get_all(
        "Radiation_Test_Data_Entry",
        filters={
            "project": doc.project,
            "subsystem": doc.subsystem,
            "package": doc.package,
            "card": doc.card,
            "docstatus": ["<", 2]  # Include draft and submitted documents
        },
        fields=["name"]
    )
    
    if not test_entry_docs:
        frappe.msgprint("No matching Radiation Test Data Entry found for the selected Project, Subsystem, Package, and Card.")
        return False
    
    # Fetch all items from matching entries
    all_items = []
    for entry in test_entry_docs:
        test_items = frappe.get_all(
            "Radiation_Test_Data_Item",
            filters={"parent": entry.name, "parenttype": "Radiation_Test_Data_Entry"},
            fields=["name", "type", "symbol", "part_number", "package", "mount_on",
                    "tid_hardness_krad", "radiation_shielding",
                    "tid_dose_krad", "rdm_", "rad_test_id", "tid_level", "link_id", "pstyle", "count"]
        )
        all_items.extend(test_items)
    
    if not all_items:
        frappe.msgprint("No test data items found in the matching Radiation Test Data Entry documents.")
        return False
    
    # Add items to the approve table
    for item in all_items:
        doc.append("table_appr", {
            "type": item.get("type"),
            "symbol": item.get("symbol"),
            "part_number": item.get("part_number"),
            "mount_on": item.get("mount_on"),
            "tid_hardness": item.get("tid_hardness_krad"),
            "radiation_shielding": item.get("radiation_shielding"),
            "tid_level": item.get("tid_level"),
            "rdm": item.get("rdm_"),
            "component_id": item.get("rad_test_id"),
            "link_id": item.get("link_id"),
            "pstyle": item.get("pstyle"),
            "count": item.get("count")
        })
    
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    frappe.msgprint(f"Fetched {len(all_items)} item(s) from Radiation Test Data Entry.")
    return True
 
 
@frappe.whitelist()

def auto_approve(docname):

    """Auto Approve or Reject based on thresholds."""

    doc = frappe.get_doc("Radiation_Shield_Approve", docname)
 
    HARDNESS_LIMIT = 50.0   # krad

    RDM_LIMIT = 10.0        # percent
 
    for row in doc.table_appr:

        try:

            tid_val = float(row.tid_hardness or 0)

            rdm_val = float(str(row.rdm or "0").replace("%", ""))
 
            if tid_val >= HARDNESS_LIMIT and rdm_val >= RDM_LIMIT:

                row.status = "Approved"

                row.remarks = "Meets radiation limits"

            else:

                row.status = "Rejected"

                row.remarks = "Below threshold"

        except Exception as e:

            row.status = "Rejected"

            row.remarks = f"Error: {e}"
 
    doc.save(ignore_permissions=True)

    frappe.db.commit()

    return True
 
 
class Radiation_Shield_Approve(Document):

    def on_submit(self):

        """Log approval data into Radiation_Shield_History."""

        hist = frappe.new_doc("Radiation_Shield_History")

        hist.project = self.project

        hist.subsystem = self.subsystem

        hist.package = self.package

        hist.card = self.card
 
        total_items = len(self.table_appr)

        approved = len([r for r in self.table_appr if r.status == "Approved"])
 
        hist.append("package_summary", {

            "package": self.package,

            "total_cards": total_items,

            "total_radiation_shield_approved": approved

        })
 
        for row in self.table_appr:

            hist.append("card_history", {

                "package": self.package,

                "card_name": self.card,

                "ecad_status": "Approved" if row.status == "Approved" else "Rejected",

                "card_shielding_status": row.status,

                "status_date": now(),

                "updated_by": frappe.session.user

            })
 
        hist.save(ignore_permissions=True)

        frappe.db.commit()

 