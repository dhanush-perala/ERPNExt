import unittest
import frappe
from frappe.tests.utils import FrappeTestCase

class TestSRNPOST(FrappeTestCase):
	def setUp(self):
		# Create a test SRN POST document
		self.srn_post = frappe.get_doc({
			"doctype": "SRN POST",
			"srn_ref_no": None  # Will be auto-generated
		})
	
	def test_srn_ref_no_generation(self):
		"""Test that SRN Reference number is automatically generated"""
		# Save the document
		self.srn_post.insert()
		
		# Check that srn_ref_no is generated
		self.assertIsNotNone(self.srn_post.srn_ref_no)
		self.assertIsInstance(self.srn_post.srn_ref_no, int)
		self.assertGreaterEqual(self.srn_post.srn_ref_no, 1000)
		self.assertLessEqual(self.srn_post.srn_ref_no, 9999)
	
	def test_srn_ref_no_uniqueness(self):
		"""Test that generated SRN Reference numbers are unique"""
		# Create multiple SRN POST documents
		srn_posts = []
		for i in range(5):
			srn_post = frappe.get_doc({
				"doctype": "SRN POST",
				"srn_ref_no": None
			})
			srn_post.insert()
			srn_posts.append(srn_post)
		
		# Check that all SRN Reference numbers are unique
		srn_ref_nos = [doc.srn_ref_no for doc in srn_posts]
		self.assertEqual(len(srn_ref_nos), len(set(srn_ref_nos)))
		
		# Clean up
		for doc in srn_posts:
			doc.delete()
	
	def tearDown(self):
		# Clean up test data
		if hasattr(self, 'srn_post') and self.srn_post.name:
			self.srn_post.delete()
