# Copyright (c) 2025, neemus and contributors
# For license information, please see license.txt
#DPA_Request_Status

import frappe
from frappe.model.document import Document

class DPA_Request_Status(Document):
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
        frappe.throw("Document marked as Inactive instead of being deleted.")

	
