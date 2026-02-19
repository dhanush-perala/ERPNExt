# Copyright (c) 2025, neemus and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import date


class SRNRequest(Document):
	def validate(self):
		# Set default request date to today if not set
		if not self.request_date:
			self.request_date = date.today()
	
	def before_save(self):
		# Ensure request_date is set before saving
		if not self.request_date:
			self.request_date = date.today()
