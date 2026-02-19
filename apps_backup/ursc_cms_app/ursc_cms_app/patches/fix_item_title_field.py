import frappe

def execute():
    meta = frappe.get_meta("Item")
    if not meta.title_field:
        meta.title_field = "item_name"
        frappe.db.set_value("DocType", "Item", "title_field", "item_name")
        frappe.db.commit()
        print("✅ Item DocType title_field set to 'item_name'")
    else:
        print("✅ Item DocType already has a title_field")
