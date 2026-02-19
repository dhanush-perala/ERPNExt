#i changed the js and i did not change my api.py code import json

import frappe
import json
import json

import frappe

from frappe import _

from frappe.desk.search import search_link as core_search_link

from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

from frappe.utils import today, getdate, add_years, formatdate
from frappe.utils import getdate, add_years

 
 
# ----------------------------------------------------------------------

# Fix Item title field (avoids "Unknown column ''" errors)

# ----------------------------------------------------------------------
import frappe

@frappe.whitelist()
def get_po_details(purchase_order):
    """Fetch Purchase Order with items and map to SRV ENTRY structure"""
    if not purchase_order:
        return {}

    po = frappe.get_doc("Purchase Order", purchase_order)

    items = []
    for d in po.items:
        # Get Item Group from Item master
        item_group = None
        if d.item_code:
            item_group = frappe.db.get_value("Item", d.item_code, "item_group")

        items.append({
            # ---- Child Table Mapping ----
            "srv_part_no": d.get("supplier_part_no"),  # PO Item.supplier_part_no → SRV ENT TABLE.srv_part_no
            "odered_qty": d.get("qty"),                # PO Item.qty → SRV ENT TABLE.odered_qty (your actual fieldname spelling)
            "u_cost": d.get("rate"),                   # PO Item.rate → SRV ENT TABLE.u_cost
            "comp_type": item_group                    # Item.item_group → SRV ENT TABLE.comp_type
            # rec_qty and ret_qty remain entry fields → not pre-filled
        })

    return {
        # ---- Parent Mapping ----
        "po_no": po.name,
        "po_date": po.transaction_date,
        "project": po.project,
        "items": items
    }

def fix_item_title_field():
    """Ensure Item doctype has a valid title_field (persisted)."""
    meta = frappe.get_meta("Item")
    if not meta.title_field or not frappe.db.has_column("Item", meta.title_field):
        frappe.db.set_value("DocType", "Item", "title_field", "item_name")
        frappe.clear_cache(doctype="Item")


def fix_item_title_field():

    """Ensure Item doctype has a valid title_field."""

    meta = frappe.get_meta("Item")

    if not meta.title_field:

        meta.title_field = "item_name"
 
 
# ----------------------------------------------------------------------

# Link search wrapper (active items only)

# ----------------------------------------------------------------------

@frappe.whitelist()

@frappe.validate_and_sanitize_search_inputs

def search_link_only_active_items(

    doctype,

    txt,

    searchfield=None,

    start=0,

    page_len=20,

    filters=None,

    reference_doctype=None,

    ignore_user_permissions=0,

):

    """Global link search wrapper. If Item, enforce active results."""

    if doctype == "Item":

        filters = filters or {}

        if frappe.db.has_column("Item", "custom_status"):

            filters.setdefault("custom_status", "Active")
 
    return core_search_link(

        doctype=doctype,

        txt=txt,

        searchfield=searchfield,

        start=start,

        page_len=page_len,

        filters=filters,

        reference_doctype=reference_doctype,

        ignore_user_permissions=ignore_user_permissions,

    )
 
 
# ----------------------------------------------------------------------

# Query: items filtered by Supplier (for Purchase Order)

# ----------------------------------------------------------------------

@frappe.whitelist()

@frappe.validate_and_sanitize_search_inputs

def item_by_supplier(doctype, txt, searchfield, start, page_len, filters):

    """Return items linked to Supplier via Item Supplier child table."""

    if isinstance(filters, str):

        try:

            filters = json.loads(filters)

        except Exception:

            filters = {}
 
    supplier = (filters or {}).get("supplier")

    if not supplier:

        return []
 
    like = f"%{txt or ''}%"
 
    return frappe.db.sql(

        """

        SELECT DISTINCT

            i.name,

            COALESCE(NULLIF(i.item_name, ''), i.name) AS label

        FROM `tabItem` i

        INNER JOIN `tabItem Supplier` s

            ON s.parent = i.name

           AND s.supplier = %(supplier)s

        WHERE COALESCE(i.disabled, 0) = 0

          AND (i.name LIKE %(like)s OR i.item_name LIKE %(like)s)

        ORDER BY i.name

        LIMIT %(start)s, %(page_len)s

        """,

        {

            "supplier": supplier,

            "like": like,

            "start": start,

            "page_len": page_len,

        },

    )
 
 
# ----------------------------------------------------------------------

# Validation: block PO save if items not supplied by selected Supplier

# ----------------------------------------------------------------------
#po no need to validate the supplier

def validate_supplier_items(doc, method=None):

    """Block saving if PO contains items the chosen Supplier does not supply."""

    if not getattr(doc, "supplier", None) or not getattr(doc, "items", None):

        return
 
    po_items = [d.item_code for d in doc.items if getattr(d, "item_code", None)]

    if not po_items:

        return
 
    supplier_norm = (doc.supplier or "").strip()
 
    rows = frappe.db.sql(

        """

        SELECT i.name AS item_code

        FROM `tabItem` i

        LEFT JOIN `tabItem Supplier` s_item

               ON s_item.parent = i.name

              AND LOWER(TRIM(s_item.supplier)) = LOWER(TRIM(%(supplier)s))

        LEFT JOIN `tabItem Supplier` s_tpl

               ON s_tpl.parent = i.variant_of

              AND i.variant_of IS NOT NULL AND i.variant_of != ''

              AND LOWER(TRIM(s_tpl.supplier)) = LOWER(TRIM(%(supplier)s))

        WHERE i.name IN %(po_items)s

          AND (s_item.name IS NOT NULL OR s_tpl.name IS NOT NULL)

        """,

        {"supplier": supplier_norm, "po_items": tuple(po_items)},

    )

    allowed_items = {r[0] for r in rows}
 
    invalid_rows = [

        "Component At "+f"<b>Row {d.idx}</b>:  {frappe.utils.escape_html(d.item_code)}"
        #+ (f" ({frappe.utils.escape_html(d.item_name)})" if getattr(d, "item_name", None) else "")
        f"Row {d.idx}: {frappe.utils.escape_html(d.item_code)}"

        + (f" ({frappe.utils.escape_html(d.item_name)})" if getattr(d, "item_name", None) else "")

        for d in doc.items

        if getattr(d, "item_code", None) and d.item_code not in allowed_items

    ]
 
    if invalid_rows:

        msg = (

            f"⚠️ The following items are not supplied by the Supplier <b>{frappe.utils.escape_html(supplier_norm)}</b>:<br>"

            + "<br>".join(invalid_rows)

            + "<br><br>Please remove them from the Purchase Order, or Select Other supplier "
            f"⚠️ The following items are not supplied by <b>{frappe.utils.escape_html(supplier_norm)}</b>:<br>"

            + "<br>".join(invalid_rows)

            + "<br><br>Please remove them from the Purchase Order, or add the supplier under "

              "<b>Item → Suppliers</b> (on the item or its template)."

        )

        frappe.throw(msg, title="Invalid Supplier Items")
 
 
# ----------------------------------------------------------------------

# Stock Entry helpers: fetch base part no + build MDB part no

# ----------------------------------------------------------------------
@frappe.whitelist()
def get_basic_part_number(item_code: str, supplier: str | None = None) -> str:
    """Return Item Supplier.basic_part_number for this item.
    Prefer exact supplier when provided; else fall back to the first row.
    """
    if not item_code:
        return ""

    params = {"item_code": item_code, "supplier": supplier}
    supplier_filter = "AND si.supplier = %(supplier)s" if supplier else ""

    rows = frappe.db.sql(
        f"""
        SELECT si.basic_part_number
        FROM `tabItem Supplier` si
        WHERE si.parent = %(item_code)s
        {supplier_filter}
        ORDER BY
            CASE WHEN %(supplier)s IS NOT NULL AND si.supplier = %(supplier)s THEN 0 ELSE 1 END,
            si.idx
        LIMIT 1
        """,
        params,
    )
    return (rows[0][0] or "") if rows else ""

def populate_mdb_part_no(doc, method=None):
    """On Stock Entry validate: generate MDB part no (format: base_part_no-quality)."""
    items = getattr(doc, "items", []) or []

    for d in items:
        base = d.custom_base_part_no or ""
        qual = d.custom_quality_save or ""

        if base and qual:
            d.custom_mdb_part_no = f"{base}-{qual}"
        else:
            d.custom_mdb_part_no = base or qual or ""

@frappe.whitelist()
def get_base_parts_by_link(link_part_no: str, supplier: str | None = None):
    if not link_part_no:
        return []

    params = {"link": link_part_no}
    supplier_join = ""
    supplier_where = ""

    # If you want to also restrict by selected Supplier
    if supplier:
        supplier_join = "LEFT JOIN `tabItem Supplier` isup ON isup.parent = i.name"
        supplier_where = "AND (isup.supplier = %(supplier)s)"
        params["supplier"] = supplier

    rows = frappe.db.sql(
        f"""
        SELECT DISTINCT i.name, i.item_name
        FROM `tabItem` i
        {supplier_join}
        WHERE i.custom_save_link_part = %(link)s
          AND COALESCE(i.disabled,0) = 0
          {supplier_where}
        ORDER BY i.name
        """,
        params,
        as_dict=True,
    )
    return rows
@frappe.whitelist()
def map_mr_parent_fields(doc, method=None):
    """
    Map parent-level fields from Material Request → Purchase Order.
    Runs on before_save of PO.
    """
    if not getattr(doc, "material_request", None):
        return

    parent_field_map = {
        "custom_select_projet": "custom_select_project",
        "custom_select_subsystem": "custom_select_subsystem",
        "custom_select_package": "custom_select_package",
        "custom_select_project_card": "custom_select_project_card",
    }

    mr_values = frappe.db.get_value(
        "Material Request",
        doc.material_request,
        list(parent_field_map.keys()),
        as_dict=True,
    )

    if mr_values:
        for mr_field, po_field in parent_field_map.items():
            if mr_values.get(mr_field) and not doc.get(po_field):
                doc.set(po_field, mr_values[mr_field])

@frappe.whitelist()
def get_srv_parts_by_item(item_code):
    """Return SRV Part Nos (supplier_part_no) linked to an Item."""
    if not item_code:
        return []
    return frappe.db.sql("""
        SELECT supplier_part_no
        FROM `tabItem Supplier`
        WHERE parent = %s
    """, item_code, as_dict=True)
@frappe.whitelist()
def get_srv_parts_options(item_code: str, supplier: str | None = None):
    """
    Return SRV Part Nos as a list of strings for a given Item (Base Part),
    filtered by supplier (case-insensitive) if provided.
    Used to populate options for custom_select_srv_part_no (Select field).
    """
    if not item_code:
        return []

    params = {"item_code": item_code, "supplier": supplier}
    supplier_clause = ""
    if supplier:
        supplier_clause = "AND LOWER(TRIM(s.supplier)) = LOWER(TRIM(%(supplier)s))"

    rows = frappe.db.sql(
        f"""
        SELECT DISTINCT s.supplier_part_no
        FROM `tabItem Supplier` s
        WHERE s.parent = %(item_code)s
          AND COALESCE(s.supplier_part_no, '') != ''
          {supplier_clause}
        ORDER BY s.idx, s.supplier_part_no
        """,
        params,
        as_dict=True,
    )

    return [r["supplier_part_no"] for r in rows if r.get("supplier_part_no")]
@frappe.whitelist()
def get_linkpart_by_item(item_code):
    """Return Link Part for an Item (custom_save_link_part)."""
    if not item_code:
        return None
    return frappe.db.get_value("Item", item_code, "custom_save_link_part")
#po get link part data for child rows
@frappe.whitelist()
def map_mr_custom_fields(doc, method=None):
    """
    When creating Purchase Order Items from Material Request:
    - copy `custom_link_part_no` from MR Item if it exists
    - else pull from Item (prefer custom_save_link_part, fallback to custom_select_link_part_number)
    """
    for d in doc.get("items", []):
        # Case 1: If MR item has a link part, copy it
        if d.material_request_item and not d.custom_link_part_no:
            link_part = frappe.db.get_value(
                "Material Request Item",
                d.material_request_item,
                "custom_link_part_no"
            )
            if link_part:
                d.custom_link_part_no = link_part
                continue

        # Case 2: Fall back to Item master
        if not d.custom_link_part_no and d.item_code:
            # Try custom_save_link_part first
            link_part = frappe.db.get_value("Item", d.item_code, "custom_save_link_part")
            if not link_part:
                # Fall back to custom_select_link_part_number (Link field)
                link_part = frappe.db.get_value("Item", d.item_code, "custom_select_link_part_number")
            if link_part:
                d.custom_link_part_no = link_part

@frappe.whitelist()
def get_srv_parts_for_item(doctype, txt, searchfield, start, page_len, filters):
    """
    Return SRV Part Nos (custom_select_supplier_part_no) for a given Item.
    This is used in Purchase Order Item → custom_select_supplier_part_no link field.
    Must return list of [value, label] tuples.
    """
    if isinstance(filters, str):
        try:
            filters = json.loads(filters)
        except Exception:
            filters = {}

    item_code = (filters or {}).get("item_code")
    if not item_code:
        return []

    like = f"%{txt or ''}%"

    rows = frappe.db.sql(
        """
        SELECT supplier_part_no
        FROM `tabItem Supplier`
        WHERE parent = %(item_code)s
          AND supplier_part_no LIKE %(like)s
        ORDER BY supplier_part_no
        LIMIT %(start)s, %(page_len)s
        """,
        {"item_code": item_code, "like": like, "start": start, "page_len": page_len},
        as_dict=True,
    )

    # Return list of [value, label]
    return [[r["supplier_part_no"], r["supplier_part_no"]] for r in rows if r.get("supplier_part_no")]

#GET PURCHASE INVOICE TO PURCHASE RECEIPT GET FIELDS
def map_bill_no_to_custom(doc, method):
    """Automatically copy bill_no → custom_enter_srv_part_number before save"""
    if doc.bill_no:
        doc.custom_enter_srv_part_number = doc.bill_no
@frappe.whitelist()
def custom_make_purchase_receipt(source_name, target_doc=None):
    """
    Custom override of make_purchase_receipt to map
    Supplier Invoice No (bill_no) into each Purchase Receipt Item row.
    """
    def update_item(source_doc, target_doc, source_parent):
        # Set custom field from parent PI
        target_doc.custom_srv_part_number = source_parent.custom_enter_srv_part_number

    doclist = get_mapped_doc(
        "Purchase Invoice",
        source_name,
        {
            "Purchase Invoice": {
                "doctype": "Purchase Receipt",
                "field_map": {
                    "supplier": "supplier",
                    "posting_date": "posting_date",
                },
            },
            "Purchase Invoice Item": {
                "doctype": "Purchase Receipt Item",
                "field_map": {
                    "item_code": "item_code",
                    "qty": "qty",
                    "rate": "rate",
                    "amount": "amount",
                },
                "postprocess": update_item,
            },
        },
        target_doc,
    )
    return doclist
def set_pr_item_status_to_be_screened(doc, method):
    """When Purchase Receipt is submitted, mark all items as To Be Screened"""
    for item in doc.items:
        frappe.db.set_value(
            "Purchase Receipt Item",
            item.name,
            "custom_item_status",
            "To Be Screened"
        )
def update_item_status_quality_checked(doc, method):
    """When Stock Entry is submitted, update related PR Item status"""
    if doc.purpose != "Material Transfer for Quality Check":
        return  # only apply for this purpose

    for item in doc.items:
        if item.purchase_receipt and item.pr_detail:  
            # item.purchase_receipt = linked PR docname
            # item.pr_detail = linked Purchase Receipt Item row

            # Update that PR Item row
            frappe.db.set_value(
                "Purchase Receipt Item",
                item.pr_detail,
                "custom_item_status",
                "Quality Checked"
            )
# get items purchase receipt to stock entry
'''
@frappe.whitelist()
def make_stock_entry(source_name, target_doc=None, args=None):
    def set_missing_values(source, target):
        target.stock_entry_type = "Material Transfer"
        target.purpose = "Material Transfer"
        target.set_missing_values()
 
    doclist = get_mapped_doc(
        "Purchase Receipt",
        source_name,
        {
            "Purchase Receipt": {
                "doctype": "Stock Entry",
            },
            "Purchase Receipt Item": {
                "doctype": "Stock Entry Detail",
                "field_map": {
                    "warehouse": "s_warehouse",
                    "parent": "reference_purchase_receipt",
                    "batch_no": "batch_no",
                },
            },
        },
        target_doc,
        set_missing_values,
    )
 
    return doclist'''
#updated make stock entry let's check
'''
@frappe.whitelist()
def make_stock_entry_with_srv(source_name, target_doc=None, args=None):
    def set_missing_values(source, target):
        # Respect what the user selected
        if not target.stock_entry_type:
            target.stock_entry_type = "Material Issue"  # default fallback
        target.set_missing_values()

        # Propagate warehouses dynamically
        if target.stock_entry_type == "Material Issue" and target.from_warehouse:
            for d in target.items:
                d.s_warehouse = target.from_warehouse

        if target.stock_entry_type == "Material Receipt" and target.to_warehouse:
            for d in target.items:
                d.t_warehouse = target.to_warehouse

        if target.stock_entry_type == "Material Transfer":
            for d in target.items:
                if target.from_warehouse:
                    d.s_warehouse = target.from_warehouse
                if target.to_warehouse:
                    d.t_warehouse = target.to_warehouse

    doclist = get_mapped_doc(
        "Purchase Receipt",
        source_name,
        {
            "Purchase Receipt": {"doctype": "Stock Entry"},
            "Purchase Receipt Item": {
                "doctype": "Stock Entry Detail",
                "field_map": {
                    "warehouse": "s_warehouse",   # maps PR.warehouse → Stock Entry.s_warehouse
                    "parent": "reference_purchase_receipt",
                    "batch_no": "batch_no",
                },
            },
        },
        target_doc,
        set_missing_values,
    )

    return doclist
'''
#updated during the benguluru visit
@frappe.whitelist()
def make_stock_entry_with_srv(source_name, target_doc=None, args=None):
    def set_missing_values(source, target):
        # ✅ Map parent-level custom fields from PR → SE
        target.custom_enter_po_no = source.custom_enter_po_no
        target.custom_select_po_date = source.custom_select_po_date
        target.custom_select_project = source.custom_project_save   # 👈 map PR.custom_project_save → SE.custom_select_project

        # Respect what the user selected
        if not target.stock_entry_type:
            target.stock_entry_type = "Material Issue"  # default fallback
        target.set_missing_values()

        # Propagate warehouses dynamically
        if target.stock_entry_type == "Material Issue" and target.from_warehouse:
            for d in target.items:
                d.s_warehouse = target.from_warehouse

        if target.stock_entry_type == "Material Receipt" and target.to_warehouse:
            for d in target.items:
                d.t_warehouse = target.to_warehouse

        if target.stock_entry_type == "Material Transfer":
            for d in target.items:
                if target.from_warehouse:
                    d.s_warehouse = target.from_warehouse
                if target.to_warehouse:
                    d.t_warehouse = target.to_warehouse

    doclist = get_mapped_doc(
        "Purchase Receipt",
        source_name,
        {
            "Purchase Receipt": {
                "doctype": "Stock Entry",
                "field_map": {
                    "custom_enter_po_no": "custom_enter_po_no",
                    "custom_select_po_date": "custom_select_po_date",
                    "custom_project_save": "custom_select_project",  # 👈 field_map version also added
                },
            },
            "Purchase Receipt Item": {
                "doctype": "Stock Entry Detail",
                "field_map": {
                    "warehouse": "s_warehouse",
                    "parent": "reference_purchase_receipt",
                    "batch_no": "batch_no",
                },
            },
        },
        target_doc,
        set_missing_values,
    )

    return doclist

 #map srv no to child rows of the stock enty
@frappe.whitelist()
def custom_pr_from_po(source_name, target_doc=None):
    """
    Custom mapping: PO → PR
    Copies qty into custom_requested_quantity
    """
    def update_item(source_doc, target_doc, source_parent):
        # push PO Item.qty → PR Item.custom_requested_quantity
        if getattr(source_doc, "qty", None):
            target_doc.custom_requested_quantity = source_doc.qty

    doc = get_mapped_doc(
        "Purchase Order",
        source_name,
        {
            "Purchase Order": {
                "doctype": "Purchase Receipt",
                "field_map": {
                    "supplier": "supplier",
                    "transaction_date": "posting_date",
                },
            },
            "Purchase Order Item": {
                "doctype": "Purchase Receipt Item",
                "field_map": {
                    "item_code": "item_code",
                    "qty": "qty",
                    "rate": "rate",
                    "amount": "amount",
                },
                "postprocess": update_item,
            },
        },
        target_doc,
    )
    return doc
#get from pi
@frappe.whitelist()
def custom_pr_from_pi(source_name, target_doc=None):
    """
    Custom mapping: PI → PR
    Copies qty into custom_requested_quantity
    """
    def update_item(source_doc, target_doc, source_parent):
        if getattr(source_doc, "qty", None):
            target_doc.custom_requested_quantity = source_doc.qty

    doc = get_mapped_doc(
        "Purchase Invoice",
        source_name,
        {
            "Purchase Invoice": {
                "doctype": "Purchase Receipt",
                "field_map": {
                    "supplier": "supplier",
                    "posting_date": "posting_date",
                },
            },
            "Purchase Invoice Item": {
                "doctype": "Purchase Receipt Item",
                "field_map": {
                    "item_code": "item_code",
                    "qty": "qty",
                    "rate": "rate",
                    "amount": "amount",
                },
                "postprocess": update_item,
            },
        },
        target_doc,
    )
    return doc



@frappe.whitelist()
def custom_make_purchase_receipt(source_name, target_doc=None):
    """
    Custom override of make_purchase_receipt
    Map qty → custom_order_qty
    And map custom_enter_srv_part_number → custom_srv_part_number
    """

    def update_item(source_doc, target_doc, source_parent):
        # Ensure srv part number also comes from PI parent
        if getattr(source_parent, "custom_enter_srv_part_number", None):
            target_doc.custom_srv_part_number = source_parent.custom_enter_srv_part_number

    doclist = get_mapped_doc(
        "Purchase Invoice",      # source doctype
        source_name,
        {
            "Purchase Invoice": {
                "doctype": "Purchase Receipt",
                "field_map": {
                    "supplier": "supplier",
                    "posting_date": "posting_date",
                },
            },
            "Purchase Invoice Item": {
                "doctype": "Purchase Receipt Item",
                "field_map": {
                    "item_code": "item_code",
                    "qty": "qty",                      # Standard qty
                    "qty": "custom_requested_quantity",         # Map also into custom_order_qty
                    "rate": "rate",
                    "amount": "amount",
                },
                "postprocess": update_item,
            },
        },
        target_doc,
    )

    return doclist
#show list basic mdb against that item in stock entry
#get the list of basic mdb for that item
CHILD_TABLE = "basic_mdb_child_table"

CHILD_FIELD = "enter_basic_mdb"
ITEM_FIELD = "custom_addedit_basic_mdb"
@frappe.whitelist()
def get_basic_mdb_options(item_code: str = None, item_code_or_group: str = None):
    """
    Return Basic MDB values for:
      • An Item's child table rows (enter_basic_mdb)
      • Else fallback to Item.custom_addedit_basic_mdb
      • Else fallback to its Item Group’s child rows
      • Or directly from an Item Group
    """
    key = (item_code_or_group or item_code or "").strip()
    if not key:
        return []

    # Case 1: Item
    if frappe.db.exists("Item", key):
        # 1a. Pull from Item’s child table
        rows = frappe.get_all(
            CHILD_TABLE,
            filters={"parent": key, "parenttype": "Item"},
            fields=[CHILD_FIELD],
            order_by="idx",
        )
        values = [r.get(CHILD_FIELD) for r in rows if r.get(CHILD_FIELD)]
        if values:
            return values

        # 1b. Fallback to Item.custom_addedit_basic_mdb
        single_val = frappe.db.get_value("Item", key, ITEM_FIELD)
        if single_val:
            return [single_val]

        # 1c. Fallback to Item Group
        item_group = frappe.db.get_value("Item", key, "item_group")
        if item_group:
            return _get_mdb_from_item_group(item_group)
        return []

    # Case 2: Item Group directly
    if frappe.db.exists("Item Group", key):
        return _get_mdb_from_item_group(key)

    return []


def _get_mdb_from_item_group(item_group: str):
    rows = frappe.db.sql(
        f"""
        SELECT DISTINCT c.{CHILD_FIELD}
        FROM `tab{CHILD_TABLE}` c
        JOIN `tabItem` i ON i.name = c.parent
        WHERE c.parenttype = 'Item'
          AND i.item_group = %s
          AND COALESCE(c.{CHILD_FIELD}, '') != ''
        ORDER BY c.{CHILD_FIELD}
        """,
        (item_group,),
        as_dict=True,
    )
    return [r.get(CHILD_FIELD) for r in rows if r.get(CHILD_FIELD)]
#list of ware of that warehouses
''' working
@frappe.whitelist()
def get_child_warehouses(parent: str):
    """
    Return all child warehouses (is_group = 0) under the given group warehouse.
    Accepts either internal `name` (e.g. "Bangalore Stores - tc")
    or human-readable `warehouse_name` (e.g. "Bangalore Stores").
    """
    if not parent:
        return []

    # Try to resolve to internal warehouse "name"
    parent_name = (
        frappe.db.get_value("Warehouse", parent, "name")
        or frappe.db.get_value("Warehouse", {"warehouse_name": parent}, "name")
    )
    if not parent_name:
        return []

    rows = frappe.db.sql("""
        SELECT w.warehouse_name
        FROM `tabWarehouse` w
        WHERE w.parent_warehouse = %(parent)s
          AND w.is_group = 0
        ORDER BY w.warehouse_name
        LIMIT 50
    """, {"parent": parent_name}, as_dict=True)

    return [r["warehouse_name"] for r in rows]'''

@frappe.whitelist()
def get_child_warehouses(parent: str):
    """
    Return all child warehouses (is_group = 0) under the given group warehouse.
    Returns both internal name (`name`) and human-readable warehouse_name (`label`).
    """
    if not parent:
        return []

    # Resolve to internal name
    parent_name = (
        frappe.db.get_value("Warehouse", parent, "name")
        or frappe.db.get_value("Warehouse", {"warehouse_name": parent}, "name")
    )
    if not parent_name:
        return []

    rows = frappe.db.sql("""
        SELECT w.name, w.warehouse_name
        FROM `tabWarehouse` w
        WHERE w.parent_warehouse = %(parent)s
          AND w.is_group = 0
        ORDER BY w.warehouse_name
        LIMIT 50
    """, {"parent": parent_name}, as_dict=True)

    # 👇 Always return dict with name + label
    return [{"name": r["name"], "label": r["warehouse_name"]} for r in rows]

def validate_expiry_date(doc, method=None):
    """Hard validation: Expiry cannot be > today + 5 years."""
    from frappe.utils import getdate, add_years # type: ignore
    limit = add_years(getdate(), 5)

    frappe.logger().debug(f"[validate_expiry_date] Running for Stock Entry {doc.name}")

    for d in (doc.items or []):
        if d.custom_exp_date and getdate(d.custom_exp_date) > limit:
            frappe.throw(
                f"Row #{d.idx}: Expiry Date {d.custom_exp_date} "
                f"cannot be more than 5 years from today."
            )

@frappe.whitelist()
def get_basic_part_number(item_code: str) -> str:
    """Always return the first basic_part_number linked to the item."""
    if not item_code:
        return ""

    rows = frappe.db.sql(
        """
        SELECT si.basic_part_number
        FROM `tabItem Supplier` si
        WHERE si.parent = %(item_code)s
        ORDER BY si.idx
        LIMIT 1
        """,
        {"item_code": item_code},
    )

    return (rows[0][0] or "") if rows else ""

 
 
def populate_mdb_part_no(doc, method=None):

    """On Stock Entry validate: fill base_part_no and generate MDB part no."""

    items = getattr(doc, "items", []) or []

    parent_supplier = getattr(doc, "supplier", None)
 
    for d in items:

        if getattr(d, "item_code", None) and not getattr(d, "custom_base_part_no", None):

            d.custom_base_part_no = get_basic_part_number(d.item_code, parent_supplier)
 
        base = d.custom_base_part_no or ""

        qual = d.custom_quality_save or ""

        d.custom_mdb_part_no = f"{qual}{base}"

 
