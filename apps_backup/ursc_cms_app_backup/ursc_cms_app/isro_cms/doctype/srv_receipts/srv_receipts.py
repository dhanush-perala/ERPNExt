# srv_receipts.py
import frappe

from frappe.model.document import Document
 
from frappe.website.website_generator import WebsiteGenerator
from frappe import _
class SRVRECEIPTS(Document):
    '''@classmethod
    def get_list(cls, args):
        if "filters" not in args:
            args["filters"] = {}
        args["filters"]["status"] = "Active"
        return super().get_list(args)'''
    # Website configuration for generator
    '''  website = frappe._dict(
        condition_field = "published",  # optional, field to filter docs for public view
        page_title_field = "title",     # field that becomes the <title>
	template = "ursc_cms_app/isro_cms/doctype/srv_receipts/templates/srv_receipts.html"

    )'''
 
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
