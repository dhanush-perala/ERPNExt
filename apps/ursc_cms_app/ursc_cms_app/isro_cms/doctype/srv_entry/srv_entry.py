# srv_entry.py
import frappe
from frappe.model.document import Document
from frappe import _

class SRVENTRY(Document):
	 
    def on_trash(self):
        # Instead of deleting, mark as inactive
        frappe.db.set_value(
            self.doctype,
            self.name,
            "status",  # Change this to your actual field name
            "Inactive"
        )
        
        frappe.db.commit()
 
        # Stop the deletion process and show a message
        frappe.throw("")
