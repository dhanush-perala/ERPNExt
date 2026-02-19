# Copyright (c) 2025, neemus and contributors
# For license information, please see license.txt

import frappe

from frappe.model.document import Document
 
from frappe.website.website_generator import WebsiteGenerator
from frappe import _
class ADDPROJECTSUBSYSTEM(Document):
    pass
    '''def on_trash(self):
        # Instead of deleting, mark as inactive
        frappe.db.set_value(
            self.doctype,
            self.name,
            "status",  # Change this to your actual field name
            "Inactive"
        )
        
        frappe.db.commit()
 
        # Stop the deletion process and show a message
        frappe.throw("")'''
	
# import frappe
from frappe.model.document import Document


class ADDPROJECTSUBSYSTEM(Document):
	pass
