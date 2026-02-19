import frappe

from frappe import _

from frappe.model.document import Document
from frappe.utils import cint
from datetime import date
import time
 
 
# =========================================================

# DOCTYPE CONTROLLER

# =========================================================
MAX_ROWS = 20
class SIV(Document): 


    """

    WORKING DRAFT SPLIT IMPLEMENTATION

    - after_insert  → first Save

    - on_update     → subsequent Saves

    """
 
    def validate(self):
        if self.status == "Inactive" and not self.is_new():
            # If doc is being updated but already Inactive, prevent unless it's the background job
            # (In Frappe, db_set doesn't call validate usually, but it's good practice)
            # We allow the update if it's the very first time it becomes inactive 
            # or if we are just reading. But since this is validate(), it's during save.
            
            # Check if status was already Inactive in the database
            old_doc = self.get_doc_before_save()
            if old_doc and old_doc.status == "Inactive":
                frappe.throw(_("Cannot edit an Inactive SIV record."))

    def before_save(self):
        self._trigger_split("before_save")

    def on_submit(self):
        if self.work_flow_status == "Approved":
            # Requirement: Status must be Active when Approved
            self.db_set("status", "Active")
            
            # Set on object so it's returned to the client immediately for the JS timer
            self.approved_on = frappe.utils.now()
            # Persist to database
            self.db_set("approved_on", self.approved_on)
            
            frappe.logger().info(f"[SIV] Approved {self.name}: Set Active and recorded approval time for 60-day inactivation.")

    def _trigger_split(self, source):
        # Draft only
        if self.docstatus != 0:
            return

        # Guard: already processed
        if cint(getattr(self, "split_processed", 0)) == 1:
            return

        row_count = len(self.table_bnpa or [])
        frappe.logger().info(f"[SIV SPLIT] {source} {self.name} rows={row_count}")

        if row_count <= MAX_ROWS:
            return

        # Split Synchronously in before_save
        frappe.logger().info(f"[SIV SPLIT] Splitting {self.name} synchronously in before_save")
        
        rows = self.table_bnpa or []
        total = len(rows)

        # 1️⃣ Keep first 20 rows in current doc
        keep_rows = rows[:MAX_ROWS]
        remaining_rows = rows[MAX_ROWS:]

        self.set("table_bnpa", keep_rows)
        self.split_processed = 1
        
        # 2️⃣ Create additional DRAFT SIVs for remaining rows
        created = []
        for i in range(0, len(remaining_rows), MAX_ROWS):
            chunk = remaining_rows[i:i + MAX_ROWS]

            new_siv = frappe.new_doc("SIV")

            # Copy parent fields
            new_siv.select_project = self.select_project
            new_siv.select_sub_system = self.select_sub_system
            new_siv.pack_name = self.pack_name
            new_siv.select_card = self.select_card
            new_siv.card_type = self.card_type

            # Prevent recursion in new docs
            new_siv.split_processed = 1

            for r in chunk:
                child = new_siv.append("table_bnpa", {})
                data = r.as_dict()
                for k, v in data.items():
                    if k in ("name", "parent", "parenttype", "parentfield", "idx", "docstatus"):
                        continue
                    child.set(k, v)

            new_siv.insert(ignore_permissions=True)
            created.append(new_siv.name)

        frappe.logger().info(f"[SIV SPLIT] Parent {self.name} truncated to 20. Created children: {created}")
 
 #siv Request for 60days
 
 
# =========================================================

# HELPERS

# =========================================================

def _is_screening_lab(destination):

    return bool(destination and destination.strip().lower() == "screening lab")
 
 
def _dc_sort(dc):

    """

    Date Code format: YYWW (e.g. 2127)

    """

    if not dc:

        return 999999

    s = str(dc).strip()

    if len(s) != 4 or not s.isdigit():

        return 999999

    yy = int(s[:2])

    ww = int(s[2:])

    if ww < 1 or ww > 53:

        return 999999

    return yy * 100 + ww
 
 
# =========================================================

# MAIN API

# =========================================================

@frappe.whitelist()

def get_siv_fifo_advice(siv_name=None, destination=""):
 
    if not siv_name:

        frappe.throw(_("SIV name is required"))
 
    siv = frappe.get_doc("SIV", siv_name)
 
    if not siv.select_card:

        frappe.throw(_("Select Card is mandatory in SIV"))
 
    project = siv.select_project

    card_name = siv.select_card

    screening_lab = _is_screening_lab(destination)

    today = date.today()
 
    # -----------------------------------------------------

    # CARD → PRIORITY WAREHOUSES (ORDER PRESERVED)

    # -----------------------------------------------------

    card = frappe.get_doc(

        "Cardwise Component List Update and Approve - Designer",

        card_name

    )
 
    allowed_warehouses = list(dict.fromkeys([

        r.stock for r in card.warehouse_priority if r.stock

    ]))
 
    if not allowed_warehouses:

        frappe.throw(_("No warehouses found in Card Warehouse Priority"))
 
    priority_index = {

        wh: idx + 1 for idx, wh in enumerate(allowed_warehouses)

    }
 
    # -----------------------------------------------------

    # ITEMS FROM SIV / CARD

    # -----------------------------------------------------

    items = list({

        r.link_part_number

        for r in siv.table_bnpa

        if r.link_part_number

    })
 
    if not items:

        frappe.throw(_("No items found in SIV child table"))
 
    # -----------------------------------------------------

    # STEP 1: PROCUREMENT LOTS (FIFO SOURCE)

    # -----------------------------------------------------

    incoming_lots = frappe.db.sql("""

        SELECT

            sed.item_code,

            sed.t_warehouse AS warehouse,

            sed.custom_date_code AS date_code,

            sed.custom_exp_date AS exp_date,

            sed.qty AS incoming_qty,

            se.posting_date

        FROM `tabStock Entry Detail` sed

        JOIN `tabStock Entry` se

            ON se.name = sed.parent

        WHERE

            se.docstatus = 1

            AND se.stock_entry_type = 'Stock Entry'

            AND sed.item_code IN %(items)s

            AND sed.t_warehouse IN %(warehouses)s

    """, {

        "items": tuple(items),

        "warehouses": tuple(allowed_warehouses)

    }, as_dict=True)
 
    # -----------------------------------------------------

    # GROUP LOTS

    # -----------------------------------------------------

    lots_by_key = {}

    for lot in incoming_lots:

        key = (lot.item_code, lot.warehouse)

        lot["dc_sort"] = _dc_sort(lot.date_code)

        lots_by_key.setdefault(key, []).append(lot)
 
    for k in lots_by_key:

        lots_by_key[k].sort(

            key=lambda x: (x["dc_sort"], x["posting_date"])

        )
 
    # -----------------------------------------------------

    # STEP 2: ISSUED QTY (LEDGER)

    # -----------------------------------------------------

    issued_rows = frappe.db.sql("""

        SELECT

            item_code,

            warehouse,

            ABS(SUM(actual_qty)) AS issued_qty

        FROM `tabStock Ledger Entry`

        WHERE

            actual_qty < 0

            AND is_cancelled = 0

            AND item_code IN %(items)s

            AND warehouse IN %(warehouses)s

        GROUP BY item_code, warehouse

    """, {

        "items": tuple(items),

        "warehouses": tuple(allowed_warehouses)

    }, as_dict=True)
 
    issued_map = {

        (r.item_code, r.warehouse): float(r.issued_qty or 0)

        for r in issued_rows

    }
 
    # -----------------------------------------------------

    # STEP 3: FIFO DEDUCTION

    # -----------------------------------------------------

    fifo_available = []
 
    for key, lots in lots_by_key.items():

        issued_left = issued_map.get(key, 0)
 
        for lot in lots:

            lot_qty = float(lot.incoming_qty or 0)
 
            if issued_left >= lot_qty:

                issued_left -= lot_qty

                continue
 
            remaining = lot_qty - issued_left

            issued_left = 0
 
            if remaining <= 0:

                continue
 
            if not screening_lab and lot.exp_date and lot.exp_date < today:

                continue
 
            fifo_available.append({

                "item_code": lot.item_code,

                "warehouse": lot.warehouse,

                "date_code": lot.date_code,

                "exp_date": lot.exp_date,

                "qty": remaining

            })
 
    fifo_available.sort(

        key=lambda x: (_dc_sort(x["date_code"]),

                       priority_index.get(x["warehouse"], 999))

    )
 
    # -----------------------------------------------------

    # STEP 4: PROJECTED QTY – CARD ITEMS

    # -----------------------------------------------------

    projected_rows = frappe.db.sql("""

        SELECT

            b.item_code,

            b.warehouse,

            b.projected_qty

        FROM `tabBin` b

        WHERE b.item_code IN %(items)s

    """, {

        "items": tuple(items)

    }, as_dict=True)
 
    card_item_projected = {}
 
    for r in projected_rows:

        item = r.item_code

        wh = r.warehouse

        qty = r.projected_qty or 0
 
        card_item_projected.setdefault(item, {

            "total_projected_qty_all_wh": 0,

            "priority_warehouse_projected": [],

            "other_warehouse_projected": []

        })
 
        card_item_projected[item]["total_projected_qty_all_wh"] += qty
 
        if wh in priority_index:

            card_item_projected[item]["priority_warehouse_projected"].append({

                "warehouse": wh,

                "projected_qty": qty,

                "priority": priority_index[wh]

            })

        else:

            card_item_projected[item]["other_warehouse_projected"].append({

                "warehouse": wh,

                "projected_qty": qty

            })
 
    for item in card_item_projected:

        card_item_projected[item]["priority_warehouse_projected"].sort(

            key=lambda x: x["priority"]

        )
 
    # -----------------------------------------------------

    # RETURN

    # -----------------------------------------------------

    return {

        "siv": siv.name,

        "project": project,

        "card": card_name,

        "destination": destination,

        "screening_lab": screening_lab,
 
        "allowed_warehouses": allowed_warehouses,

        "advice_lines": fifo_available,
 
        # ⭐ WHAT YOU ASKED FOR

        "card_item_projected_qty": card_item_projected,
 
        "processed_by": frappe.session.user,

        "processed_on": frappe.utils.now_datetime()

    }

 
 
@frappe.whitelist()

def debug_siv_split(siv_name):

    """

    Debug helper to check SIV split logic

    """

    if not siv_name:

        frappe.throw("SIV name is required")
 
    siv = frappe.get_doc("SIV", siv_name)
 
    return {

        "siv": siv.name,

        "total_rows": len(siv.table_bnpa or []),

        "project": siv.select_project,

        "card": siv.select_card

    }

 

 
@frappe.whitelist()
@frappe.whitelist()
def inactivate_old_siv_records():
    """
    Daily job: Inactivate SIV records approved more than 60 days ago.
    """
    from frappe.utils import add_days, now_datetime
    
    # Calculate the cutoff date (60 days ago)
    cutoff = add_days(now_datetime(), -60)
    
    # Find active, approved SIVs older than 60 days
    old_sivs = frappe.get_all(
        "SIV",
        filters={
            "status": "Active",
            "work_flow_status": "Approved",
            "approved_on": ["<=", cutoff],
            "docstatus": 1
        },
        pluck="name"
    )
    
    for docname in old_sivs:
        # Use set_value to update status and reset workflow
        frappe.db.set_value(
            "SIV",
            docname,
            {"status": "Inactive", "work_flow_status": "Initial", "docstatus": 0},
            update_modified=True,
        )
        frappe.clear_document_cache("SIV", docname)
        frappe.logger().info(f"[SIV] Multi-day inactivation completed for {docname}")
    
    if old_sivs:
        frappe.db.commit()

@frappe.whitelist()
def delayed_status_update(docname):
    """
    DEPRECATED: Background job for 30s inactivation (kept for backward compatibility during transition)
    """
    pass
