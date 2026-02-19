import frappe
from frappe.model.document import Document
import random

class SRNPOST(Document):
	def validate(self):
		# Generate unique 4-digit SRN Reference number if not already set
		if not self.srn_ref_no:
			self.srn_ref_no = self.generate_unique_srn_ref_no()
	
	def generate_unique_srn_ref_no(self):
		"""Generate a unique 4-digit SRN Reference number"""
		max_attempts = 100  # Prevent infinite loop
		attempt = 0
		
		while attempt < max_attempts:
			# Generate a random 4-digit number (1000-9999)
			srn_ref_no = random.randint(1000, 9999)
			
			# Check if this number already exists
			existing = frappe.db.exists("SRN POST", {"srn_ref_no": srn_ref_no})
			if not existing:
				return srn_ref_no
			
			attempt += 1
		
		# If we couldn't find a unique number after max_attempts, 
		# fall back to sequential numbering starting from 1000
		last_number = frappe.db.sql("""
			SELECT MAX(CAST(srn_ref_no AS UNSIGNED)) 
			FROM `tabSRN POST` 
			WHERE srn_ref_no REGEXP '^[0-9]+$'
		""")
		
		if last_number and last_number[0][0]:
			next_number = int(last_number[0][0]) + 1
		else:
			next_number = 1000
		
		# Ensure it's 4 digits
		return next_number if next_number <= 9999 else 1000
	
	def before_save(self):
		# Ensure srn_ref_no is set before saving
		if not self.srn_ref_no:
			self.srn_ref_no = self.generate_unique_srn_ref_no()
	
	@frappe.whitelist()
	def generate_srn_ref_no(self):
		"""Server-side method to generate unique SRN Reference number"""
		return self.generate_unique_srn_ref_no()
