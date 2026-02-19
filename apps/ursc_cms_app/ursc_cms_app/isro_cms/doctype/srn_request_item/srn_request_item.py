# Copyright (c) 2025, neemus and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import date, datetime


class SRNRequestItem(Document):
	def validate(self):
		# Auto-fill acquisition_date from Component doctype if not set
		if not self.acquisition_date and self.component:
			self.acquisition_date = self.get_acquisition_date_from_component()
		
		# Calculate component age if manufacture_date is available
		if self.manufacture_date:
			self.component_age = self.calculate_component_age()
			
			# Auto-check requires_testing if age > 5 years
			if self.component_age > 5:
				self.requires_testing = 1
			else:
				self.requires_testing = 0
	
	def get_acquisition_date_from_component(self):
		"""Get acquisition date from Component doctype"""
		try:
			# Try to get acquisition date from Item doctype
			item_doc = frappe.get_doc("Item", self.component)
			
			# Check if Item has custom acquisition_date field
			if hasattr(item_doc, 'acquisition_date') and item_doc.acquisition_date:
				return item_doc.acquisition_date
			
			# Check if Item has custom manufacture_date field
			if hasattr(item_doc, 'manufacture_date') and item_doc.manufacture_date:
				return item_doc.manufacture_date
			
			# If no specific acquisition date, use creation date as fallback
			return item_doc.creation.date()
			
		except Exception as e:
			frappe.log_error(f"Error getting acquisition date for component {self.component}: {str(e)}")
			# Return today's date as fallback
			return date.today()
	
	def calculate_component_age(self):
		"""Calculate component age in years based on manufacture_date"""
		if not self.manufacture_date:
			return 0
		
		try:
			# Convert manufacture_date to date object if it's a string
			if isinstance(self.manufacture_date, str):
				manufacture_date = datetime.strptime(self.manufacture_date, '%Y-%m-%d').date()
			else:
				manufacture_date = self.manufacture_date
			
			# Calculate difference in years
			today = date.today()
			age_days = (today - manufacture_date).days
			age_years = age_days / 365.25  # Using 365.25 for leap years
			
			# Round to 2 decimal places
			return round(age_years, 2)
			
		except Exception as e:
			frappe.log_error(f"Error calculating component age: {str(e)}")
			return 0
	
	@frappe.whitelist()
	def get_component_details(self):
		"""Server-side method to get component details"""
		if not self.component:
			return None
		
		try:
			item_doc = frappe.get_doc("Item", self.component)
			details = {
				"acquisition_date": None,
				"manufacture_date": None,
				"description": item_doc.description or item_doc.item_name
			}
			
			# Get acquisition date
			if hasattr(item_doc, 'acquisition_date') and item_doc.acquisition_date:
				details["acquisition_date"] = item_doc.acquisition_date
			elif hasattr(item_doc, 'manufacture_date') and item_doc.manufacture_date:
				details["manufacture_date"] = item_doc.manufacture_date
				details["acquisition_date"] = item_doc.manufacture_date
			
			return details
			
		except Exception as e:
			frappe.log_error(f"Error getting component details: {str(e)}")
			return None
