import json
import frappe
from erpnext.stock.get_item_details import get_item_details as core_get_item_details

def _safe_json_loads(obj):
    if obj and isinstance(obj, str):
        try:
            return json.loads(obj)
        except Exception:
            return None
    return obj

def _call_core(args, doc, for_update=False, overwrite_warehouse=False):
    try:
        return core_get_item_details(args, doc, for_update)  # older signature
    except TypeError:
        try:
            return core_get_item_details(args, doc, overwrite_warehouse=overwrite_warehouse)  # newer
        except TypeError:
            return core_get_item_details(args, doc)

@frappe.whitelist()
def get_item_details(args, doc=None, for_update=False, overwrite_warehouse=False):
    # --- Parse inputs
    args_obj = _safe_json_loads(args) or args
    doc_obj = _safe_json_loads(doc)

    row_name = args_obj.get("name") if isinstance(args_obj, dict) else None

    # --- Call core
    out = _call_core(args_obj, doc, for_update=for_update, overwrite_warehouse=overwrite_warehouse)
    if not isinstance(out, dict):
        out = frappe._dict(out)

    # --- Find same child row from docs
    current_row = None
    if isinstance(doc_obj, dict):
        for d in (doc_obj.get("items") or []):
            if d.get("name") == row_name:
                current_row = d
                break

    # --- Protect fields: don't let core blank them
    protected_selects = [
        "custom_srv_number",
        "custom_warehouse_s_program",
        "custom_target_stock_select",
        "custom_sprogram_save",
        "custom_tprogram_save",
    ]
    protected_links = ["s_warehouse", "t_warehouse"]

    if current_row:
        for field in protected_selects + protected_links:
            val = current_row.get(field)
            if val not in (None, "", [], 0):
                out[field] = val

        # Mirror logic if you want label==link scenarios
        if current_row.get("s_warehouse") and current_row.get("custom_sprogram_save") == current_row.get("s_warehouse"):
            out["custom_warehouse_s_program"] = current_row.get("s_warehouse")

        if current_row.get("t_warehouse") and current_row.get("custom_tprogram_save") == current_row.get("t_warehouse"):
            out["custom_target_stock_select"] = current_row.get("t_warehouse")

    # 👇 Visible flag in Network response to confirm override is active
    out["_ursc_override_applied"] = True

    # 👇 Server log to bench
    frappe.logger("ursc").info(f"[URSCCMS OVERRIDE] get_item_details hit; row={row_name}, protected_applied={bool(current_row)}")

    return out
