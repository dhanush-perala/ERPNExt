# Copyright (c) 2025, neemus and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestUpdate_Failure_Result(FrappeTestCase):
	 def on_trash(self):
        # Instead of deleting, mark as inactive
        frappe.db.set_value(
            self.doctype,
            self.name,
            "status",  # Change this to your actual field name
            "Inactive"
        )
        
        frappe.db.set_value(
        self.doctype,
        self.name,
        "docstatus",  # Change this to your actual field name
        "2"
        )
        frappe.db.commit()
 
        # Stop the deletion process and show a message
        frappe.throw("")
	
