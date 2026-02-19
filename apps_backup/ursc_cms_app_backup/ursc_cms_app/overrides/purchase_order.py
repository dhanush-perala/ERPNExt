import frappe
from erpnext.buying.doctype.purchase_order.purchase_order import PurchaseOrder

# MR → PO mapping
MR_TO_PO_CUSTOM_FIELDS = {
    "custom_select_projet": "custom_select_project",
    "custom_select_subsystem": "custom_select_subsystem",
    "custom_select_package": "custom_select_package",
    "custom_select_project_card": "custom_select_project_card",
}

class CustomPurchaseOrder(PurchaseOrder):
    def set_missing_values(self, for_validate=False):
        super().set_missing_values(for_validate=for_validate)

        if getattr(self, "from_material_request", None):
            for d in self.get("items", []):
                if d.material_request_item:
                    mr_item = frappe.db.get_value(
                        "Material Request Item",
                        d.material_request_item,
                        list(MR_TO_PO_CUSTOM_FIELDS.keys()),
                        as_dict=True,
                    )
                    if mr_item:
                        for mr_field, po_field in MR_TO_PO_CUSTOM_FIELDS.items():
                            value = mr_item.get(mr_field)
                            if value:
                                d.set(po_field, value)

