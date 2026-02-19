# Copyright (c) 2025, neemus and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AddProjectCard(Document):
	def validate(self):
		# pack_code is optional (read_only field), but try to auto-fill if possible
		# If pack_code is not set and select_sub_system is set, try to find a matching PRJ_PACK
		if not self.pack_code and self.select_sub_system:
			# Try to find a PRJ_PACK linked to this subsystem
			pack = frappe.db.get_value(
				"PRJ_PACK",
				{"select_sub_system": self.select_sub_system},
				"name",
				order_by="modified desc"
			)
			if pack:
				self.pack_code = pack
		# Allow saving even if pack_code is empty (it's no longer required)
