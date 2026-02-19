# Copyright (c) 2025, neemus and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class GENERATEREQUESTKITTEDCOMPONENTS(Document):
	pass
import frappe

from frappe.model.document import Document
 
class GENERATEREQUESTKITTEDCOMPONENTS(Document):

    pass
 
''' 
def cancel_linked_sales_order_after_cancel(doc, method=None):

    """

    Automatically cancel linked Sales Order

    when Kit Request is cancelled

    """
 
    if not doc.sales_order:

        return
 
    # 1️⃣ Cancel Stock Reservation Entries

    sre_list = frappe.get_all(

        "Stock Reservation Entry",

        filters={

            "voucher_type": "Sales Order",

            "voucher_no": doc.sales_order,

            "docstatus": 1

        },

        pluck="name"

    )
 
    for sre_name in sre_list:

        try:

            frappe.get_doc("Stock Reservation Entry", sre_name).cancel()

        except Exception:

            frappe.log_error(frappe.get_traceback(), "Failed to cancel SRE")
 
    # 2️⃣ Cancel Sales Order

    try:

        so = frappe.get_doc("Sales Order", doc.sales_order)

        if so.docstatus == 1:

            so.flags.ignore_links = True   # 🔥 critical

            so.cancel()

    except Exception:

        frappe.log_error(frappe.get_traceback(), "Failed to cancel Sales Order")

 '''