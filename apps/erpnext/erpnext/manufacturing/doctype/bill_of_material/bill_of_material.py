# Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class BillofMaterial(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from erpnext.manufacturing.doctype.bom_explosion_item.bom_explosion_item import BOMExplosionItem
		from erpnext.manufacturing.doctype.bom_items.bom_items import BOMItems
		from erpnext.manufacturing.doctype.bom_operation.bom_operation import BOMOperation
		from erpnext.manufacturing.doctype.bom_scrap_item.bom_scrap_item import BOMScrapItem
		from frappe.types import DF

		allow_alternative_item: DF.Check
		amended_from: DF.Link | None
		base_operating_cost: DF.Currency
		base_raw_material_cost: DF.Currency
		base_scrap_material_cost: DF.Currency
		base_total_cost: DF.Currency
		bom_creator: DF.Link | None
		bom_creator_item: DF.Data | None
		buying_price_list: DF.Link | None
		card_name: DF.Link | None
		card_type: DF.Literal["Select", "Subsystem", "Production"]
		company: DF.Link | None
		conversion_rate: DF.Float
		currency: DF.Link
		description: DF.SmallText | None
		exploded_items: DF.Table[BOMExplosionItem]
		fabrication_remarks: DF.SmallText | None
		fg_based_operating_cost: DF.Check
		function: DF.Data | None
		has_variants: DF.Check
		image: DF.AttachImage | None
		inspection_required: DF.Check
		is_active: DF.Check
		is_default: DF.Check
		item: DF.Link | None
		item_name: DF.Data | None
		items: DF.Table[BOMItems]
		operating_cost: DF.Currency
		operating_cost_per_bom_quantity: DF.Currency
		operations: DF.Table[BOMOperation]
		plc_conversion_rate: DF.Float
		price_list_currency: DF.Link | None
		process_loss_percentage: DF.Percent
		process_loss_qty: DF.Float
		project: DF.Link | None
		quality_inspection_template: DF.Link | None
		quantity: DF.Float
		raw_material_cost: DF.Currency
		rm_cost_as_per: DF.Literal["Valuation Rate", "Last Purchase Rate", "Price List"]
		route: DF.SmallText | None
		routing: DF.Link | None
		scrap_items: DF.Table[BOMScrapItem]
		scrap_material_cost: DF.Currency
		set_rate_of_sub_assembly_item_based_on_bom: DF.Check
		show_in_website: DF.Check
		show_items: DF.Check
		show_operations: DF.Check
		template_bom: DF.Link | None
		thumbnail: DF.Data | None
		total_cost: DF.Currency
		transfer_material_against: DF.Literal["", "Work Order", "Job Card"]
		uom: DF.Link | None
		web_long_description: DF.TextEditor | None
		website_image: DF.AttachImage | None
		with_operations: DF.Check
	# end: auto-generated types
	pass
