import frappe
import json
from frappe import _
import io

from PyPDF2 import PdfMerger
from frappe.utils.pdf import get_pdf
from frappe.utils import escape_html

from frappe.desk.search import search_link as core_search_link

from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

from frappe.utils import today, getdate, add_years, formatdate
from frappe.utils import getdate, add_years


# ursc_cms_app/api.py
import frappe

@frappe.whitelist()
def get_date_codes(component_type):
    """
    Returns a list of custom_date_code from Stock Entry Detail
    filtered by component_type (custom_select_component_type)
    """
    if not component_type:
        return []

    result = frappe.get_all(
        "Stock Entry Detail",
        filters={"custom_select_component_type": component_type},
        fields=["custom_date_code"]
    )

    # Remove duplicates and empty values
    codes = list({row['custom_date_code'] for row in result if row['custom_date_code']})
    return codes

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

        for d in doc.items

        if getattr(d, "item_code", None) and d.item_code not in allowed_items

    ]
 
    if invalid_rows:

        msg = (

            f" The following items are not supplied by the Supplier <b>{frappe.utils.escape_html(supplier_norm)}</b>:<br>"

            + "<br>".join(invalid_rows)

            + "<br><br>Please remove them from the Purchase Order, or Select Other supplier "

        )

        frappe.throw(msg, title="Invalid Supplier Items")
 
 
# ----------------------------------------------------------------------

# Stock Entry helpers: fetch base part no + build MDB part no

# ----------------------------------------------------------------------
@frappe.whitelist()
def get_basic_part_number(item_code: str, supplier: str | None = None) -> str:
    """Return calculated basic_part_number for this item.
    Calculates as item_code + "-" + supplier_part_no from Item Supplier.
    Prefer exact supplier when provided; else fall back to the first row.
    """
    if not item_code:
        return ""

    params = {"item_code": item_code}
    supplier_filter = ""
    order_clause = "si.idx"
    
    if supplier:
        params["supplier"] = supplier
        supplier_filter = "AND si.supplier = %(supplier)s"
        order_clause = """
            CASE WHEN si.supplier = %(supplier)s THEN 0 ELSE 1 END,
            si.idx
        """

    rows = frappe.db.sql(
        f"""
        SELECT si.supplier_part_no
        FROM `tabItem Supplier` si
        WHERE si.parent = %(item_code)s
        {supplier_filter}
        ORDER BY {order_clause}
        LIMIT 1
        """,
        params,
    )
    
    # If no rows found or supplier_part_no is empty/None, return item_code
    if not rows:
        return item_code
    
    supplier_part_no = (rows[0][0] or "").strip()
    
    # Calculate basic_part_number: item_code + "-" + supplier_part_no
    if supplier_part_no:
        return f"{item_code}-{supplier_part_no}"
    else:
        return item_code

def populate_mdb_part_no(doc, method=None):
    """On Stock Entry validate: generate MDB part no (format: base_part_no-quality)."""
    items = getattr(doc, "items", []) or []

    for d in items:
        base = d.custom_srv_number or ""#here need to change
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
#getting purchase
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
#updated make stock entry let's check
#updated during the benguluru visit
@frappe.whitelist()
def make_stock_entry_with_srv(source_name, target_doc=None, args=None):
    """
    Custom mapping: Purchase Receipt → Stock Entry
    - Maps project, PO details, and warehouses properly
    - Ensures correct item-level warehouse mappings
    - Handles missing custom fields gracefully
    """

    def set_missing_values(source, target):
        # Safely copy parent-level custom fields
        target.custom_enter_po_no = source.get("custom_enter_po_no") or ""
        target.custom_select_po_date = source.get("custom_select_po_date") or ""
        target.stock_entry_type = "Stock Entry"
        target.purpose = "Material Transfer"
        target.set_missing_values()
 

        # Handle project field with both naming conventions
        target.custom_select_project = (
            source.get("custom_project_save")
            or source.get("custom_select_project")
            or ""
        )

        # Default stock entry type
        if not target.stock_entry_type:
            target.stock_entry_type = "Stock Entry"

        target.set_missing_values()

        # Automatically set warehouse values for items
        if target.stock_entry_type in ("Material Issue", "Material Transfer", "Material Receipt"):
            for d in target.items:
                # From warehouse
                if target.stock_entry_type in ("Material Issue", "Material Transfer") and target.from_warehouse:
                    d.s_warehouse = target.from_warehouse

                # To warehouse
                if target.stock_entry_type in ("Material Receipt", "Material Transfer") and target.to_warehouse:
                    d.t_warehouse = target.to_warehouse

    #  get_mapped_doc for PR → SE mapping
    doclist = get_mapped_doc(
        "Purchase Receipt",
        source_name,
        {
            "Purchase Receipt": {
                "doctype": "Stock Entry",
                "field_map": {
                    # map PO info and project
                    "custom_enter_po_no": "custom_enter_po_no",
                    "custom_select_po_date": "custom_select_po_date",
                    "custom_project_save": "custom_select_project",
                    "custom_select_project": "custom_select_project",  # fallback
                    "supplier": "supplier",
                },
            },
            "Purchase Receipt Item": {
                "doctype": "Stock Entry Detail",
                "field_map": {
                    #  Correct field mappings
                    "item_code": "item_code",
                    "item_name": "item_name",
                    "description": "description",
                    "uom": "uom",
                    "stock_uom": "stock_uom",
                    "batch_no": "batch_no",
                    "warehouse": "custom_source_stock",
                    "qty": "qty",
                    "rate": "basic_rate",
                    "amount": "amount",
                    # Links for traceability
                    "parent": "purchase_receipt",
                    "name": "pr_detail",
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
                    "item_group":"item_group",
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
    Custom override of make_purchase_receipt to fetch supplier from PO and set in PR.
    """
    def update_item(source_doc, target_doc, source_parent):
        # Ensure requested quantity is passed
        target_doc.custom_requested_quantity = source_doc.qty

        # Fetch and set supplier part number based on the item_code and supplier
        if getattr(source_parent, "supplier", None):
            # Fetch supplier part number
            supplier_part_number = frappe.db.get_value("Item Supplier", 
                {"parent": source_doc.item_code, "supplier": source_parent.supplier}, "supplier_part_no")
            if supplier_part_number:
                target_doc.custom_srv_part_number = supplier_part_number
            else:
                target_doc.custom_srv_part_number = ""  # Clear if not found

    # Create Purchase Receipt from PO
    doclist = get_mapped_doc(
        "Purchase Order",
        source_name,
        {
            "Purchase Order": {
                "doctype": "Purchase Receipt",
                "field_map": {
                    "supplier": "supplier",  # Map supplier from PO to PR
                    "transaction_date": "posting_date",
                },
            },
            "Purchase Order Item": {
                "doctype": "Purchase Receipt Item",
                "field_map": {
                    "item_code": "item_code",
                    "item_group":"item_group",
                    "qty": "qty",
                    "rate": "rate",
                    "amount": "amount",
                },
                "postprocess": update_item,  # Apply updates after mapping
            },
        },
        target_doc,
    )

    # After the mapping, fetch the supplier from PO and set it to the PR
    target_doc = custom_fetch_supplier_for_pr(source_name, target_doc)

    return doclist

#nov4
#show list basic mdb against that item in stock entry
#get the list of basic mdb for that item
CHILD_TABLE = "basic_mdb_child_table"
CHILD_FIELD = "enter_basic_mdb"
ITEM_FIELD = "custom_srv_number"  # <-- the preferred field name

@frappe.whitelist()
def get_basic_mdb_options(item_code: str = None, item_code_or_group: str = None):
    """
    Return Basic MDB (SRV) values for:
      • Item child table (basic_mdb_child_table.enter_basic_mdb)
      • Fallback to Item.custom_srv_number if exists
      • Fallback to Item Group child table
      • Fallback to Item Group’s own basic field
    Always returns a list of strings.
    """

    key = (item_code_or_group or item_code or "").strip()
    if not key:
        return []

    # Case 1: If Item exists
    if frappe.db.exists("Item", key):
        # --- 1a. From child table ---
        rows = frappe.get_all(
            CHILD_TABLE,
            filters={"parent": key, "parenttype": "Item"},
            fields=[CHILD_FIELD],
            order_by="idx",
        )
        values = [r.get(CHILD_FIELD) for r in rows if r.get(CHILD_FIELD)]
        if values:
            return values

        # --- 1b. From Item.custom_srv_number (safe check) ---
        if frappe.db.has_column("Item", ITEM_FIELD):
            single_val = frappe.db.get_value("Item", key, ITEM_FIELD)
            if single_val:
                return [single_val]

        # --- 1c. From linked Item Group ---
        item_group = frappe.db.get_value("Item", key, "item_group")
        if item_group:
            return _get_mdb_from_item_group(item_group)

        return []

    # Case 2: Item Group directly
    if frappe.db.exists("Item Group", key):
        return _get_mdb_from_item_group(key)

    return []


def _get_mdb_from_item_group(item_group: str):
    """
    Fallback: Fetch MDB values from Item Group’s child table.
    """
    rows = frappe.get_all(
        CHILD_TABLE,
        filters={"parent": item_group, "parenttype": "Item Group"},
        fields=[CHILD_FIELD],
        order_by="idx",
    )
    values = [r.get(CHILD_FIELD) for r in rows if r.get(CHILD_FIELD)]
    return values

#list of ware of that warehouses
@frappe.whitelist()
def get_child_warehouses(parent: str):
    if not parent:
        return []

    parent_name = (
        frappe.db.get_value("Warehouse", parent, "name")
        or frappe.db.get_value("Warehouse", {"warehouse_name": parent}, "name")
    )
    if not parent_name:
        return []

    rows = frappe.db.sql("""
        SELECT name, warehouse_name, is_group
        FROM `tabWarehouse`
        WHERE parent_warehouse = %(parent)s
        ORDER BY warehouse_name
    """, {"parent": parent_name}, as_dict=True)

    return [
        {
            "name": r["name"],
            "label": r["warehouse_name"],
            "is_group": r["is_group"]
        }
        for r in rows
    ]

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
import frappe, json

# ===========================================================
#  PROJECT → SUBSYSTEM
# ===========================================================
import frappe, json

# Helper to normalize filters
def _parse_filters(filters):
    if isinstance(filters, str):
        try:
            return json.loads(filters)
        except Exception:
            return {}
    return filters or {}

# ===========================================================
#  PRJ_CARDS helper: fetch Add Project Card names
# ===========================================================
@frappe.whitelist()
def get_add_project_card_names():
    """Return card_name values from Add Project Card Table for PRJ_CARDS UI."""
    rows = frappe.get_all(
        "Add Project Card Table",
        fields=["card_name"],
        filters={"card_name": ["!=", ""]},
        distinct=True,
        order_by="card_name",
    )
    return rows


@frappe.whitelist()
def get_card_names_for_pack(pack_name: str | None = None):
    """Return card_name values linked to the supplied PRJ_PACK (pack_name)."""
    if not pack_name:
        return []

    rows = frappe.db.sql(
        """
        SELECT DISTINCT child.card_name
        FROM `tabAdd Project Card Table` child
        INNER JOIN `tabAdd Project Card` parent
            ON child.parent = parent.name
           AND child.parenttype = 'Add Project Card'
        WHERE parent.pack_name = %(pack_name)s
        ORDER BY child.card_name
        """,
        {"pack_name": pack_name},
        as_dict=True,
    )

    return [r.get("card_name") for r in rows if r.get("card_name")]


@frappe.whitelist()
def get_project_ref_names():
    """
    Return distinct Project Reference values to populate PRJ_CARDS.project_ref_name.

    Uses Add Project Card.select_project_copy (project name string) and, if needed,
    Add Project Card.project_ref_name as a fallback.
    Always returns a simple list of strings.
    """
    # From select_project_copy (preferred)
    rows_copy = frappe.db.sql(
        """
        SELECT DISTINCT TRIM(select_project_copy) AS ref
        FROM `tabAdd Project Card`
        WHERE IFNULL(select_project_copy, '') != ''
        """,
        as_dict=True,
    )

    # From project_ref_name (optional fallback / legacy)
    rows_ref = frappe.db.sql(
        """
        SELECT DISTINCT TRIM(project_ref_name) AS ref
        FROM `tabAdd Project Card`
        WHERE IFNULL(project_ref_name, '') != ''
        """,
        as_dict=True,
    )

    refs = {r.ref for r in rows_copy if r.get("ref")}
    refs.update({r.ref for r in rows_ref if r.get("ref")})

    return sorted(refs)


@frappe.whitelist()
def get_ecad_card_names_by_project_ref(project_ref_name: str | None = None):
    """
    Return ECAD card_name values for PRJ_CARDS.ecad_card_name filtered by Project REF.

    A card is included if its parent Add Project Card:
      - has select_project_copy = project_ref_name  OR
      - has project_ref_name = project_ref_name
    """
    if not project_ref_name:
        return []

    rows = frappe.db.sql(
        """
        SELECT DISTINCT child.card_name
        FROM `tabAdd Project Card Table` child
        INNER JOIN `tabAdd Project Card` parent
            ON child.parent = parent.name
           AND child.parenttype = 'Add Project Card'
        WHERE child.card_name IS NOT NULL
          AND TRIM(child.card_name) != ''
          AND (
                TRIM(parent.select_project_copy) = %(ref)s
             OR TRIM(parent.project_ref_name) = %(ref)s
          )
        ORDER BY child.card_name
        """,
        {"ref": project_ref_name},
        as_dict=True,
    )

    return [r.get("card_name") for r in rows if r.get("card_name")]


@frappe.whitelist()
def get_ecad_card_names_for_project(project: str | None = None):
    """Return card_name values for the given project from Add Project Card Table."""
    if not project:
        return []

    rows = frappe.db.sql(
        """
        SELECT DISTINCT child.card_name
        FROM `tabAdd Project Card Table` child
        INNER JOIN `tabAdd Project Card` parent
            ON child.parent = parent.name
           AND child.parenttype = 'Add Project Card'
        WHERE parent.select_project = %(project)s
        ORDER BY child.card_name
        """,
        {"project": project},
        as_dict=True,
    )

    return [r.get("card_name") for r in rows if r.get("card_name")]


@frappe.whitelist()
def get_approved_cards_by_type(card_type: str | None = None):
    """Return card names whose Add Project Card type matches and designer workflow is Approve."""
    if not card_type:
        return []

    rows = frappe.db.sql(
        """
        SELECT DISTINCT designer.card_name
        FROM `tabCardwise Component List Update and Approve - Designer` designer
        INNER JOIN `tabAdd Project Card Table` child
            ON child.card_name = designer.card_name
        INNER JOIN `tabAdd Project Card` parent
            ON child.parent = parent.name
           AND child.parenttype = 'Add Project Card'
        WHERE parent.card_type = %(card_type)s
          AND designer.workflow_status = 'Approve'
        ORDER BY designer.card_name
        """,
        {"card_type": card_type},
        as_dict=True,
    )

    return [r.get("card_name") for r in rows if r.get("card_name")]


@frappe.whitelist()
def get_card_names_for_material_request(pack_name: str | None = None):
    """Return card names for Material Request's custom_card based on selected package."""
    if not pack_name:
        return []

    rows = frappe.db.sql(
        """
        SELECT DISTINCT card_name
        FROM `tabCardwise Component List Update and Approve - Designer`
        WHERE pack_name = %(pack_name)s
          AND workflow_status = 'Approve'
        ORDER BY card_name
        """,
        {"pack_name": pack_name},
        as_dict=True,
    )

    return [r.get("card_name") for r in rows if r.get("card_name")]

# ===========================================================
#  PROJECT → SUBSYSTEM
# ===========================================================
@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_subsystems_for_project(doctype, txt, searchfield, start, page_len, filters):
    f = _parse_filters(filters)
    project_val = f.get("select_project")
    if not project_val:
        return []

    # accept either DocName or proj_code (int)
    if frappe.db.exists("PROJECT_MASTER", project_val):
        proj_code = frappe.db.get_value("PROJECT_MASTER", project_val, "proj_code")
    else:
        proj_code = project_val  # assume already integer

    rows = frappe.db.sql("""
        SELECT name, sub_system
        FROM `tabPRJ_SUB`
        WHERE proj_code = %(proj_code)s
        ORDER BY sub_code
    """, {"proj_code": int(proj_code)}, as_dict=True)

    return [[r["name"], r["sub_system"]] for r in rows]


# ===========================================================
#  SUBSYSTEM → PACKAGE
# ===========================================================
@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_packages_for_subsystem(doctype, txt, searchfield, start, page_len, filters):
    f = _parse_filters(filters)
    subsystem_val = f.get("select_sub_system")
    if not subsystem_val:
        return []

    # accept either DocName or sub_code (int)
    if frappe.db.exists("PRJ_SUB", subsystem_val):
        sub_code = frappe.db.get_value("PRJ_SUB", subsystem_val, "sub_code")
    else:
        sub_code = subsystem_val

    rows = frappe.db.sql("""
        SELECT name, pack_name
        FROM `tabPROJECT_PACKAGE`
        WHERE sub_code = %(sub_code)s
        ORDER BY pack_name
    """, {"sub_code": int(sub_code)}, as_dict=True)

    return [[r["name"], r["pack_name"]] for r in rows]


# ===========================================================
#  PACKAGE → CARD
# ===========================================================
@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_cards_for_package(doctype, txt, searchfield, start, page_len, filters):
    f = _parse_filters(filters)
    package_val = f.get("select_pack_name")
    if not package_val:
        return []

    # accept either DocName or pack_name (int)
    if frappe.db.exists("PROJECT_PACKAGE", package_val):
        pack_name = frappe.db.get_value("PROJECT_PACKAGE", package_val, "pack_name")
    else:
        pack_name = package_val

    rows = frappe.db.sql("""
        SELECT name, ecad_card_name
        FROM `tabPRJ_CARDS`
        WHERE pack_name = %(pack_name)s
        ORDER BY card_code
    """, {"pack_name": int(pack_name)}, as_dict=True)

    return [[r["name"], r["ecad_card_name"]] for r in rows]
#FOR THE PROJECT card MANIPULATION
@frappe.whitelist()
def get_items_for_group(item_group):
    """Return all items that belong to a given Item Group (with custom_pstylesave)."""
    if not item_group:
        return []

    items = frappe.db.get_all(
        "Item",
        filters={"item_group": item_group},
        fields=["name", "item_name", "description", "custom_pstylesave"],
        order_by="item_name"
    )
    return items
#mapping cardwise project to bom
#not used
'''
@frappe.whitelist()
def get_components_for_bom(cardwise_component_list):#
    # Fetch the items from the child table (Component List Item) linked to the parent (Cardwise Component List)
    components = frappe.get_all('Component List Item', 
                                filters={'parent': cardwise_component_list}, 
                                fields=['link_part as item_code', 'qty'])

    return components
'''
#mapping cardwise project to bom

@frappe.whitelist()

def get_components_for_bom(cardwise_component_list):

    components = frappe.get_all(

        "On Box Component Item",

        filters={

            "parent": cardwise_component_list

        },

        fields=[

            "link_part_number as item_code"

        ]

    )
 
    for row in components:

        # Qty always 1

        row["qty"] = 1
 
        # Fetch stock UOM from Item

        row["uom"] = frappe.db.get_value(

            "Item",

            row["item_code"],

            "stock_uom"

        )
 
        # Fetch last rate (PO → PR → SE)

        row["rate"] = get_last_item_rate(row["item_code"]) or 0
 
    return components

def get_last_item_rate(item_code):

    # 1️⃣ Purchase Order

    rate = frappe.db.sql("""

        SELECT rate

        FROM `tabPurchase Order Item`

        WHERE item_code = %s

        ORDER BY creation DESC

        LIMIT 1

    """, item_code)
 
    if rate:

        return rate[0][0]
 
    # 2️⃣ Purchase Receipt

    rate = frappe.db.sql("""

        SELECT rate

        FROM `tabPurchase Receipt Item`

        WHERE item_code = %s

        ORDER BY creation DESC

        LIMIT 1

    """, item_code)
 
    if rate:

        return rate[0][0]
 
    # 3️⃣ Stock Entry

    rate = frappe.db.sql("""

        SELECT basic_rate

        FROM `tabStock Entry Detail`

        WHERE item_code = %s

        ORDER BY creation DESC

        LIMIT 1

    """, item_code)
 
    if rate:

        return rate[0][0]
 
    return 0

 

 
@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_items_by_group_name(doctype, txt, searchfield, start, page_len, filters):
    """
    Return Items belonging to a given Item Group.
    Works whether custom_item_group_save stores Item Group Name or ID.
    """
    import json

    if isinstance(filters, str):
        try:
            filters = json.loads(filters)
        except Exception:
            filters = {}

    group_name = (filters or {}).get("custom_item_group_save")
    if not group_name:
        return []

    like = f"%{txt or ''}%"

    return frappe.db.sql(
        """
        SELECT i.name, i.item_name
        FROM `tabItem` i
        WHERE i.item_group = %(group_name)s
          AND COALESCE(i.disabled, 0) = 0
          AND (i.name LIKE %(like)s OR i.item_name LIKE %(like)s)
        ORDER BY i.item_name
        LIMIT %(start)s, %(page_len)s
        """,
        {
            "group_name": group_name,
            "like": like,
            "start": start,
            "page_len": page_len,
        },
        as_dict=True,
    )
# po inavalidaton script added on oct 31
# file: ursc_cms_app/api.py
import frappe, json
#bypassing the user permissions
@frappe.whitelist()
def get_po_items(po_name):
    """Return PO items for a given Purchase Order (bypasses permission)."""
    return frappe.get_all(
        "Purchase Order Item",
        filters={"parent": po_name},
        fields=["name", "item_code", "item_group","item_name", "custom_requested_qty", "qty", "custom_po_flag"],
        ignore_permissions=True
    )

'''
@frappe.whitelist()
def invalidate_po_items(parent_pos=None, item_names=None):
    """
    Invalidate selected Purchase Orders or PO Items.
    Sets custom_po_flag = 0 for selected rows and/or documents.
    Works even for submitted (docstatus=1) POs.
    """

    updated_items, updated_pos = [], []

    # --- normalize inputs ---
    if isinstance(parent_pos, str):
        try:
            parent_pos = json.loads(parent_pos)
        except Exception:
            parent_pos = [p.strip() for p in parent_pos.split(",") if p.strip()]

    if isinstance(item_names, str):
        try:
            item_names = json.loads(item_names)
        except Exception:
            item_names = [i.strip() for i in item_names.split(",") if i.strip()]

    # --- invalidate specific PO items ---
    if item_names:
        for item_name in item_names:
            if not item_name:
                continue
            frappe.db.set_value(
                "Purchase Order Item",
                item_name,
                "custom_po_flag",
                0,
                update_modified=False
            )
            updated_items.append(item_name)

    # --- invalidate entire POs ---
    if parent_pos:
        for po_name in parent_pos:
            po_name = po_name.strip()
            if not po_name:
                continue

            try:
                po = frappe.get_doc("Purchase Order", po_name)
            except frappe.DoesNotExistError:
                continue

            if po.docstatus != 1:
                continue

            frappe.db.sql("""
                UPDATE `tabPurchase Order Item`
                SET custom_po_flag = 0
                WHERE parent = %s
            """, (po_name,))

            frappe.db.set_value(
                "Purchase Order",
                po_name,
                "custom_po_flag",
                0,
                update_modified=False
            )
            updated_pos.append(po_name)

    frappe.db.commit()

    message = f"Invalidated {len(updated_pos)} PO(s) and {len(updated_items)} item(s)."
    frappe.logger().info({
        "event": "po_invalidation",
        "updated_pos": updated_pos,
        "updated_items": updated_items
    })

    return {
        "message": message,
        "updated_pos": updated_pos,
        "updated_items": updated_items
    }
'''
@frappe.whitelist()
def invalidate_po_items(parent_pos=None, item_names=None, action_type="invalidate"):
    """
    Invalidate or validate selected Purchase Orders or PO Items.
    - action_type = "invalidate" → set custom_po_flag = 0
    - action_type = "validate"   → set custom_po_flag = 1
    """

    updated_items, updated_pos = [], []
    new_flag_value = 0 if action_type == "invalidate" else 1

    # --- Normalize inputs ---
    if isinstance(parent_pos, str):
        try:
            parent_pos = json.loads(parent_pos)
        except Exception:
            parent_pos = [p.strip() for p in parent_pos.split(",") if p.strip()]

    if isinstance(item_names, str):
        try:
            item_names = json.loads(item_names)
        except Exception:
            item_names = [i.strip() for i in item_names.split(",") if i.strip()]

    # --- Update specific PO items ---
    if item_names:
        for item_name in item_names:
            if not item_name:
                continue
            frappe.db.set_value(
                "Purchase Order Item",
                item_name,
                "custom_po_flag",
                new_flag_value,
                update_modified=False
            )
            updated_items.append(item_name)

    # --- Update entire POs ---
    if parent_pos:
        for po_name in parent_pos:
            po_name = po_name.strip()
            if not po_name:
                continue

            try:
                po = frappe.get_doc("Purchase Order", po_name)
            except frappe.DoesNotExistError:
                continue

            if po.docstatus != 1:
                continue

            frappe.db.sql("""
                UPDATE `tabPurchase Order Item`
                SET custom_po_flag = %(flag)s
                WHERE parent = %(po)s
            """, {"po": po_name, "flag": new_flag_value})

            frappe.db.set_value(
                "Purchase Order",
                po_name,
                "custom_po_flag",
                new_flag_value,
                update_modified=False
            )
            updated_pos.append(po_name)

    frappe.db.commit()

    action_label = "Validated" if action_type == "validate" else "Invalidated"

    message = f"{action_label} {len(updated_pos)} PO(s) and {len(updated_items)} item(s)."
    frappe.logger().info({
        "event": f"po_{action_type}",
        "updated_pos": updated_pos,
        "updated_items": updated_items
    })

    return {
        "message": message,
        "updated_pos": updated_pos,
        "updated_items": updated_items
    }

#validate the po
@frappe.whitelist()
def validate_po_items(parent_pos=None, item_names=None):
    """
    Validate (reactivate) selected Purchase Orders or PO Items.
    Sets custom_po_flag = 1 for selected rows and/or documents.
    Works even for submitted (docstatus=1) POs.
    """

    updated_items, updated_pos = [], []

    # --- normalize inputs ---
    if isinstance(parent_pos, str):
        try:
            parent_pos = json.loads(parent_pos)
        except Exception:
            parent_pos = [p.strip() for p in parent_pos.split(",") if p.strip()]

    if isinstance(item_names, str):
        try:
            item_names = json.loads(item_names)
        except Exception:
            item_names = [i.strip() for i in item_names.split(",") if i.strip()]

    # --- validate (reactivate) specific PO items ---
    if item_names:
        for item_name in item_names:
            if not item_name:
                continue
            frappe.db.set_value(
                "Purchase Order Item",
                item_name,
                "custom_po_flag",
                1,  # ✅ set to active
                update_modified=False
            )
            updated_items.append(item_name)

    # --- validate entire POs ---
    if parent_pos:
        for po_name in parent_pos:
            po_name = po_name.strip()
            if not po_name:
                continue

            try:
                po = frappe.get_doc("Purchase Order", po_name)
            except frappe.DoesNotExistError:
                continue

            if po.docstatus != 1:
                continue

            # Set all items back to active
            frappe.db.sql("""
                UPDATE `tabPurchase Order Item`
                SET custom_po_flag = 1
                WHERE parent = %s
            """, (po_name,))

            # Also reactivate parent flag
            frappe.db.set_value(
                "Purchase Order",
                po_name,
                "custom_po_flag",
                1,
                update_modified=False
            )
            updated_pos.append(po_name)

    frappe.db.commit()

    message = f"Validated {len(updated_pos)} PO(s) and {len(updated_items)} item(s)."
    frappe.logger().info({
        "event": "po_validation",
        "validated_pos": updated_pos,
        "validated_items": updated_items
    })

    return {
        "message": message,
        "validated_pos": updated_pos,
        "validated_items": updated_items
    }
'''
#filter based on flag
@frappe.whitelist()
def custom_make_purchase_receipt_from_po(source_name, target_doc=None):
    """
    Custom override for ERPNext's make_purchase_receipt.
    Fetches only PO Items where custom_po_flag = 1.
    """

    def update_item(source_doc, target_doc, source_parent):
        target_doc.custom_requested_quantity = source_doc.qty

    from frappe.model.mapper import get_mapped_doc

    doc = get_mapped_doc(
        "Purchase Order",
        source_name,
        {
            "Purchase Order": {
                "doctype": "Purchase Receipt",
                "field_map": {
                    "supplier": "supplier",
                    "transaction_date": "posting_date",
                    "company": "company",
                },
            },
            "Purchase Order Item": {
                "doctype": "Purchase Receipt Item",
                "condition": lambda d: d.custom_po_flag == 1,  # filter here
                "field_map": {
                    "item_code": "item_code",
                    "item_name": "item_name",
                    "description": "description",
                    "qty": "qty",
                    "rate": "rate",
                    "amount": "amount",
                    "uom": "uom",
                    "stock_uom": "stock_uom",
                    "warehouse": "warehouse",
                    "cost_center": "cost_center",
                    "project": "project",
                },
                "postprocess": update_item,
            },
        },
        target_doc,
    )

    return doc
'''
@frappe.whitelist()
def custom_make_purchase_receipt_from_po(source_name, target_doc=None):
    """
    Custom override for ERPNext's make_purchase_receipt.
    Fetches only PO Items where custom_po_flag = 1 and copies the supplier to the parent PR.
    """
    def update_item(source_doc, target_doc, source_parent):
        # Ensure that the supplier from PO is copied over to the PR
        target_doc.supplier = source_parent.supplier  # Copy supplier from PO to PR
        target_doc.custom_requested_quantity = source_doc.qty  # Map quantity
        if getattr(source_parent, "custom_enter_srv_part_number", None):
            target_doc.custom_srv_part_number = source_parent.custom_enter_srv_part_number  # Map custom part number

    doc = get_mapped_doc(
        "Purchase Order",  # Source document
        source_name,  # PO document name
        {
"Purchase Order": {
    "doctype": "Purchase Receipt",
    "field_map": {
        "supplier": "supplier",
        "transaction_date": "posting_date",
        "company": "company",
    },
},
"Purchase Order Item": {
    "doctype": "Purchase Receipt Item",
    "condition": lambda d: d.custom_po_flag == 1,
    "field_map": {
        "item_code": "item_code",
        "item_name": "item_name",
        "description": "description",
        "qty": "qty",
        "rate": "rate",
        "amount": "amount",
        "item_group":"item_group",
        "uom": "uom",
        "stock_uom": "stock_uom",
        "warehouse": "warehouse",
        "cost_center": "cost_center",
        "project": "project",
        "parent": "purchase_order",  # <-- add this
    },
    "postprocess": update_item,
},
        },
        target_doc,
    )

    return doc

#filter by flags
@frappe.whitelist()
def get_po_items_for_pr(po_name):
    """
    Return only Purchase Order Items with custom_po_flag = 1
    for the 'Get Items from PO' button in Purchase Receipt.
    """
    if not po_name:
        return []
 
    return frappe.get_all(
        "Purchase Order Item",
        filters={"parent": po_name, "custom_po_flag": 1},
        fields=["name", "item_code","item_group", "item_name", "description", "qty", "rate", "amount", "uom", "stock_uom", "warehouse"],
        order_by="idx",
        ignore_permissions=True
    )
#get ponumber
@frappe.whitelist()

def get_po_custom_number(po_name):

    """

    Fetch Purchase Order custom_po_number only

    """

    if not po_name:

        return None
 
    return frappe.db.get_value(

        "Purchase Order",

        po_name,

        "custom_po_number"

    )

 
 
'''
@frappe.whitelist()
def custom_make_purchase_receipt(source_name, target_doc=None):
    """
    Custom override of make_purchase_receipt:
    - Load only PO Items where custom_po_flag = 1
    - Remove blank initial PR rows
    """

    def update_item(source_doc, target_doc, source_parent):
        target_doc.custom_requested_quantity = source_doc.qty
        if getattr(source_parent, "custom_enter_srv_part_number", None):
            target_doc.custom_srv_part_number = source_parent.custom_enter_srv_part_number

    # Map only active items
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
                    "item_group":"item_group",
                    "amount": "amount",
                },
                "postprocess": update_item,
                "condition": lambda doc: doc.custom_po_flag == 1,  # 👈 filter only accepted ones
            },
        },
        target_doc,
    )

    # Remove any blank first row created by default
    if hasattr(doc, "items"):
        doc.items = [d for d in doc.items if d.item_code]

    return doc
'''
@frappe.whitelist()
def custom_make_purchase_receipt(source_name, target_doc=None):
    """
    Custom override of make_purchase_receipt:
    - Load only PO Items where custom_po_flag = 1
    - Map custom_select_projet → custom_project_save
    """

    def update_item(source_doc, target_doc, source_parent):
        target_doc.custom_requested_quantity = source_doc.qty
        if getattr(source_parent, "custom_enter_srv_part_number", None):
            target_doc.custom_srv_part_number = source_parent.custom_enter_srv_part_number

    # Map only active items
    doc = get_mapped_doc(
        "Purchase Order",
        source_name,
        {
            "Purchase Order": {
                "doctype": "Purchase Receipt",
                "field_map": {
                    "supplier": "supplier",
                    "transaction_date": "posting_date",
                    # ✅ add this line:
                    "custom_select_projet": "custom_project_save",
                },
            },
            "Purchase Order Item": {
                "doctype": "Purchase Receipt Item",
                "field_map": {
                    "item_code": "item_code",
                    "qty": "qty",
                    "rate": "rate",
                    "item_group":"item_group",
                    "amount": "amount",
                },
                "postprocess": update_item,
                "condition": lambda doc: doc.custom_po_flag == 1,
            },
        },
        target_doc,
    )

    # Remove any blank first row created by default
    if hasattr(doc, "items"):
        doc.items = [d for d in doc.items if d.item_code]

    return doc

#fetch request qty form po to ordered qty to pr
@frappe.whitelist()
def custom_pr_from_po(source_name, target_doc=None):
    """
    Custom mapping: Purchase Order → Purchase Receipt
    - Maps custom_requested_qty → custom_ordered_quantity
    - Fetches only PO items with custom_po_flag = 1
    """

    def update_item(source_doc, target_doc, source_parent):
        # map requested → ordered qty
        target_doc.custom_ordered_quantity = (
            source_doc.custom_requested_qty or source_doc.qty or 0
        )

    # ✅ Only include active (custom_po_flag = 1) items
    po_items = frappe.db.get_all(
        "Purchase Order Item",
        filters={"parent": source_name, "custom_po_flag": 1},
        pluck="name",
    )

    if not po_items:
        frappe.msgprint("No active PO items (custom_po_flag = 1) found.")
        return None

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
                    "item_group":"item_group",
                    "item_code": "item_code",
                    "qty": "qty",
                    "rate": "rate",
                    "amount": "amount",
                },
                "postprocess": update_item,
                # ✅ Map only items from list above
                "condition": lambda doc: doc.name in po_items,
            },
        },
        target_doc,
    )

    return doc
#synchornization child and parent fields
def sync_po_item_flags(doc, method=None):
    """
    Whenever a PO is saved:
    - If parent custom_po_flag = 0, mark all children as 0.
    - If all child rows = 0, mark parent = 0.
    """
    if not doc.get("items"):
        return

    # Case 1: If PO itself marked invalid, cascade to all items
    if doc.custom_po_flag == 0:
        frappe.db.sql("""
            UPDATE `tabPurchase Order Item`
            SET custom_po_flag = 0
            WHERE parent = %s
        """, doc.name)
        return

    # Case 2: If all items are invalid, mark PO as invalid
    active_count = frappe.db.count(
        "Purchase Order Item",
        filters={"parent": doc.name, "custom_po_flag": 1}
    )
    if active_count == 0 and doc.custom_po_flag == 1:
        frappe.db.set_value("Purchase Order", doc.name, "custom_po_flag", 0)
# date code week validate
def validate_custom_date_code(doc, method=None):
    """Ensure Stock Entry Detail.custom_date_code is 4 digits and week ≤ 52."""
    frappe.logger().debug(f"[validate_custom_date_code] Running for Stock Entry {doc.name}")

    for d in (doc.items or []):
        if not d.custom_date_code:
            continue

        code = str(d.custom_date_code).strip()

        # Must be exactly four digits
        if not code.isdigit() or len(code) != 4:
            frappe.throw(f"Row #{d.idx}: Date Code must be a 4-digit number (e.g., 2452).")

        # Split into YY + WW
        year_part = int(code[:2])
        week_part = int(code[2:])

        if week_part < 1 or week_part > 52:
            frappe.throw(
                f"Row #{d.idx}: Invalid Date Code '{code}'. "
                f"Week number ({week_part}) must be between 01 and 52."
            )

@frappe.whitelist(allow_guest=True)
def fetch_supplier_part_number(item_code, supplier):
    # Fetch the supplier part number from Item Supplier table
    result = frappe.db.get_value("Item Supplier", {"parent": item_code, "supplier": supplier}, "supplier_part_no")
    if result:
        return result
    else:
        return _("No supplier part number found for this item with the selected supplier.")
@frappe.whitelist()
def fetch_supplier_from_po(purchase_order):
    """
    Fetch the supplier from the Purchase Order and return it.
    """
    if not purchase_order:
        return None

    # Fetch the supplier from the Purchase Order
    po = frappe.get_doc("Purchase Order", purchase_order)
    
    # Return the supplier
    return po.supplier
@frappe.whitelist()
def custom_fetch_supplier_for_pr(purchase_order, target_doc=None):
    """
    Custom function to fetch supplier from PO and map it to the PR.
    """
    # Fetch supplier from the Purchase Order
    supplier = fetch_supplier_from_po(purchase_order)
    
    if supplier:
        # Set the supplier in the parent PR (Purchase Receipt)
        target_doc.supplier = supplier
        frappe.db.commit()  # Commit the changes to DB
    
    return target_doc
@frappe.whitelist()
def custom_make_purchase_receipt(source_name, target_doc=None):
    """
    Custom override of make_purchase_receipt:
    - Fetch the supplier from the Purchase Order and map it to the Purchase Receipt.
    - Fetch only PO Items where custom_po_flag = 1.
    """

    def update_item(source_doc, target_doc, source_parent):
        # Map quantity and supplier part number to PR Item
        target_doc.custom_requested_quantity = source_doc.qty
        if getattr(source_parent, "supplier", None):
            # Fetch supplier part number from Item Supplier and map it to the PR Item
            supplier_part_number = frappe.db.get_value("Item Supplier", 
                {"parent": source_doc.item_code, "supplier": source_parent.supplier}, "supplier_part_no")
            if supplier_part_number:
                target_doc.custom_srv_part_number = supplier_part_number
            else:
                target_doc.custom_srv_part_number = ""  # Clear if no part number found

    # Fetch Purchase Order document
    po_doc = frappe.get_doc("Purchase Order", source_name)

    if po_doc.supplier:
        # Set the supplier from PO to the PR parent (target_doc)
        target_doc.supplier = po_doc.supplier

    # Create Purchase Receipt from PO
    doclist = get_mapped_doc(
        "Purchase Order",  # Source document (PO)
        source_name,  # PO document name
        {
            "Purchase Order": {
                "doctype": "Purchase Receipt",  # Target document (PR)
                "field_map": {
                    "supplier": "supplier",  # Map supplier from PO to PR
                    "transaction_date": "posting_date",  # Map posting date
                },
            },
            "Purchase Order Item": {
                "doctype": "Purchase Receipt Item",  # Item child table
                "field_map": {
                    "item_code": "item_code",
                    "qty": "qty",
                    "rate": "rate",
                    "amount": "amount",
                    "item_group":"item_group"
                },
                "postprocess": update_item,  # Apply updates after mapping
                "condition": lambda doc: doc.custom_po_flag == 1,  # Filter to only include valid items
            },
        },
        target_doc,
    )

    return doclist

@frappe.whitelist(allow_guest=True)
def fetch_supplier_part_number(item_code, supplier):
    """
    Fetch the supplier part number from Item Supplier table.
    """
    # Ensure both item_code and supplier are provided
    if not item_code or not supplier:
        return _("No item code or supplier provided.")
    
    result = frappe.db.get_value(
        "Item Supplier", 
        {"parent": item_code, "supplier": supplier}, 
        "supplier_part_no"
    )
    
    if result:
        return result
    else:
        return _("No supplier part number found for this item with the selected supplier.")
#fetch stock entry data
@frappe.whitelist()
def copy_stock_entry_with_all_fields(source_name, target_doc=None):
    """
    Copy entire Stock Entry with ALL fields (standard + custom) and ALL items.
    This ensures the standard Copy button works correctly with all data.
    """
    if not source_name:
        frappe.throw("Source Stock Entry is required")
    
    # Get source document
    source_doc = frappe.get_doc("Stock Entry", source_name)
    
    # Create new document
    if target_doc:
        target_doc = frappe.get_doc("Stock Entry", target_doc)
    else:
        target_doc = frappe.new_doc("Stock Entry")
    
    # Copy ALL parent-level fields
    # Standard fields
    target_doc.stock_entry_type = source_doc.stock_entry_type
    target_doc.purpose = source_doc.purpose
    target_doc.posting_date = source_doc.posting_date
    target_doc.posting_time = source_doc.posting_time
    target_doc.set_posting_time = source_doc.set_posting_time
    target_doc.company = source_doc.company
    target_doc.from_warehouse = source_doc.from_warehouse
    target_doc.to_warehouse = source_doc.to_warehouse
    target_doc.supplier = source_doc.supplier
    target_doc.supplier_name = source_doc.supplier_name
    target_doc.supplier_address = source_doc.supplier_address
    target_doc.address_display = source_doc.address_display
    target_doc.project = source_doc.project
    target_doc.remarks = source_doc.remarks
    
    # Copy ALL custom fields dynamically
    for field in source_doc.meta.fields:
        if field.fieldname.startswith("custom_"):
            if hasattr(source_doc, field.fieldname):
                value = getattr(source_doc, field.fieldname)
                if value is not None:
                    setattr(target_doc, field.fieldname, value)
    
    # Copy ALL child items with ALL their fields
    target_doc.items = []
    for source_item in source_doc.items:
        new_item = frappe.new_doc("Stock Entry Detail")
        
        # Copy standard item fields
        new_item.item_code = source_item.item_code
        new_item.item_name = source_item.item_name
        new_item.description = source_item.description
        new_item.uom = source_item.uom
        new_item.stock_uom = source_item.stock_uom
        new_item.qty = source_item.qty
        new_item.basic_rate = source_item.basic_rate
        new_item.amount = source_item.amount
        new_item.valuation_rate = source_item.valuation_rate
        new_item.s_warehouse = source_item.s_warehouse
        new_item.t_warehouse = source_item.t_warehouse
        new_item.batch_no = source_item.batch_no
        new_item.serial_no = source_item.serial_no
        new_item.expense_account = source_item.expense_account
        new_item.cost_center = source_item.cost_center
        new_item.project = source_item.project
        new_item.purchase_receipt = source_item.purchase_receipt
        new_item.pr_detail = source_item.pr_detail
        new_item.purchase_order = source_item.purchase_order
        new_item.po_detail = source_item.po_detail
        
        # Copy ALL custom item fields dynamically
        for field in source_item.meta.fields:
            if field.fieldname.startswith("custom_"):
                if hasattr(source_item, field.fieldname):
                    value = getattr(source_item, field.fieldname)
                    if value is not None:
                        setattr(new_item, field.fieldname, value)
        
        target_doc.append("items", new_item)
    
    # Set missing values
    target_doc.set_missing_values()
    
    return target_doc
@frappe.whitelist()
def fetch_stock_entry_payload(source_name: str) -> dict:
    """
    Return a payload to populate the CURRENT new Stock Entry with data from an existing one.
    - Copies only fields that exist in your doctypes to avoid AttributeError
    - Includes all custom fields (custom_*) that exist
    - Returns {"parent": {...}, "items": [{...}, ...]}
    """
    if not source_name:
        frappe.throw("Source Stock Entry is required")

    source = frappe.get_doc("Stock Entry", source_name)
    parent_meta = frappe.get_meta("Stock Entry")
    item_meta = frappe.get_meta("Stock Entry Detail")

    # System/internal fields to skip
    PARENT_SKIP = {
        "name", "owner", "creation", "modified", "modified_by", "docstatus",
        "parent", "parenttype", "parentfield", "idx", "amended_from"
    }
    ITEM_SKIP = PARENT_SKIP.copy()

    # Build allowed fieldname sets from meta (exists check)
    parent_allowed = {df.fieldname for df in parent_meta.fields if df.fieldname} - PARENT_SKIP
    item_allowed = {df.fieldname for df in item_meta.fields if df.fieldname} - ITEM_SKIP

    # Parent payload
    parent_payload = {}
    for fname in parent_allowed:
        # include all normal fields and custom_* that actually exist
        if hasattr(source, fname):
            parent_payload[fname] = source.get(fname)

    # Ensure manufacturing-required fields are present for Manufacture flows
    se_type = source.get("stock_entry_type")
    if se_type in ("Manufacture", "Material Transfer for Manufacture"):
        # Add known required fields if they exist on your doctype
        for mf in ("bom_no", "manufacturing_quantity", "fg_completed_qty"):
            if frappe.db.has_column("Stock Entry", mf):
                parent_payload[mf] = source.get(mf)

    # Items payload
    items_payload = []
    for s in (source.items or []):
        row = {}

        # Always copy essentials (including custom_srv_number and custom_mdb_part_no)
        essential_fields = [
            "item_code", "item_name", "description", "uom", "stock_uom", "qty",
            "s_warehouse", "t_warehouse", "batch_no", "serial_no", "basic_rate",
            "amount", "valuation_rate", "expense_account", "cost_center", "project",
            "custom_mdb_part_no", "custom_srv_number", "custom_quality_save",  # Updated: custom_srv_number instead of custom_base_part_no
            "custom_exp_date", "custom_date_code", "custom_srv_part_number",
            "custom_source_parent_warehouse", "custom_target_parent_warhouse",  # Your custom warehouse fields
            "custom_warehouse_s_program", "custom_target_stock_select",
            "custom_sprogram_save", "custom_tprogram_save"
        ]
        
        for k in essential_fields:
            if hasattr(s, k):
                row[k] = s.get(k)

        # Also copy any other fields that exist in your child doctype (incl. custom_)
        for fname in item_allowed:
            if fname not in row and hasattr(s, fname):
                row[fname] = s.get(fname)

        items_payload.append(row)

    return {
        "parent": parent_payload,
        "items": items_payload,
    }
#validate po against a pr
@frappe.whitelist()
def validate_po_qty_for_prupdate_purchase_order_item_on_pr_submission(po_name):
    """Validate if any items in the PO have already been fully received."""
    
    # Fetch Purchase Order Items and their custom_requested_qty (instead of received_qty)
    po_items = frappe.get_all(
        'Purchase Order Item', 
        filters={'parent': po_name}, 
        fields=['name', 'item_code',"item_group", 'qty', 'custom_requested_qty']
    )
    
    # Loop through each PO item to check the custom_requested_qty
    for item in po_items:
        if item.qty > item.custom_requested_qty:
            # If quantity is still remaining to be received, return True
            return True
    
    # If all items in the PO are fully received, return False
    return False
''''
import frappe
import frappe

def update_po_item_on_pr_submission(self, method):
    """Update Purchase Order Item quantities based on requested quantities in Purchase Receipt."""
    
    pr_doc = self  # `self` refers to the current instance of the Purchase Receipt document

    # Loop through all items in the Purchase Receipt
    for pr_item in pr_doc.items:
        # Search for the Purchase Order Item (POI) based on the item_code from the PR
        po_items = frappe.get_all(
            "Purchase Order Item",  # Search in the Purchase Order Item doctype
            filters={"item_code": pr_item.item_code},  # Match item_code in PO Items
            fields=["name", "custom_requested_qty", "parent", "item_code"],  # Get PO item details
        )

        if not po_items:
            # If no matching Purchase Order Item is found, raise an error
            frappe.throw(f"Purchase Order Item for item '{pr_item.item_code}' not found in the Purchase Order.")
        
        # Loop through the matching PO Items to check for quantity validation
        for po_item in po_items:
            po_name = po_item.parent  # Get the Purchase Order name

            # Check if the item is part of the same Purchase Order (for the sake of validation)
            if pr_item.purchase_order == po_name:
                # Calculate the total requested quantity including this PR
                new_requested_qty = po_item.custom_requested_qty + pr_item.qty

                # Update the Purchase Order Item with the new custom_requested_qty
                frappe.db.set_value(
                    "Purchase Order Item",
                    po_item.name,
                    "custom_requested_qty",
                    new_requested_qty,
                )

                # Optional: You can also update any fields or perform further actions here
                # Example: Linking the PO Item to PR Item (if needed)
                pr_item.purchase_order_item = po_item.name
                pr_item.save()  # Save the updated Purchase Receipt Item

                # Commit the changes to the database
                frappe.db.commit()
                
                # Return success message
                frappe.msgprint(f"Successfully updated requested quantity for item '{pr_item.item_code}' in Purchase Order.")

    # Return success message if all items are updated successfully
    return {"message": "All Purchase Order Items have been updated successfully."}

#validate
@frappe.whitelist()
def validate_purchase_order_item_on_pr_submission(self, method):
    """Validate Purchase Order Item quantities against Purchase Receipt Items before saving/submitting."""

    pr_doc = self  # `self` refers to the current instance of the Purchase Receipt document

    # Loop through all items in the Purchase Receipt
    for pr_item in pr_doc.items:
        # Search for Purchase Order Item matching item_code and fetch its corresponding Purchase Order
        po_items = frappe.get_all(
            "Purchase Order Item",  # Search in the Purchase Order Item doctype
            filters={"item_code": pr_item.item_code},  # Match item_code in PO Items
            fields=["name", "qty", "parent", "item_code"],  # Get PO item details
        )

        if not po_items:
            # If no matching Purchase Order Item is found, raise an error
            frappe.throw(f"Purchase Order Item for item '{pr_item.item_code}' not found in the Purchase Order.")
        
        # Loop through the matching PO Items to check for quantity validation
        for po_item in po_items:
            po_name = po_item.parent  # Get the Purchase Order name
            po_qty = po_item.qty  # Get the quantity in the Purchase Order

            # Check if the PR item is linked to the same Purchase Order (i.e., matching parent)
            if pr_item.purchase_order == po_name:
                
                # Step 1: Validate if PR quantity exceeds PO quantity
                if pr_item.qty > po_qty:
                    frappe.throw(f"Received quantity for item '{pr_item.item_code}' exceeds the available quantity in Purchase Order {po_name}.")

                # Step 2: Check if PR Item already exists in PO, and calculate the received quantity
                received_qty = frappe.db.get_value("Purchase Receipt Item", {"purchase_order_item": po_item.name}, "sum(qty)") or 0
                
                if received_qty >= po_qty:
                    # If the entire PO quantity has been received already, prevent PR creation
                    frappe.throw(f"Purchase Order '{po_name}' has already been fully received. No further Purchase Receipts can be created for this PO.")

                # Step 3: Check if the quantity in PR exceeds the remaining quantity from PO
                remaining_qty = po_qty - received_qty
                if pr_item.qty > remaining_qty:
                    # If PR quantity exceeds the remaining available quantity, raise an error
                    frappe.throw(f"Cannot receive more than {remaining_qty} of item '{pr_item.item_code}' from Purchase Order '{po_name}'.")

                # Optional: Link PO Item to PR Item
                pr_item.purchase_order_item = po_item.name
                pr_item.save()  # Save the updated Purchase Receipt Item
                
        # No need to explicitly commit, since saving will automatically commit
        # If any issues arise during the save, they will automatically be rolled back by the system.

    # Return success message if all items are validated successfully
    return {"message": "All Purchase Order Items have been validated and linked with Purchase Receipt Items."}
'''
@frappe.whitelist()
def validate_purchase_order_item_on_pr_submission(self, method):
    """Validate Purchase Order Item quantities against Purchase Receipt Items before saving/submitting."""

    pr_doc = self  # `self` refers to the current instance of the Purchase Receipt document

    for pr_item in pr_doc.items:
        po_items = frappe.get_all(
            "Purchase Order Item",
            filters={"item_code": pr_item.item_code},
            fields=["name", "qty", "parent", "item_code","item_group"]
        )

        if not po_items:
            frappe.throw(f"Purchase Order Item for item '{pr_item.item_code}' not found in the Purchase Order.")
        
        for po_item in po_items:
            po_name = po_item.parent
            po_qty = po_item.qty

            if pr_item.purchase_order == po_name:
                # Validate if PR quantity exceeds PO quantity
                if pr_item.qty > po_qty:
                    frappe.throw(f"Received quantity for item '{pr_item.item_code}' exceeds the available quantity in Purchase Order {po_name}.")
                
                # Validate if the PO has already been fully received
                received_qty = frappe.db.get_value("Purchase Receipt Item", {"purchase_order_item": po_item.name}, "sum(qty)") or 0
                if received_qty >= po_qty:
                    frappe.throw(f"Purchase Order '{po_name}' has already been fully received. No further Purchase Receipts can be created for this PO.")

    return {"message": "Validation successful."}

@frappe.whitelist()
def update_po_item_on_pr_submission(self, method):
    """Update Purchase Order Item quantities based on requested quantities in Purchase Receipt."""
    
    pr_doc = self  # `self` refers to the current instance of the Purchase Receipt document

    for pr_item in pr_doc.items:
        po_items = frappe.get_all(
            "Purchase Order Item",
            filters={"item_code": pr_item.item_code},
            fields=["name", "custom_requested_qty", "parent", "item_code"]
        )

        if not po_items:
            frappe.throw(f"Purchase Order Item for item '{pr_item.item_code}' not found in the Purchase Order.")
        
        for po_item in po_items:
            po_name = po_item.parent

            if pr_item.purchase_order == po_name:
                # Update custom_requested_qty
                new_requested_qty = po_item.custom_requested_qty + pr_item.qty
                frappe.db.set_value(
                    "Purchase Order Item",
                    po_item.name,
                    "custom_requested_qty",
                    new_requested_qty,
                )

                # Link the PO Item to the PR Item
                pr_item.purchase_order_item = po_item.name
                pr_item.save()

    return {"message": "Purchase Order Items updated successfully."}

@frappe.whitelist()
def get_srv_numbers_by_item_group(item_group=None):
    item_group = (item_group or "").strip()
    if not item_group:
        return []
 
    item_codes = frappe.db.get_all(
        "Item",
        filters={"item_group": item_group},
        pluck="name"
    )
    if not item_codes:
        return []
 
    rows = frappe.db.sql(
        """
        SELECT DISTINCT custom_srv_number
        FROM `tabStock Entry Detail`
        WHERE item_code IN %(items)s
          AND IFNULL(custom_srv_number, '') != ''
        ORDER BY custom_srv_number
        """,
        {"items": item_codes},
        as_dict=True,
    )
 
    return [r.custom_srv_number for r in rows]




@frappe.whitelist()
def get_package_styles_by_item_group(item_group=None):
    """
    One Component Type → Many Package Styles (DISTINCT)
 
    Uses ONLY:
    - custom_pstylesave (Data)
 
    custom_package_style is completely ignored.
    """
 
    item_group = (item_group or "").strip()
    if not item_group:
        return []
 
    rows = frappe.db.sql(
        """
        SELECT DISTINCT TRIM(custom_pstylesave) AS pkg
        FROM `tabItem`
        WHERE item_group = %(group)s
          AND custom_pstylesave IS NOT NULL
          AND TRIM(custom_pstylesave) != ''
        ORDER BY pkg
        """,
        {"group": item_group},
        as_dict=True,
    )
 
    return [r.pkg for r in rows]

@frappe.whitelist()
def get_stock_entry_meta_by_srv(srv_number=None):
    """
    Fetch DISTINCT Date Code and Quality values
    from Stock Entry Detail based on selected SRV Number
    """
 
    srv_number = (srv_number or "").strip()
    if not srv_number:
        return {
            "date_codes": [],
            "qualities": []
        }
 
    frappe.logger().info({
        "event": "fetch_stock_entry_meta",
        "srv_number": srv_number
    })
 
    rows = frappe.db.sql(
        """
        SELECT DISTINCT
            sed.custom_date_code,
            COALESCE(NULLIF(sed.custom_quality_save,''), sed.custom_quality) AS quality
        FROM `tabStock Entry Detail` sed
        WHERE sed.custom_srv_number = %(srv)s
        """,
        {"srv": srv_number},
        as_dict=True
    )
 
    date_codes = sorted({
        r.custom_date_code for r in rows if r.custom_date_code
    })
 
    qualities = sorted({
        r.quality for r in rows if r.quality
    })
 
    frappe.logger().info({
        "event": "stock_entry_meta_result",
        "date_codes": date_codes,
        "qualities": qualities
    })
 
    return {
        "date_codes": date_codes,
        "qualities": qualities
    }
@frappe.whitelist()
def get_package_styles_by_item_group(item_group=None):
    """
    One Component Type → Many Package Styles (DISTINCT)
 
    Uses ONLY:
    - custom_pstylesave (Data)
 
    custom_package_style is completely ignored.
    """
 
    item_group = (item_group or "").strip()
    if not item_group:
        return []
 
    rows = frappe.db.sql(
        """
        SELECT DISTINCT TRIM(custom_pstylesave) AS pkg
        FROM `tabItem`
        WHERE item_group = %(group)s
          AND custom_pstylesave IS NOT NULL
          AND TRIM(custom_pstylesave) != ''
        ORDER BY pkg
        """,
        {"group": item_group},
        as_dict=True,
    )
 
    return [r.pkg for r in rows]
@frappe.whitelist()
def get_manufacturers_by_item_group(item_group=None):
    """
    One Component Type (Item Group) → Many Manufacturers (DISTINCT)
 
    Pulls manufacturers from:
    Item → Item Manufacturer
    """
 
    item_group = (item_group or "").strip()
    if not item_group:
        return []
 
    rows = frappe.db.sql(
        """
        SELECT DISTINCT im.manufacturer
        FROM `tabItem` i
        INNER JOIN `tabItem Manufacturer` im
            ON im.item_code = i.name
        WHERE i.item_group = %(group)s
          AND im.manufacturer IS NOT NULL
          AND TRIM(im.manufacturer) != ''
        ORDER BY im.manufacturer
        """,
        {"group": item_group},
        as_dict=True
    )
 
    return [r.manufacturer for r in rows]
@frappe.whitelist()
def set_requested_meta(doc, method=None):
    # Set requester only once
    if not doc.requested_by:
        doc.requested_by = frappe.session.user
 
    # Set requested date only once
    if not doc.requested_date:
        doc.requested_date = frappe.utils.now_datetime()
@frappe.whitelist()
def get_rejected_dpa_list():
    return frappe.get_all(
        "DPA Request",
        filters={
            "dpa_status_flag": ["in", ["0", "2"]]
        },
        fields=["name"],
        order_by="modified desc"
    )
 

#for dpa accept api
# ============================================================
# 1. GRID DATA: PENDING / REJECTED DPA REQUESTS
# ============================================================
 
@frappe.whitelist()
def get_pending_dpa_grid():
    """
    Returns flat rows:
    Req No | Req Date | Part No | Date Code | Manufacturer | DPA Stage | Status
    Where parent.dpa_status_flag IN ('0','2')
    """
 
    rows = frappe.db.sql(
        """
        SELECT
            dpa.name AS dpa_name,
            dpa.requested_date,
            dpa.dpa_status_flag,
            dpa.dpa_stage,
            comp.basic_part_no,
            comp.date_code,
            comp.manufacturer
        FROM `tabDPA Request` dpa
        INNER JOIN `tabDPA Component Detail` comp
            ON comp.parent = dpa.name
        WHERE dpa.dpa_status_flag IN ('0')
        ORDER BY dpa.creation DESC, comp.idx
        """,
        as_dict=True,
    )
    return rows
 
  
#for dpa accept api
# ============================================================
# 1. GRID DATA: PENDING / REJECTED DPA REQUESTS
# ============================================================
 
@frappe.whitelist()
def get_pending_dpa_grid():
    """
    Returns flat rows:
    Req No | Req Date | Part No | Date Code | Manufacturer | DPA Stage | Status
    Where parent.dpa_status_flag IN ('0','2')
    """
 
    rows = frappe.db.sql(
        """
        SELECT
            dpa.name AS dpa_name,
            dpa.requested_date,
            dpa.dpa_status_flag,
            dpa.dpa_stage,
            comp.basic_part_no,
            comp.date_code,
            comp.manufacturer
        FROM `tabDPA Request` dpa
        INNER JOIN `tabDPA Component Detail` comp
            ON comp.parent = dpa.name
        WHERE dpa.dpa_status_flag IN ('0')
        ORDER BY dpa.creation DESC, comp.idx
        """,
        as_dict=True,
    )
    return rows
 
 
# ============================================================
# 2. FULL PREVIEW (PARENT + CHILDREN)
# ============================================================
 
@frappe.whitelist()
def get_dpa_full_preview(dpa_name):
    """
    Returns full DPA header + all components for preview.
    Some UI logic (quality/spec 'Others') is handled in JS.
    """
    doc = frappe.get_doc("DPA Request", dpa_name)
 
    parent = {
        "name": doc.name,
        "requested_by": getattr(doc, "requested_by", None),
        "requested_date": getattr(doc, "requested_date", None),
        "dpa_stage": getattr(doc, "dpa_stage", None),
        "status": getattr(doc, "dpa_status_flag", None),
        "remarks": getattr(doc, "reject_remarks", None),
    }
 
    children = [row.as_dict() for row in doc.get("components_detail", [])]
 
    return {
        "parent": parent,
        "children": children,
    }
 
 
# ============================================================
# 3. APPROVE
# ============================================================
  
@frappe.whitelist()
def approve_dpa(dpa_name):
    """
    Approve DPA:
    - parent.dpa_status_flag = 1
    - approved_on = now
    - approved_by = current user
    - children.dpa_status_flag = 1
    """
    if not dpa_name:
        frappe.throw("DPA Name is required")
 
    doc = frappe.get_doc("DPA Request", dpa_name)
 
    now = frappe.utils.now_datetime()
    user = frappe.session.user
 
    # Update parent
    doc.db_set({
        "dpa_status_flag": 1,
        "approved_on": now,
        "approved_by": user
    })
 
    # Update children
    frappe.db.sql(
        """
        UPDATE `tabDPA Component Detail`
        SET dpa_status_flag = 1
        WHERE parent = %s
        """,
        (dpa_name,),
    )
 
    frappe.db.commit()
 
    return {
        "status": "success",
        "message": f"{dpa_name} approved",
        "approved_on": now,
        "approved_by": user
    }
 
 
# ============================================================
# 4. REJECT
# ============================================================
@frappe.whitelist()
def reject_dpa(dpa_name, remarks):
    """
    Reject DPA:
    - parent.dpa_status_flag = 2
    - rejected_on = now
    - rejected_by = current user
    - reject_remarks saved
    - children.dpa_status_flag = 2
    """
    if not dpa_name:
        frappe.throw("DPA Name is required")
 
    if not remarks:
        frappe.throw("Rejection remarks are required")
 
    doc = frappe.get_doc("DPA Request", dpa_name)
 
    now = frappe.utils.now_datetime()
    user = frappe.session.user
 
    # Update parent
    doc.db_set({
        "dpa_status_flag": 2,
        "reject_remarks": remarks,
        "rejected_on": now,
        "rejected_by": user
    })
 
    # Update children
    frappe.db.sql(
        """
        UPDATE `tabDPA Component Detail`
        SET dpa_status_flag = 2
        WHERE parent = %s
        """,
        (dpa_name,),
    )
 
    frappe.db.commit()
 
    return {
        "status": "success",
        "message": f"{dpa_name} rejected",
        "rejected_on": now,
        "rejected_by": user
    }
#dpa auto increment the key
@frappe.whitelist()
def get_next_dpa_req_no():
    """
    Returns next DPA Request Number.
 
    Rules:
    - Ignore NULL / 0 values
    - If no records exist → start from 1
    - Preserve migrated numbers
    """
 
    result = frappe.db.sql(
        """
        SELECT MAX(CAST(dpa_req_no AS UNSIGNED))
        FROM `tabDPA Request`
        WHERE dpa_req_no IS NOT NULL
          AND dpa_req_no != 0
        """,
        as_list=True
    )
 
    max_no = result[0][0] if result and result[0][0] else 0
 
    return int(max_no) + 1 

#fa auto increments
@frappe.whitelist()
def get_next_fa_req_no():
    """
    Returns next Failure Request Number.
 
    Rules:
    - Ignore NULL / 0 values
    - If no records exist → start from 1
    - Preserve migrated numbers
    """
 
    result = frappe.db.sql(
        """
        SELECT MAX(CAST(fa_req_no AS UNSIGNED))
        FROM `tabFailure Request`
        WHERE fa_req_no IS NOT NULL
          AND fa_req_no != 0
        """,
        as_list=True
    )
 
    max_no = result[0][0] if result and result[0][0] else 0
 
    return int(max_no) + 1 

import frappe

#raidation shield data auto increment
 
@frappe.whitelist()

def get_next_rad_shield_id():

    """

    Returns next Radiation Shield ID.
 
    Rules:

    - Ignore NULL / 0 values

    - If no records exist → start from 1

    - Preserve migrated Oracle IDs

    """
 
    result = frappe.db.sql(

        """

        SELECT MAX(CAST(rad_shield_id AS UNSIGNED))

        FROM `tabRadiation Shield Data`

        WHERE rad_shield_id IS NOT NULL

          AND rad_shield_id != 0

        """,

        as_list=True

    )
 
    max_no = result[0][0] if result and result[0][0] else 0

    return int(max_no) + 1
#radiation request auto increment
@frappe.whitelist()

def get_next_rad_req_no():

    """

    Returns next Radiation Request Number.
 
    Rules:

    - Ignore NULL / 0 values

    - If no records exist → start from 1

    - Preserve migrated Oracle numbers

    """
 
    result = frappe.db.sql(

        """

        SELECT MAX(CAST(rad_req_no AS UNSIGNED))

        FROM `tabRadiation Request`

        WHERE rad_req_no IS NOT NULL

          AND rad_req_no != 0

        """,

        as_list=True

    )
 
    max_no = result[0][0] if result and result[0][0] else 0

    return int(max_no) + 1

 
 
@frappe.whitelist()
def get_next_proj_code():
    """
    Returns next Project Code.

    Rules:
    - Ignore NULL / 0 values
    - If no records exist → start from 1
    - Preserve migrated numbers
    """

    result = frappe.db.sql(
        """
        SELECT MAX(CAST(proj_code AS UNSIGNED))
        FROM `tabProject`
        WHERE proj_code IS NOT NULL
          AND proj_code != 0
        """,
        as_list=True
    )

    max_no = result[0][0] if result and result[0][0] else 0
    return int(max_no) + 1



@frappe.whitelist()
def get_next_sub_code():
    """
    Returns next Sub Code for PRJ_SUB.

    Rules:
    - Ignore NULL / 0 values
    - If no records exist → start from 1
    - Preserve migrated values
    """

    result = frappe.db.sql(
        """
        SELECT MAX(CAST(sub_code AS UNSIGNED))
        FROM `tabPRJ_SUB`
        WHERE sub_code IS NOT NULL
          AND sub_code != 0
        """,
        as_list=True
    )

    max_no = result[0][0] if result and result[0][0] else 0
    return int(max_no) + 1




@frappe.whitelist()
def get_next_pack_code():
    """
    Returns next Package Code.

    Rules:
    - Ignore NULL / 0 values
    - If no records exist → start from 1
    - Preserve migrated numbers
    """

    result = frappe.db.sql(
        """
        SELECT MAX(CAST(pack_code AS UNSIGNED))
        FROM `tabPROJECT_PACKAGE`
        WHERE pack_code IS NOT NULL
          AND pack_code != 0
        """,
        as_list=True
    )

    max_no = result[0][0] if result and result[0][0] else 0
    return int(max_no) + 1



@frappe.whitelist()
def get_next_card_code():
    """
    Returns next Card Code for PRJ_CARDS
    """

    result = frappe.db.sql(
        """
        SELECT MAX(CAST(card_code AS UNSIGNED))
        FROM `tabPRJ_CARDS`
        WHERE card_code IS NOT NULL
          AND card_code != 0
        """,
        as_list=True
    )

    max_no = result[0][0] if result and result[0][0] else 0
    return int(max_no) + 1

 
#dpa request view 
import frappe
 
@frappe.whitelist()

def get_dpa_request_view_data(

    search_by=None,

    dpa_stage=None,

    requested_by=None,

    from_date=None,

    to_date=None,

    dpa_req_no=None,

    page=1,

    page_size=50

):

    page = int(page or 1)

    page_size = int(page_size or 50)

    offset = (page - 1) * page_size
 
    conditions = []

    values = {}
 
    # ------------------ Dynamic filters ------------------

    if search_by == "DPA STAGE" and dpa_stage:

        conditions.append("dpa.dpa_stage = %(dpa_stage)s")

        values["dpa_stage"] = dpa_stage
 
    if search_by == "USER" and requested_by:

        conditions.append("dpa.requested_by = %(requested_by)s")

        values["requested_by"] = requested_by
 
    if search_by == "REQUEST DATE" and from_date and to_date:

        conditions.append(

            "DATE(dpa.dpa_req_date) BETWEEN %(from_date)s AND %(to_date)s"

        )

        values["from_date"] = from_date

        values["to_date"] = to_date
 
    if search_by == "DPA REQUEST NUMBER" and dpa_req_no:

        conditions.append("dpa.dpa_req_no = %(dpa_req_no)s")

        values["dpa_req_no"] = dpa_req_no
 
    where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
 
    # ------------------ Count ------------------

    total_count = frappe.db.sql(

        f"""

        SELECT COUNT(DISTINCT dpa.name)

        FROM `tabDPA Request` dpa

        LEFT JOIN `tabDPA Component Detail` comp

            ON comp.parent = dpa.name

        {where_clause}

        """,

        values

    )[0][0]
 
    # ------------------ Data ------------------

    rows = frappe.db.sql(

        f"""

        SELECT

            dpa.name,

            dpa.dpa_req_no,

            dpa.dpa_req_date,

            dpa.requested_by,

            dpa.dpa_stage,

            dpa.dpa_status_flag,
 
            comp.comp_type,

            comp.basic_part_no,

            comp.dpa_dc,

            comp.manufacturer,

            comp.quality
 
        FROM `tabDPA Request` dpa

        LEFT JOIN `tabDPA Component Detail` comp

            ON comp.parent = dpa.name
 
        {where_clause}
 
        ORDER BY dpa.dpa_req_date DESC, comp.idx

        LIMIT %(limit)s OFFSET %(offset)s

        """,

        {**values, "limit": page_size, "offset": offset},

        as_dict=True

    )
 
    return {

        "rows": rows,

        "total_count": int(total_count or 0),

        "page": page,

        "page_size": page_size
    }
#  parent level flags are updating only not worked for child rows
import frappe

from frappe.utils import now
 
def handle_dpa_workflow(doc, method):

    """

    Handles workflow transitions for DPA Request

    - Updates parent + child dpa_status_flag

    - Captures approved/rejected user and time

    """
 
    # Avoid Draft

    if doc.workflow_state == "Draft":

        return
 
    current_user = frappe.session.user

    current_time = now()
 
    # =========================

    # APPROVED

    # =========================

    if doc.workflow_state == "Approved":

        doc.db_set("dpa_status_flag", "1", update_modified=False)

        doc.db_set("approved_by", current_user, update_modified=False)

        doc.db_set("approved_on", current_time, update_modified=False)
 
        # ✅ UPDATE ALL CHILD ROWS

        for row in doc.components_detail:

            row.db_set("dpa_status_flag", "1", update_modified=False)
 
    # =========================

    # REJECTED

    # =========================

    elif doc.workflow_state == "Rejected":

        doc.db_set("dpa_status_flag", "2", update_modified=False)

        doc.db_set("rejected_by", current_user, update_modified=False)

        doc.db_set("rejected_on", current_time, update_modified=False)
 
        # ✅ UPDATE ALL CHILD ROWS

        for row in doc.components_detail:

            row.db_set("dpa_status_flag", "2", update_modified=False)
 
    # =========================

    # RESET TO PENDING

    # =========================

    elif doc.workflow_state == "Pending":

        doc.db_set("dpa_status_flag", "0", update_modified=False)

        doc.db_set("approved_by", None, update_modified=False)

        doc.db_set("approved_on", None, update_modified=False)

        doc.db_set("rejected_by", None, update_modified=False)

        doc.db_set("rejected_on", None, update_modified=False)
 
        for row in doc.components_detail:

            row.db_set("dpa_status_flag", "0", update_modified=False)

@frappe.whitelist()

def get_po_parent_fields(po_name):

    if not po_name:

        return {}
 
    po = frappe.get_doc(

        "Purchase Order",

        po_name,

        ignore_permissions=True

    )
 
    return {

        "custom_po_number": po.custom_po_number,

        "transaction_date": po.transaction_date,

        "custom_project_save": po.custom_project_save

    }

 # File: your_app/your_module/api.py

@frappe.whitelist()
def get_stock_entry_details(component_type, mdb_part_no=None):
    """
    Returns Stock Entry Detail rows filtered by component_type and optional mdb_part_no.
    """
    filters = {"custom_select_component_type": component_type}
    if mdb_part_no:
        filters["custom_mdb_part_no"] = mdb_part_no

    return frappe.get_all(
        "Stock Entry Detail",
        filters=filters,
        fields=["custom_mdb_part_no", "custom_date_code"],
        limit_page_length=1000
    )

#Old date code stock trasfer metohd
@frappe.whitelist()

def transfer_expired_stock(target_warehouse, items,old_dc_no=None):

    import json

    from frappe.utils import today
 
    if isinstance(items, str):

        items = json.loads(items)
 
    if not target_warehouse:

        frappe.throw("Target Warehouse is required")
 
    if not items:

        frappe.throw("No items selected for transfer")
 
    grouped = {}

    for row in items:

        grouped.setdefault(row["warehouse"], []).append(row)
 
    for source_wh, rows in grouped.items():

        se = frappe.new_doc("Stock Entry")

        se.stock_entry_type = "Material Transfer"

        se.company = frappe.defaults.get_global_default("company")
 
        # ✅ YOUR CUSTOM STATUS

        se.custom_stock_entry_status = "Old Date Code Stock Transfer"

        #se.custom_old_dc_no = frappe.flags.current_old_dc_no
        se.custom_old_dc_no = old_dc_no   # traceability

 
        item_group = frappe.db.get_value("Item", row["item_code"], "item_group")
 
        if not item_group:frappe.throw(f"Item Group not found for Item {row['item_code']}")

 
        for row in rows:

            if row["warehouse"] == target_warehouse:

                continue
            se.append("items", {
    "custom_target_store_": target_warehouse,

    "custom_target_program": target_warehouse,

    "custom_target_stock": target_warehouse,
 

    "item_code": row["item_code"],

    "qty": row["qty"],

    "s_warehouse": row["warehouse"],

    "t_warehouse": target_warehouse,

    "custom_date_code": row["custom_date_code"],

    "custom_exp_date": row.get("expiry_date") or today(),

    "custom_select_component_type": item_group,  # ✅ correct source

    "custom_quality": "Expired"
    })

 
 
            '''se.append("items", {

                "item_code": row["item_code"],
                "custom_select_component_type": row["item_group"],

                "qty": row["qty"],

                "s_warehouse": row["warehouse"],

                "t_warehouse": target_warehouse,

                "custom_date_code": row["custom_date_code"],
 
                # ✅ mandatory custom fields

                "custom_quality": "Expired",

                "custom_exp_date": row.get("expiry_date") or today()

            })'''
 
        if se.items:

            se.insert(ignore_permissions=True)

            se.submit()
 
    return "Expired stock successfully transferred"
#Old date code stock trasfer read method
@frappe.whitelist()

def get_expired_components(item_group):

    import datetime

    from frappe.utils import add_to_date, getdate
 
    # 1️⃣ Fetch validity rule

    validity_name = frappe.db.get_value(

        "Component Type Datecode Validity Master",

        {"item_group": item_group, "is_active": 1},

        "name"

    )
 
    if not validity_name:

        return []
 
    validity = frappe.get_doc(

        "Component Type Datecode Validity Master",

        validity_name

    )
 
    # 2️⃣ Scan stock excluding rejected warehouses

    rows = frappe.db.sql("""

SELECT
                         
sed.item_group,
    sed.item_code,

    i.item_name,

    sed.custom_date_code,

    sle.warehouse,

    SUM(sle.actual_qty) AS qty

FROM `tabStock Entry Detail` sed

JOIN `tabStock Entry` se

    ON se.name = sed.parent

    AND se.docstatus = 1

JOIN `tabStock Ledger Entry` sle

    ON sle.voucher_no = se.name

    AND sle.voucher_detail_no = sed.name

JOIN `tabItem` i

    ON i.name = sed.item_code

JOIN `tabWarehouse` w

    ON w.name = sle.warehouse

WHERE

    i.item_group = %s

    AND sed.custom_date_code IS NOT NULL

    AND IFNULL(w.is_rejected_warehouse, 0) = 0

GROUP BY

    sed.item_code,

    sed.custom_date_code,

    sle.warehouse

HAVING

    SUM(sle.actual_qty) > 0

 

    """, item_group, as_dict=True)
 
    today = getdate()

    expired = []
 
    # 3️⃣ Expiry calculation

    for row in rows:

        date_code = row.custom_date_code
 
        year = int("20" + date_code[:2])

        week = int(date_code[2:])

        mfg_date = datetime.date.fromisocalendar(year, week, 1)
 
        expiry_date = add_to_date(

            mfg_date,

            years=validity.validity_years,

            months=validity.validity_months

        )
 
        if expiry_date < today:

            row.update({

                "mfg_date": mfg_date,

                "expiry_date": expiry_date

            })

            expired.append(row)
 
    return expired

 #getting purchase receipts work same like po screen
@frappe.whitelist()

def make_pr_from_po_like_standard(po_name):

    """

    ERPNext v15 compatible

    EXACT same behavior as:

    Purchase Order → Create → Purchase Receipt

    """
    po = frappe.get_doc("Purchase Order", po_name)
 
    if po.custom_extra_pr_used:

        frappe.throw(

            f"""

           This Purchase Order is Already Created Extra QTY Once.<br><br>

            No Purchase Receipt can be created Aganist this PO.

            """,

            title="Purchase Order Extra QTY Used"

        )
 
    if not po_name:

        frappe.throw("Purchase Order is required")
 
    from erpnext.buying.doctype.purchase_order.purchase_order import make_purchase_receipt
 
    pr = make_purchase_receipt(po_name)
 
    # Your custom parent linkage

    pr.custom_select_project = po_name
 
    return pr

@frappe.whitelist()

def get_item_locations(doctype, txt, searchfield, start, page_len, filters):

    warehouse = filters.get("warehouse")
 
    if not warehouse:

        return []
 
    return frappe.db.sql("""

        SELECT DISTINCT wlm.enter_location

        FROM `tabWarehouse Location Master` wlm

        INNER JOIN `tabWarehouse Location Stock Grade` wls

            ON wls.parent = wlm.name

        WHERE wls.select_warehouse = %s

          AND wlm.enter_location LIKE %s

        ORDER BY wlm.modified DESC

        LIMIT %s OFFSET %s

    """, (

        warehouse,

        f"%{txt}%",

        page_len,

        start

    ))

  
@frappe.whitelist()

def get_default_item_location(item_code=None, warehouse=None):

    if not warehouse:

        return None
 
    row = frappe.db.sql("""

        SELECT wlm.enter_location

        FROM `tabWarehouse Location Master` wlm

        INNER JOIN `tabWarehouse Location Stock Grade` wls

            ON wls.parent = wlm.name

        WHERE wls.select_warehouse = %s

        ORDER BY wlm.modified DESC

        LIMIT 1

    """, (warehouse,), as_dict=True)
 
    return row[0]["enter_location"] if row else None

 
import frappe

from frappe import _
 
@frappe.whitelist()

def fetch_link_part_numbers_by_package(package_name: str):

    """

    Fetch link_part_number values based on selected package.
 
    Flow:

    selected package

        → Cardwise Component List Update and Approve - Designer.pack_name

        → Cardwise.name

        → On Box Component Item.parent

        → link_part_number

    """
 
    if not package_name:

        frappe.throw(_("package_name is required"))
 
    rows = frappe.db.sql(

        """

        SELECT DISTINCT

            c.link_part_number

        FROM `tabCardwise Component List Update and Approve - Designer` p

        JOIN `tabOn Box Component Item` c

          ON c.parent = p.name

         AND c.parenttype = 'Cardwise Component List Update and Approve - Designer'

         AND c.parentfield = 'table_yvva'

        WHERE p.pack_name = %(package_name)s

          AND p.docstatus = 1

          AND c.link_part_number IS NOT NULL

        ORDER BY c.link_part_number

        """,

        {"package_name": package_name},

        as_dict=True

    )
 
    return {

        "status": "ok",

        "package_name": package_name,

        "count": len(rows),

        "data": rows

    }

 #filter component type to package style ,so based on selected package style-comptype linkage,whenever adding link part number,added filteration jan13-2026
@frappe.whitelist()

def pstyle_query(doctype, txt, searchfield, start, page_len, filters):

    """

    Link field query for PSTYLE.

    Filters PSTYLE by Item Group.
 
    Mapping:

    PSTYLE.select_component = Item Group.name

    """
 
    item_group = None

    if isinstance(filters, dict):

        item_group = filters.get("item_group")
 
    if not item_group:

        return []
 
    start = int(start or 0)

    page_len = int(page_len or 20)
 
    return frappe.db.sql(

        """

        SELECT

            p.name,

            p.package_style_name

        FROM `tabPSTYLE` p

        WHERE p.select_component = %(item_group)s

          AND (

                p.package_style_name LIKE %(txt)s

                OR p.name LIKE %(txt)s

              )

        ORDER BY p.package_style_name

        LIMIT %(start)s, %(page_len)s

        """,

        {

            "item_group": item_group,

            "txt": f"%{txt}%" if txt else "%",

            "start": start,

            "page_len": page_len

        }

    )

 #filter item-group to quality 
 
@frappe.whitelist()

def quality_isro_query(doctype, txt, searchfield, start, page_len, filters):

    """

    Link query for QUALITY_ISRO.

    Filters only by component type (Item Group name).

    """
 
    component_type = filters.get("component_type") if filters else None

    if not component_type:

        return []
 
    # Pagination safety

    start = int(start or 0)

    page_len = int(page_len or 20)
 
    # Search text

    txt = f"%{txt}%" if txt else "%"
 
    return frappe.db.sql(

        """

        SELECT

            q.name,

            q.qual_name

        FROM `tabQUALITY_ISRO` q

        WHERE q.select_component = %(component_type)s

          AND (

                q.qual_name LIKE %(txt)s

                OR q.qual_code LIKE %(txt)s

                OR q.name LIKE %(txt)s

              )

        ORDER BY q.qual_name

        LIMIT %(start)s, %(page_len)s

        """,

        {

            "component_type": component_type,

            "txt": txt,

            "start": start,

            "page_len": page_len

        }

    )
#stock entry  comptype to  item-code filteration
'''import frappe
 
@frappe.whitelist()

def item_query_by_component_type(doctype, txt, searchfield, start, page_len, filters):

    """

    Link query for Item (item_code).

    Filters Items by component type (Item Group).

    """
 
    component_type = filters.get("component_type") if filters else None

    if not component_type:

        return []
 
    start = int(start or 0)

    page_len = int(page_len or 20)

    txt = f"%{txt}%" if txt else "%"
 
    return frappe.db.sql(

        """

        SELECT

            i.name,

            i.item_name AS label

        FROM `tabItem` i

        WHERE i.item_group = %(component_type)s

          AND i.disabled = 0

          AND (

                i.name LIKE %(txt)s

                OR i.item_name LIKE %(txt)s

              )

        ORDER BY i.item_name

        LIMIT %(start)s, %(page_len)s

        """,

        {

            "component_type": component_type,

            "txt": txt,

            "start": start,

            "page_len": page_len

        }

    )'''

 # ursc_cms_app/api.py

@frappe.whitelist()
def get_items_by_group_name(doctype, txt, searchfield, start, page_len, filters=None):
    filters = frappe._dict(filters or {})
    item_group = filters.get("custom_item_group_save")

    if not item_group:
        return []

    # SQL returns list of tuples -> safe for Frappe Link field
    return frappe.db.sql("""
        SELECT name, item_name
        FROM `tabItem`
        WHERE item_group = %s
        AND disabled = 0
        AND (name LIKE %s OR item_name LIKE %s)
        ORDER BY name
        LIMIT %s OFFSET %s
    """, (
        item_group,
        f"%{txt}%",
        f"%{txt}%",
        page_len,
        start
    ))



# api.py


@frappe.whitelist()
def get_mdb_for_component_type(component_type):
    """
    Return a list of unique MDB numbers for the given Component Type.
    """
    if not component_type:
        return []

    # Fetch MDBs from Stock Entry Detail linked to this component type
    mdb_list = frappe.db.get_all(
        "Stock Entry Detail",
        filters={
            "custom_select_component_type": component_type,
            "parenttype": "Stock Entry",
            "parentfield": "items"
        },
        fields=["custom_mdb_part_no"],
        limit_page_length=200
    )

    # Remove empty values and make unique
    options = list({d["custom_mdb_part_no"] for d in mdb_list if d["custom_mdb_part_no"]})

    return options
# get manufacturer name for the srv post print format
import frappe
 
@frappe.whitelist()

def get_item_manufacturers(item_codes):

    """

    Resolve manufacturer for each item_code using priority:

    1. Purchase Receipt Item

    2. Purchase Order Item

    3. Item Manufacturer (Item master)

    """
 
    if isinstance(item_codes, str):

        item_codes = frappe.parse_json(item_codes)
 
    if not item_codes:

        return {}
 
    mfr_map = {}
 
    # -------------------------------------------------

    # 1️⃣ From Purchase Receipt Item (highest priority)

    # -------------------------------------------------

    pr_items = frappe.get_all(

        "Purchase Receipt Item",

        filters={

            "item_code": ["in", item_codes]

        },

        fields=["item_code", "manufacturer"],

        order_by="modified desc"

    )
 
    for row in pr_items:

        if row.manufacturer and row.item_code not in mfr_map:

            mfr_map[row.item_code] = row.manufacturer
 
    # -------------------------------------------------

    # 2️⃣ From Purchase Order Item (fallback)

    # -------------------------------------------------

    missing_items = [i for i in item_codes if i not in mfr_map]
 
    if missing_items:

        po_items = frappe.get_all(

            "Purchase Order Item",

            filters={

                "item_code": ["in", missing_items]

            },

            fields=["item_code", "manufacturer"],

            order_by="modified desc"

        )
 
        for row in po_items:

            if row.manufacturer and row.item_code not in mfr_map:

                mfr_map[row.item_code] = row.manufacturer
 
    # -------------------------------------------------

    # 3️⃣ From Item Manufacturer (final fallback)

    # -------------------------------------------------

    still_missing = [i for i in item_codes if i not in mfr_map]
 
    if still_missing:

        item_mfrs = frappe.get_all(

            "Item Manufacturer",

            filters={

                "item_code": ["in", still_missing]

            },

            fields=["item_code", "manufacturer"]

        )
 
        for row in item_mfrs:

            if row.item_code not in mfr_map:

                mfr_map[row.item_code] = row.manufacturer
 
    # -------------------------------------------------

    # Ensure all item_codes exist in response

    # -------------------------------------------------

    for item_code in item_codes:

        mfr_map.setdefault(item_code, "")
 
    return mfr_map

  #do stock reservation
#SALES ORDER LINK FILTERATION
'''import frappe
 
@frappe.whitelist()

def get_flight_items():

    warehouses = frappe.get_all(

        "Warehouse",

        or_filters=[

            ["Warehouse", "name", "like", "%Flight G1%"],

            ["Warehouse", "name", "like", "%Flight G2%"],

            ["Warehouse", "name", "like", "%FG1%"],

            ["Warehouse", "name", "like", "%FG2%"]

        ],

        pluck="name"

    )
 
    if not warehouses:

        return []
 
    items = frappe.db.sql("""

        SELECT DISTINCT item_code

        FROM `tabBin`

        WHERE warehouse IN %(warehouses)s

          AND actual_qty > 0

    """, {

        "warehouses": tuple(warehouses)

    }, as_dict=True)
 
    return items'''
import frappe
 
@frappe.whitelist()

def get_flight_items():

    """

    Fast, cached, scalable Flight Items fetch

    Compatible with ERPNext v15 + MariaDB

    """
 
    CACHE_KEY = "flight_items_v1"

    CACHE_TTL = 300  # 5 minutes
 
    # 1Try cache first

    cached = frappe.cache().get_value(CACHE_KEY)

    if cached:

        return cached
 
    # 2️ Fast SQL using JOIN (MariaDB optimized)
    #use in case need to filter with another fg1 name

    items = frappe.db.sql("""

        SELECT DISTINCT b.item_code

        FROM `tabBin` b

        JOIN `tabWarehouse` w ON w.name = b.warehouse

        WHERE (

            w.name LIKE '%Flight G1%'

            OR w.name LIKE '%Flight G2%'

            OR w.name LIKE '%FG1%'
            OR w.name LIKE '%fg1%'
            OR w.name LIKE '%fg2%'
            OR w.name LIKE '%Flight-G1%'
            OR w.name LIKE '%Flight-G2%'
            OR w.name LIKE '%flight-g1%'         
            OR w.name LIKE '%flight-g2%'
            OR w.name LIKE '%FG2%'

        )

        AND b.actual_qty > 0

    """, as_dict=True)
 
    # 3️ Store in cache

    frappe.cache().set_value(

        CACHE_KEY,

        items,

        expires_in_sec=CACHE_TTL

    )
 
    return items

 

 #stock reserve 4 api methods
@frappe.whitelist()

# reserving stock api 1
@frappe.whitelist()

def reserve_kit_stock(docname):
 
    kit = frappe.get_doc("GENERATE REQUEST - KITTED COMPONENTS", docname)
 
    if kit.docstatus != 1:

        frappe.throw("Submit Kit Request first.")
 
    if kit.status != "Draft":

        frappe.throw(f"Kit is not eligible. Current status: {kit.status}")
 
    company = frappe.db.get_single_value("Global Defaults", "default_company")

    if not company:

        frappe.throw("Default Company not set")
 
    # --- Sales Order ---

    if kit.sales_order:

        so = frappe.get_doc("Sales Order", kit.sales_order)

        if so.docstatus == 2:

            frappe.throw("Linked Sales Order is cancelled")

    else:

        so = frappe.new_doc("Sales Order")

        so.customer = "Internal Stock Reservation"

        so.company = company

        so.delivery_date = frappe.utils.today()

        so.is_internal_customer = 1

        so.ignore_pricing_rule = 1

        so.disable_rounded_total = 1

        so.set_warehouse = kit.source_warehouse
 
        items_added = 0

        for row in kit.table_reas:

            if not row.link_part_number or not row.required_qty or row.required_qty <= 0:

                continue
 
            so.append("items", {

                "item_code": row.link_part_number,

                "qty": row.required_qty,

                "warehouse": row.stock_grade or kit.source_warehouse,

                "custom_component_type": row.component_type,

                "rate": 0,

                "price_list_rate": 0,

            })

            items_added += 1
 
        if items_added == 0:

            frappe.throw("No valid items to reserve")
 
        so.insert(ignore_permissions=True)

        so.submit()
 
        kit.db_set("sales_order", so.name)
 
    # --- Stock Reservation ---

    created = 0

    from frappe.utils import flt
 
    for so_item in so.items:
 
        bin_row = frappe.db.get_value(

            "Bin",

            {"item_code": so_item.item_code, "warehouse": so_item.warehouse},

            ["actual_qty", "reserved_qty"],

            as_dict=True

        )
 
        if not bin_row:

            frappe.throw(

                f"No Bin found for {so_item.item_code} in {so_item.warehouse}"

            )
 
        available_qty = flt(bin_row.actual_qty) - flt(bin_row.reserved_qty)
 
        if available_qty <= 0:

            frappe.throw(

                f"No available stock for {so_item.item_code} in {so_item.warehouse}"

            )
 
        reserve_qty = min(so_item.qty, available_qty)
 
        sre = frappe.new_doc("Stock Reservation Entry")

        sre.company = company

        sre.item_code = so_item.item_code

        sre.warehouse = so_item.warehouse
 
        # REQUIRED FIELDS

        sre.qty = reserve_qty

        sre.reserved_qty = reserve_qty

        sre.voucher_qty = so_item.qty

        sre.available_qty = available_qty
 
        sre.voucher_type = "Sales Order"

        sre.voucher_no = so.name

        sre.voucher_detail_no = so_item.name
 
        sre.insert(ignore_permissions=True)

        sre.submit()
 
        created += 1
 
    if created == 0:

        frappe.throw("No Stock Reservation Entries created")
 
    kit.db_set("status", "Reserved")
 
    return {

        "ok": True,

        "sales_order": so.name,

        "status": "Reserved",

        "reservations_created": created

    }
@frappe.whitelist()

@frappe.whitelist()

#kit remove
def reserve_kit_row(row_name):

    row = frappe.get_doc("Kit Request Item", row_name)

    kit = frappe.get_doc("GENERATE REQUEST - KITTED COMPONENTS", row.parent)
 
    if row.reservation_status == "Reserved":

        frappe.throw("Already reserved")
 
    # Create Sales Order Item if missing

    # Create Stock Reservation Entry ONLY for this row
 
    sre = frappe.new_doc("Stock Reservation Entry")

    sre.voucher_type = "Sales Order"

    sre.voucher_no = kit.sales_order

    sre.voucher_detail_no = row.sales_order_item

    sre.item_code = row.link_part_number

    sre.warehouse = row.stock_grade

    sre.qty = row.required_qty

    sre.reserved_qty = row.required_qty

    sre.insert()

    sre.submit()
 
    row.db_set({

        "reserved_qty": row.required_qty,

        "reservation_status": "Reserved"

    })

@frappe.whitelist()
#kit remove
def unreserve_kit_row(row_name):

    row = frappe.get_doc("Kit Request Item", row_name)
 
    reservations = frappe.get_all(

        "Stock Reservation Entry",

        filters={

            "voucher_detail_no": row.sales_order_item,

            "docstatus": 1

        },

        pluck="name"

    )
 
    for r in reservations:

        frappe.get_doc("Stock Reservation Entry", r).cancel()
 
    row.db_set({

        "reserved_qty": 0,

        "reservation_status": "Draft"

    })

@frappe.whitelist()

def unreserve_kit_stock(docname):

    kit = frappe.get_doc("GENERATE REQUEST - KITTED COMPONENTS", docname)
 
    if kit.docstatus != 1 or kit.status != "Reserved":

        frappe.throw("Kit is not in Reserved state")
 
    if not kit.sales_order:

        frappe.throw("No Sales Order linked to this Kit")
 
    reservations = frappe.get_all(

        "Stock Reservation Entry",

        filters={

            "voucher_type": "Sales Order",

            "voucher_no": kit.sales_order,

            "docstatus": 1

        },

        pluck="name"

    )
 
    if not reservations:

        frappe.throw("No active stock reservations found")
 
    for sre_name in reservations:

        frappe.get_doc("Stock Reservation Entry", sre_name).cancel()
 
    kit.db_set("status", "Draft")
 
    return {

        "ok": True,

        "status": "Draft",

        "unreserved_entries": len(reservations)

    }

import json

import frappe
 
@frappe.whitelist()

def unreserve_selected_kit_stock(reservations):

    # reservations can come as list OR JSON string

    if isinstance(reservations, str):

        reservations = json.loads(reservations)
 
    if not reservations:

        frappe.throw("No reservations received")
 
    cancelled = 0

    for sre_name in reservations:

        doc = frappe.get_doc("Stock Reservation Entry", sre_name)
 
        # only cancel submitted

        if doc.docstatus == 1:

            doc.cancel()

            cancelled += 1
 
    return {

        "ok": True,

        "cancelled": cancelled

    }

 


import frappe

from frappe.utils import cint
 
@frappe.whitelist()

def get_kit_reserved_stock(docname):

    docname = str(docname)
 
    kit = frappe.get_doc("GENERATE REQUEST - KITTED COMPONENTS", docname)
 
    # If your kit reserves through Sales Order (your reserve_kit_stock does this)

    if not kit.sales_order:

        return []
 
    # Pull active reservations created against the Sales Order

    rows = frappe.get_all(

        "Stock Reservation Entry",

        filters={

            "voucher_type": "Sales Order",

            "voucher_no": kit.sales_order,

            "docstatus": 1

        },

        fields=[

            "name as reservation",

            "item_code",

            "warehouse",

            "reserved_qty",

            "voucher_detail_no"   # ✅ exists (SO Item row name)

        ],

        order_by="modified desc"

    )
 
    # Debug log (shows in bench console / logs)

    frappe.logger().info({

        "method": "get_kit_reserved_stock",

        "kit": kit.name,

        "sales_order": kit.sales_order,

        "count": len(rows)

    })
 
    return rows

 
 

def release_kit_stock(docname):
 
    kit = frappe.get_doc("GENERATE REQUEST - KITTED COMPONENTS", docname)
 
    if kit.docstatus != 1 or kit.status != "Reserved":

        frappe.throw("Document not eligible for release")
 
    if not kit.sales_order:

        frappe.throw("No Sales Order linked")
 
    if not kit.kitting_warehouse:

        frappe.throw("Kitting Warehouse is mandatory")
 
    so = frappe.get_doc("Sales Order", kit.sales_order)
 
    # 🔁 Build lookup from Kit child table

    kit_map = {}

    for r in kit.table_reas:

        kit_map[r.link_part_number] = r
 
    se = frappe.new_doc("Stock Entry")

    se.stock_entry_type = "Material Transfer"

    se.company = so.company
 
    for so_row in so.items:
 
        if not so_row.warehouse:

            frappe.throw(f"Source warehouse missing for item {so_row.item_code}")
 
        kit_row = kit_map.get(so_row.item_code)

        if not kit_row:

            frappe.throw(f"Kit row not found for item {so_row.item_code}")
 
        se.append("items", {

            "item_code": so_row.item_code,

            "qty": so_row.qty,

            "s_warehouse": so_row.warehouse,

            "t_warehouse": kit_row.stock_grade,
         # Project name
 
 
            # ✅ YOUR CUSTOM FIELDS (Stock Entry Detail)

            "custom_date_code": "0000",

            "custom_quality": "KIT",

            "custom_exp_date": add_years(today(), 10),

            "custom_target_store_": kit_row.stock_grade,   # Warehouse name

           "custom_target_program": kit_row.stock_grade,    

            "custom_target_stock": kit_row.stock_grade,

        })
 
    se.insert(ignore_permissions=True)

    se.submit()
 
    # 🔓 Cancel SO → releases reservation

    #so.cancel()
 
    kit.db_set("status", "Released")
 
    return {

        "ok": True,

        "status": "Released",

        "stock_entry": se.name

    }
#cancel kit request
import frappe
 
@frappe.whitelist()

def cancel_kit_request_with_so(docname):

    kit = frappe.get_doc("GENERATE REQUEST - KITTED COMPONENTS", docname)
 
    if kit.docstatus != 1:

        frappe.throw("Only submitted Kit Requests can be cancelled")
 
    # Cancel Stock Reservation Entries

    if kit.sales_order:

        reservations = frappe.get_all(

            "Stock Reservation Entry",

            filters={

                "voucher_type": "Sales Order",

                "voucher_no": kit.sales_order,

                "docstatus": 1

            },

            pluck="name"

        )

        for name in reservations:

            frappe.get_doc("Stock Reservation Entry", name).cancel()
 
    # Cancel Sales Order

    if kit.sales_order:

        so = frappe.get_doc("Sales Order", kit.sales_order)

        if so.docstatus == 1:

            so.cancel()
 
    # Cancel Kit Request

    kit.cancel()
 
    return {"ok": True}

 
 
@frappe.whitelist()

def cancel_kit_reservation(docname):

    kit = frappe.get_doc("GENERATE REQUEST - KITTED COMPONENTS", docname)
 
    if kit.docstatus != 1 or kit.status != "Reserved":

        frappe.throw("Document not eligible for cancellation")
 
    reservations = frappe.get_all(

        "Stock Reservation Entry",

        filters={

            "voucher_type": kit.doctype,

            "voucher_no": kit.name,

            "docstatus": 1

        },

        pluck="name"

    )
 
    if not reservations:

        frappe.throw("No active reservations found")
 
    for name in reservations:

        frappe.get_doc("Stock Reservation Entry", name).cancel()
 
    kit.db_set("status", "Cancelled")
 
    return {

        "ok": True,

        "status": "Cancelled"

    }


 
@frappe.whitelist()

def get_last_po_cost(item_code):

    result = frappe.db.sql("""

        SELECT poi.rate

        FROM `tabPurchase Order Item` poi

        JOIN `tabPurchase Order` po

            ON po.name = poi.parent

        WHERE

            poi.item_code = %s

            AND po.docstatus = 1

        ORDER BY

            po.transaction_date DESC

        LIMIT 1

    """, item_code)
 
    return result[0][0] if result else None

#kit request get data to htmnl grid 27/01/2026
import frappe

from frappe.utils import cint
 
@frappe.whitelist()

def get_available_flight_stock(

    date_code=None,

    expiry_date=None,     # kept for backward compatibility (not used)

    exp_from=None,

    exp_to=None,

    mdb_part_no=None,

    search=None,

    page=1,

    page_size=20

):

    page = cint(page) or 1

    page_size = cint(page_size) or 20

    offset = (page - 1) * page_size
 
    values = {}
 
    # ---------------------------

    # BASE CONDITIONS

    # ---------------------------

    conditions = [

        "b.actual_qty > b.reserved_qty",

        "LOWER(w.name) REGEXP 'flight[ -]?g[12]|fg[12]'"

    ]
 
    if search:

        conditions.append("b.item_code LIKE %(search)s")

        values["search"] = f"%{search}%"
 
    if date_code:

        conditions.append("sed.custom_date_code = %(date_code)s")

        values["date_code"] = date_code
 
    if mdb_part_no:

        conditions.append("sed.custom_mdb_part_no LIKE %(mdb_part_no)s")

        values["mdb_part_no"] = f"%{mdb_part_no}%"
 
    if exp_from and exp_to:

        conditions.append("sed.custom_exp_date BETWEEN %(exp_from)s AND %(exp_to)s")

        values["exp_from"] = exp_from

        values["exp_to"] = exp_to

    elif exp_from:

        conditions.append("sed.custom_exp_date >= %(exp_from)s")

        values["exp_from"] = exp_from

    elif exp_to:

        conditions.append("sed.custom_exp_date <= %(exp_to)s")

        values["exp_to"] = exp_to
 
    where_clause = " AND ".join(conditions)
 
    # ---------------------------

    # MAIN QUERY (CORRECT MODEL)

    # ---------------------------

    query = f"""

        SELECT

            item_code,

            warehouse,

            available_qty,

            custom_date_code,

            custom_exp_date,

            custom_mdb_part_no

        FROM (

            SELECT

                b.item_code,

                b.warehouse,

                (b.actual_qty - b.reserved_qty) AS available_qty,

                sed.custom_date_code,

                sed.custom_exp_date,

                sed.custom_mdb_part_no,

                ROW_NUMBER() OVER (

                    PARTITION BY b.item_code, b.warehouse

                    ORDER BY

                        COALESCE(sed.custom_exp_date, '9999-12-31') ASC,

                        sle.posting_date DESC,

                        sle.creation DESC

                ) AS rn

            FROM `tabBin` b

            JOIN `tabWarehouse` w

                ON w.name = b.warehouse

            JOIN `tabStock Ledger Entry` sle

                ON sle.item_code = b.item_code

               AND sle.warehouse = b.warehouse

               AND sle.voucher_type = 'Stock Entry'

               AND sle.actual_qty > 0

            JOIN `tabStock Entry Detail` sed

                ON sed.name = sle.voucher_detail_no

            WHERE {where_clause}

        ) t

        WHERE rn = 1

        ORDER BY custom_exp_date ASC

        LIMIT {page_size} OFFSET {offset}

    """
 
    return frappe.db.sql(query, values, as_dict=True)

#card specific code
@frappe.whitelist()

def get_available_flight_stock_lifo(

    search=None,

    page=1,

    page_size=20

):

    page = cint(page) or 1

    page_size = cint(page_size) or 20

    offset = (page - 1) * page_size
 
    values = {}
 
    conditions = [

        "b.actual_qty > b.reserved_qty",

        "LOWER(w.name) REGEXP 'flight[ -]?g[12]|fg[12]'"

    ]
 
    if search:

        conditions.append("b.item_code LIKE %(search)s")

        values["search"] = f"%{search}%"
 
    where_clause = " AND ".join(conditions)
 
    query = f"""

        SELECT

            item_code,

            warehouse,

            available_qty,

            custom_date_code,

            custom_exp_date

        FROM (

            SELECT

                b.item_code,

                b.warehouse,

                (b.actual_qty - b.reserved_qty) AS available_qty,

                sed.custom_date_code,

                sed.custom_exp_date,
 
                ROW_NUMBER() OVER (

                    PARTITION BY b.item_code, b.warehouse

                    ORDER BY

                        -- 🔥 LIFO LOGIC (OR condition)

                        COALESCE(

                            sed.custom_exp_date,

                            STR_TO_DATE(CONCAT('20', LEFT(sed.custom_date_code, 2), '-01-01'), '%Y-%m-%d')

                        ) DESC,

                        sle.posting_date DESC,

                        sle.creation DESC

                ) AS rn
 
            FROM `tabBin` b

            JOIN `tabWarehouse` w

                ON w.name = b.warehouse

            JOIN `tabStock Ledger Entry` sle

                ON sle.item_code = b.item_code

               AND sle.warehouse = b.warehouse

               AND sle.actual_qty > 0

            JOIN `tabStock Entry Detail` sed

                ON sed.name = sle.voucher_detail_no

            WHERE {where_clause}

        ) t

        WHERE rn = 1

        ORDER BY

            COALESCE(custom_exp_date, '1900-01-01') DESC

        LIMIT {page_size} OFFSET {offset}

    """
 
    return frappe.db.sql(query, values, as_dict=True)
@frappe.whitelist()

@frappe.whitelist()

def get_project_card_component_list(project_card, search=None):

    """

    Card-wise items

    + ERPNext standard warehouse stock from Bin

    """
 
    # 1️⃣ Cardwise items

    rows = frappe.get_all(

        "On Box Component Item",

        filters={

            "parenttype": "Cardwise Component List Update and Approve - Designer",

            "parentfield": "table_yvva",

            "parent": project_card,

        },

        fields=[

            "component_type",

            "link_part_number as item_code",

        ],

        order_by="idx asc",

    )
 
    if not rows:

        return []
 
    item_codes = list({r["item_code"] for r in rows})
 
    # 2️⃣ Stock from Bin (ERPNext standard)

    bins = frappe.get_all(

        "Bin",

        filters={

            "item_code": ["in", item_codes],

            "actual_qty": [">", 0],

        },

        fields=[

            "item_code",

            "warehouse",

            "actual_qty",

            "reserved_qty",

        ],

    )
 
    # 3️⃣ Build lookup: item → list of warehouses

    stock_map = {}

    for b in bins:

        qty = (b.actual_qty or 0) - (b.reserved_qty or 0)

        if qty <= 0:

            continue
 
        stock_map.setdefault(b.item_code, []).append({

            "warehouse": b.warehouse,

            "available_qty": qty,

        })
 
    # 4️⃣ Expand rows (one row per item + warehouse)

    result = []

    for r in rows:

        stocks = stock_map.get(r["item_code"], [])
 
        if not stocks:

            result.append({

                "component_type": r["component_type"],

                "item_code": r["item_code"],

                "project_warehouse": None,

                "available_qty": 0,

            })

        else:

            for s in stocks:

                result.append({

                    "component_type": r["component_type"],

                    "item_code": r["item_code"],

                    "project_warehouse": s["warehouse"],

                    "available_qty": s["available_qty"],

                })
 
    # 5️⃣ Search

    if search:

        s = search.lower()

        result = [

            r for r in result

            if s in (r["item_code"] or "").lower()

        ]
 
    return result

 # get the card wise component list in lifo order of fg1,fg2 olny
@frappe.whitelist()

def get_project_card_flight_stock_lifo(project_card, search=None):

    """

    Cardwise Component List

    → Flight G1 / G2 warehouses only

    → Valid by expiry date OR date code

    → LIFO order

    """
 
    today = frappe.utils.today()
 
    # 1️⃣ Cardwise items

    items = frappe.get_all(

        "On Box Component Item",

        filters={

            "parenttype": "Cardwise Component List Update and Approve - Designer",

            "parentfield": "table_yvva",

            "parent": project_card,

        },

        fields=[

            "component_type",

            "link_part_number as item_code",

        ],

    )
 
    if not items:

        return []
 
    item_codes = list({i.item_code for i in items})
 
    # 2️⃣ Stock query (Flight warehouses only, LIFO)

    rows = frappe.db.sql("""

        SELECT

            i.component_type,

            sle.item_code,

            w.name AS warehouse,

            (b.actual_qty - b.reserved_qty) AS available_qty,

            sed.custom_date_code,

            sed.custom_exp_date,

            sle.posting_date,

            sle.creation

        FROM `tabStock Ledger Entry` sle

        JOIN `tabStock Entry Detail` sed

            ON sed.name = sle.voucher_detail_no

        JOIN `tabWarehouse` w

            ON w.name = sle.warehouse

        JOIN `tabBin` b

            ON b.item_code = sle.item_code

           AND b.warehouse = sle.warehouse

        JOIN (

            SELECT

                link_part_number AS item_code,

                component_type

            FROM `tabOn Box Component Item`

            WHERE parent = %(project_card)s

        ) i

            ON i.item_code = sle.item_code

        WHERE

            sle.item_code IN %(item_codes)s

            AND sle.actual_qty > 0
 
            -- ✅ Flight G1 / G2 warehouse filter

            AND (

                LOWER(w.name) LIKE '%%flight g1%%'

                OR LOWER(w.name) LIKE '%%flight g2%%'

                OR LOWER(w.name) LIKE '%%fg1%%'

                OR LOWER(w.name) LIKE '%%fg2%%'

                OR LOWER(w.name) LIKE '%%flight-g1%%'

                OR LOWER(w.name) LIKE '%%flight-g2%%'

            )
 
            -- ✅ Validity: expiry OR date code

            AND (

                sed.custom_exp_date >= %(today)s

                OR sed.custom_date_code >= DATE_FORMAT(%(today)s, '%%y%%v')

            )
 
            AND (b.actual_qty - b.reserved_qty) > 0

        ORDER BY

            sle.posting_date DESC,

            sle.creation DESC

    """, {

        "project_card": project_card,

        "item_codes": tuple(item_codes),

        "today": today,

    }, as_dict=True)
 
    # 3️⃣ Optional search

    if search:

        s = search.lower()

        rows = [r for r in rows if s in (r.item_code or "").lower()]
 
    return rows

 
 
#item group,mfr details for kit requ,working well on jan28
import frappe
 
@frappe.whitelist()

def get_item_component_meta(item_code):

    if not item_code:

        return {}
 
    # 1️⃣ Get component_type from Item

    component_type = frappe.db.get_value(

        "Item",

        item_code,

        "item_group"

    )
 
    # 2️⃣ Get manufacturers from Item Manufacturer table

    manufacturers = frappe.db.sql(

        """

        SELECT DISTINCT im.manufacturer

        FROM `tabItem Manufacturer` im

        WHERE im.item_code = %s

        ORDER BY im.is_default DESC, im.manufacturer

        """,

        (item_code,),

        as_dict=True

    )
 
    return {

        "component_type": component_type,

        "manufacturers": [m.manufacturer for m in manufacturers]

    }

@frappe.whitelist()

def get_item_stock_by_warehouse(item_code):

    if not item_code:

        return []
 
    return frappe.db.sql("""

        SELECT

            item_code,

            warehouse,

            (actual_qty - reserved_qty) AS available_qty

        FROM `tabBin`

        WHERE

            item_code = %(item_code)s

            AND (actual_qty - reserved_qty) > 0

        ORDER BY

            available_qty DESC

    """, {"item_code": item_code}, as_dict=True)

 
import frappe

from frappe.utils import cint
 
# ---- CONFIG (change only if your fieldnames differ) ----

SOURCE_PARENT_DOCTYPE = "Cardwise Component List Update and Approve - Designer"

SOURCE_CHILD_DOCTYPE = "On Box Component Item"

SOURCE_CHILD_PARENTFIELD = "table_yvva"
 
TARGET_PARENT_DOCTYPE = "GENERATE REQUEST - KITTED COMPONENTS"

TARGET_CHILD_PARENTFIELD = "table_reas"

# Child DocType for target table is inferred by DocField, no need to hardcode.
 
FIELDS_TO_COPY = ["component_type", "link_part_number"]
 
 
@frappe.whitelist()

def preview_components(project_card: str, limit: int = 50, offset: int = 0):

    """

    Read rows from source child table and return minimal fields.

    Use this for preview/pagination if there are many rows.

    """

    if not project_card:

        return {"total": 0, "rows": []}
 
    limit = cint(limit)

    offset = cint(offset)
 
    # total count

    total = frappe.db.count(

        SOURCE_CHILD_DOCTYPE,

        filters={

            "parenttype": SOURCE_PARENT_DOCTYPE,

            "parentfield": SOURCE_CHILD_PARENTFIELD,

            "parent": project_card,

        },

    )
 
    rows = frappe.get_all(

        SOURCE_CHILD_DOCTYPE,

        filters={

            "parenttype": SOURCE_PARENT_DOCTYPE,

            "parentfield": SOURCE_CHILD_PARENTFIELD,

            "parent": project_card,

        },

        fields=FIELDS_TO_COPY,

        order_by="idx asc",

        limit_start=offset,

        limit_page_length=limit,

    )
 
    return {"total": total, "rows": rows}
 
 
import frappe

from frappe.utils import cint
 
@frappe.whitelist()

def sync_kitted_components(

    target_docname: str,

    project_card: str,

    mode: str = "replace",

    chunk_size: int = 500

):

    target_doc = frappe.get_doc(

        "GENERATE REQUEST - KITTED COMPONENTS",

        target_docname

    )
 
    if mode == "replace":

        target_doc.set("table_reas", [])
 
    chunk_size = max(50, cint(chunk_size))

    offset = 0
 
    while True:

        rows = frappe.get_all(

            "On Box Component Item",

            filters={

                "parenttype": "Cardwise Component List Update and Approve - Designer",

                "parentfield": "table_yvva",

                "parent": project_card,

            },

            fields=["component_type", "link_part_number"],

            order_by="idx asc",

            limit_start=offset,

            limit_page_length=chunk_size,

        )
 
        if not rows:

            break
 
        for r in rows:

            target_doc.append("table_reas", {

                "component_type": r.component_type,

                "link_part_number": r.link_part_number,

            })
 
        offset += chunk_size
 
    target_doc.save()

    return {

        "ok": True,

        "rows_copied": len(target_doc.get("table_reas") or [])

    }

 
 
@frappe.whitelist()

def enqueue_sync_kitted_components(target_docname: str, project_card: str, mode: str = "replace", chunk_size: int = 500):

    """

    For very large tables: enqueue job so request won’t timeout.

    """

    frappe.enqueue(

        "my_app.api._sync_job",

        queue="long",

        job_name=f"sync_kitted_components::{target_docname}",

        target_docname=target_docname,

        project_card=project_card,

        mode=mode,

        chunk_size=chunk_size,

    )

    return {"ok": True, "enqueued": True}
 
 
def _sync_job(target_docname: str, project_card: str, mode: str, chunk_size: int):

    # Run as background job

    frappe.set_user("Administrator")

    sync_kitted_components(target_docname, project_card, mode=mode, chunk_size=chunk_size)

 

#bancode
def check_ban(
    item_code=None,
    date_code=None,
    manufacturer=None,
    quality=None
):
    """
    Global BAN checker
    Call this from ANY DocType
    """

    bans = frappe.get_all(
        "Add BAN",
        filters={
            "status": "Active"
        },
        fields=[
            "ban_type",
            "link_part_number",
            "date_code",
            "manufacturer",
            "quality"
        ]
    )

    for ban in bans:

        # -------------------------------
        # PART NUMBER BAN
        # -------------------------------
        if ban.ban_type == "Part Number BAN":
            if ban.link_part_number == item_code:
                frappe.throw(
                    f"🚫 Item {item_code} is BANNED (Part Number BAN)"
                )

        # -------------------------------
        # DATE CODE BAN
        # -------------------------------
        elif ban.ban_type == "Date Code BAN":
            if ban.date_code == date_code:
                frappe.throw(
                    f"🚫 Date Code {date_code} is BANNED"
                )

        # -------------------------------
        # MANUFACTURER BAN
        # -------------------------------
        elif ban.ban_type == "Manufacturer BAN":
            if ban.manufacturer == manufacturer:
                frappe.throw(
                    f"🚫 Manufacturer {manufacturer} is BANNED"
                )

        # -------------------------------
        # MFR + DATE CODE BAN
        # -------------------------------
        elif ban.ban_type == "MFR + Date Code BAN":
            if ban.manufacturer == manufacturer and ban.date_code == date_code:
                frappe.throw(
                    "🚫 Manufacturer + Date Code combination is BANNED"
                )

        # -------------------------------
        # QUALITY BAN
        # -------------------------------
        elif ban.ban_type == "Quality BAN":
            if ban.quality == quality:
                frappe.throw(
                    f"🚫 Quality {quality} is BANNED"
                )



import frappe

from frappe.utils import today

from datetime import date
 
 
@frappe.whitelist()

def get_project_card_component_list_flight_lifo_soft(project_card, search=None):

    """

    Cardwise Component List

    + Bin-based available qty (correct stock)

    + Flight G1 / G2 warehouses only

    + Soft LIFO ordering using latest valid expiry/date_code

    """
 
    today_date = today()
 
    # --------------------------------------------------

    # 1️⃣ Cardwise Component List (source of items)

    # --------------------------------------------------

    card_items = frappe.get_all(

        "On Box Component Item",

        filters={

            "parenttype": "Cardwise Component List Update and Approve - Designer",

            "parentfield": "table_yvva",

            "parent": project_card,

        },

        fields=[

            "component_type",

            "link_part_number as item_code",

        ],

        order_by="idx asc",

    )
 
    if not card_items:

        return []
 
    item_codes = list({r["item_code"] for r in card_items if r.get("item_code")})
 
    # --------------------------------------------------

    # 2️⃣ Flight G1 / G2 warehouses (name-based filter)

    # --------------------------------------------------

    flight_warehouses = frappe.db.sql("""

        SELECT name

        FROM `tabWarehouse`

        WHERE

            LOWER(name) LIKE '%%flight g1%%'

            OR LOWER(name) LIKE '%%flight g2%%'

            OR LOWER(name) LIKE '%%flight-g1%%'

            OR LOWER(name) LIKE '%%flight-g2%%'

            OR LOWER(name) LIKE '%%fg1%%'

            OR LOWER(name) LIKE '%%fg2%%'

    """, as_dict=True)
 
    flight_wh_names = [w["name"] for w in flight_warehouses]
 
    if not flight_wh_names:

        return []
 
    # --------------------------------------------------

    # 3️⃣ Stock from Bin (SOURCE OF TRUTH FOR QTY)

    # --------------------------------------------------

    bins = frappe.get_all(

        "Bin",

        filters={

            "item_code": ["in", item_codes],

            "warehouse": ["in", flight_wh_names],

            "actual_qty": [">", 0],

        },

        fields=[

            "item_code",

            "warehouse",

            "actual_qty",

            "reserved_qty",

        ],

    )
 
    stock_map = {}

    for b in bins:

        qty = (b.actual_qty or 0) - (b.reserved_qty or 0)

        if qty <= 0:

            continue
 
        stock_map.setdefault(b.item_code, []).append({

            "warehouse": b.warehouse,

            "available_qty": qty,

        })
 
    # --------------------------------------------------

    # 4️⃣ Latest VALID expiry / date code (for ordering only)

    # --------------------------------------------------

    date_rows = frappe.db.sql("""

        SELECT

            sed.item_code,

            sed.t_warehouse AS warehouse,

            MAX(sed.custom_exp_date) AS latest_expiry,

            MAX(sed.custom_date_code) AS latest_date_code

        FROM `tabStock Entry Detail` sed

        WHERE

            sed.item_code IN %(items)s

            AND sed.t_warehouse IN %(warehouses)s

            AND (

                sed.custom_exp_date >= %(today)s

                OR sed.custom_date_code >= DATE_FORMAT(%(today)s, '%%y%%v')

            )

        GROUP BY

            sed.item_code,

            sed.t_warehouse

    """, {

        "items": tuple(item_codes),

        "warehouses": tuple(flight_wh_names),

        "today": today_date,

    }, as_dict=True)
 
    date_map = {

        (d["item_code"], d["warehouse"]): {

            "custom_exp_date": d["latest_expiry"],

            "custom_date_code": d["latest_date_code"],

        }

        for d in date_rows

    }
 
    # --------------------------------------------------

    # 5️⃣ Merge data (item + warehouse + qty + dates)

    # --------------------------------------------------

    result = []
 
    for r in card_items:

        stocks = stock_map.get(r["item_code"], [])
 
        if not stocks:

            result.append({

                "component_type": r["component_type"],

                "item_code": r["item_code"],

                "project_warehouse": None,

                "available_qty": 0,

                "custom_exp_date": None,

                "custom_date_code": None,

            })

        else:

            for s in stocks:

                meta = date_map.get((r["item_code"], s["warehouse"]), {})

                result.append({

                    "component_type": r["component_type"],

                    "item_code": r["item_code"],

                    "project_warehouse": s["warehouse"],

                    "available_qty": s["available_qty"],

                    "custom_exp_date": meta.get("custom_exp_date"),

                    "custom_date_code": meta.get("custom_date_code"),

                })
 
    # --------------------------------------------------

    # 6️⃣ SOFT LIFO SORT (safe type handling)

    # --------------------------------------------------

    def lifo_sort_key(x):

        exp = x.get("custom_exp_date")

        dc = x.get("custom_date_code")
 
        # expiry date → integer

        exp_key = exp.toordinal() if isinstance(exp, date) else 0
 
        # date code (yyww) → integer

        try:

            dc_key = int(dc)

        except (TypeError, ValueError):

            dc_key = 0
 
        return (exp_key, dc_key)
 
    result.sort(key=lifo_sort_key, reverse=True)
 
    # --------------------------------------------------

    # 7️⃣ Search filter

    # --------------------------------------------------

    if search:

        s = search.lower()

        result = [

            r for r in result

            if s in (r.get("item_code") or "").lower()

        ]
 
    return result

#ban get date codes
import frappe
 
@frappe.whitelist()

def get_date_codes_ban(component_type):

    """

    Returns ALL DISTINCT Date Codes for a given Component Type (Item Group)

    using Item → Stock Entry Detail (LEFT JOIN)

    """
 
    if not component_type:

        return []
 
    rows = frappe.db.sql(

        """

        SELECT DISTINCT

            TRIM(sed.custom_date_code) AS date_code

        FROM `tabItem` i

        LEFT JOIN `tabStock Entry Detail` sed

            ON sed.item_code = i.item_code

        WHERE i.item_group = %s

          AND sed.custom_date_code IS NOT NULL

          AND sed.custom_date_code != ''

        ORDER BY date_code

        """,

        (component_type,),

        as_dict=True

    )
 
    return [r.date_code for r in rows]

#Trigger erpnext item disable functioanlity thorugh ban for datecode
@frappe.whitelist()

def get_mfr_by_component(component_type):

    if not component_type:

        return []
 
    rows = frappe.db.sql("""

        SELECT DISTINCT im.manufacturer

        FROM `tabItem Manufacturer` im

        INNER JOIN `tabStock Entry Detail` sed

            ON sed.item_code = im.item_code

        WHERE sed.custom_select_component_type = %s

          AND im.manufacturer IS NOT NULL

          AND im.manufacturer != ''

    """, component_type, as_list=True)
 
    return sorted({r[0] for r in rows})

 
 
@frappe.whitelist()

def get_datecodes_by_component_and_mfr(component_type, mfr):

    if not component_type or not mfr:

        return []
 
    rows = frappe.db.sql("""

        SELECT DISTINCT sed.custom_date_code

        FROM `tabStock Entry Detail` sed

        INNER JOIN `tabItem Manufacturer` im

            ON im.item_code = sed.item_code

        WHERE sed.item_group = %s

          AND im.manufacturer = %s

          AND sed.custom_date_code IS NOT NULL

          AND sed.custom_date_code != ''

    """, (component_type, mfr), as_list=True)
 
    return sorted({r[0] for r in rows})

#Excel 
import frappe
from frappe.utils.xlsxutils import make_xlsx

@frappe.whitelist()
def download_prj_sub_excel_dynamic(names, fields=None):

    names = [n for n in names.split(",") if n]
    meta = frappe.get_meta("PRJ_SUB")

    # -------------------------------
    # 1️⃣ Collect fields from client
    # -------------------------------
    client_fields = []
    if fields:
        client_fields = [f.strip() for f in fields.split(",") if f]

    # -------------------------------
    # 2️⃣ Validate fields
    # -------------------------------
    valid_fields = [
        f for f in client_fields
        if meta.has_field(f) or f == "name"
    ]

    # -------------------------------
    # 3️⃣ FALLBACK → List View fields
    # -------------------------------
    if not valid_fields:
        valid_fields = ["name"]

        for df in meta.fields:
            if df.in_list_view:
                valid_fields.append(df.fieldname)

    # still empty? (very rare)
    if not valid_fields:
        frappe.throw("No exportable fields found")

    # -------------------------------
    # 4️⃣ Headers
    # -------------------------------
    headers = [
        meta.get_label(f) if f != "name" else "ID"
        for f in valid_fields
    ]

    data = [headers]

    # -------------------------------
    # 5️⃣ Data rows
    # -------------------------------
    for name in names:
        row = frappe.db.get_value(
            "PRJ_SUB",
            name,
            valid_fields,
            as_dict=True
        )

        data.append([
            row.get(f, "") if row else ""
            for f in valid_fields
        ])

    xlsx_file = make_xlsx(data, "PRJ_SUB_List")

    frappe.response.clear()
    frappe.response["filename"] = "PRJ_SUB_List.xlsx"
    frappe.response["filecontent"] = xlsx_file.getvalue()
    frappe.response["type"] = "binary"


#PDF
@frappe.whitelist()
def download_prj_sub_pdf_dynamic(names, fields=None):

    names = [n for n in names.split(",") if n]
    meta = frappe.get_meta("PRJ_SUB")

    if not names:
        frappe.throw("No records selected")

    # -------------------------------
    # 1️⃣ Collect fields from client
    # -------------------------------
    client_fields = []
    if fields:
        client_fields = [f.strip() for f in fields.split(",") if f]

    # -------------------------------
    # 2️⃣ Validate fields
    # -------------------------------
    valid_fields = [
        f for f in client_fields
        if meta.has_field(f) or f == "name"
    ]

    # -------------------------------
    # 3️⃣ FALLBACK → List View fields
    # -------------------------------
    if not valid_fields:
        valid_fields = ["name"]
        for df in meta.fields:
            if df.in_list_view:
                valid_fields.append(df.fieldname)

    if not valid_fields:
        frappe.throw("No exportable fields found")

    # -------------------------------
    # 4️⃣ Headers
    # -------------------------------
    headers = [
        meta.get_label(f) if f != "name" else "ID"
        for f in valid_fields
    ]

    # -------------------------------
    # 5️⃣ Build HTML
    # -------------------------------
    html = """
    <h3 style="text-align:center;">Project SubSystem</h3>
    <table border="1" width="100%" cellspacing="0" cellpadding="5">
        <thead>
            <tr>
    """

    for h in headers:
        html += f"<th>{escape_html(h)}</th>"

    html += "</tr></thead><tbody>"

    # -------------------------------
    # 6️⃣ Data rows
    # -------------------------------
    for name in names:
        row = frappe.db.get_value(
            "PRJ_SUB",
            name,
            valid_fields,
            as_dict=True
        )

        html += "<tr>"
        for f in valid_fields:
            value = row.get(f, "") if row else ""
            html += f"<td>{escape_html(str(value))}</td>"
        html += "</tr>"

    html += "</tbody></table>"

    # -------------------------------
    # 7️⃣ Convert to PDF
    # -------------------------------
    pdf = get_pdf(html)

    frappe.response.clear()
    frappe.response["filename"] = "PRJ_SUB_List.pdf"
    frappe.response["filecontent"] = pdf
    frappe.response["type"] = "binary"



#item alternate get and delete
import frappe
 
@frappe.whitelist()

def get_item_alternatives(item_code):
 
    if not item_code:

        return []
 
    return frappe.db.sql(

        """

        SELECT alternative_item_code

        FROM `tabItem Alternative`

        WHERE item_code = %s

        """,

        item_code,

        as_dict=True

    )

import frappe
 
@frappe.whitelist()

def delete_item_alternatives(item_code, alternatives_json):
 
    if not item_code:

        frappe.throw("item_code is required")
 
    alternatives = frappe.parse_json(alternatives_json) or []
 
    if not isinstance(alternatives, list):

        frappe.throw("alternatives_json must be a JSON list")
 
    deleted = []
 
    for alt_item in alternatives:

        if not alt_item:

            continue
 
        frappe.db.delete(

            "Item Alternative",

            {

                "item_code": item_code,

                "alternative_item_code": alt_item

            }

        )

        deleted.append(alt_item)
 
    return {

        "item_code": item_code,

        "deleted": deleted

    }

 #api for screening and relifing
import frappe
 
@frappe.whitelist()

def get_item_groups_by_project(doctype, txt, searchfield, start, page_len, filters):

    # ---- DEBUG: log call ----

    frappe.log_error(

        title="Item Group Filter Debug",

        message=f"Filters received: {filters}"

    )
 
    project = filters.get("project") if filters else None
 
    if not project:

        return []
 
    query = """

        SELECT DISTINCT

            ig.name

        FROM `tabItem Group` ig

        WHERE ig.name IN (
 
            SELECT i.item_group

            FROM `tabPurchase Order` po

            JOIN `tabPurchase Order Item` poi ON poi.parent = po.name

            JOIN `tabItem` i ON i.name = poi.item_code

            WHERE po.project = %(project)s

              AND po.docstatus = 1
 
            UNION
 
            SELECT i.item_group

            FROM `tabPurchase Receipt` pr

            JOIN `tabPurchase Receipt Item` pri ON pri.parent = pr.name

            JOIN `tabItem` i ON i.name = pri.item_code

            WHERE pr.project = %(project)s

              AND pr.docstatus = 1
 
            UNION
 
            SELECT i.item_group

            FROM `tabStock Entry` se

            JOIN `tabStock Entry Detail` sed ON sed.parent = se.name

            JOIN `tabItem` i ON i.name = sed.item_code

            JOIN `tabProject` p ON p.project_name = se.custom_select_project

            WHERE p.name = %(project)s

              AND se.stock_entry_type = 'Stock Entry'

              AND se.docstatus = 1

        )

        AND ig.name LIKE %(txt)s

        LIMIT %(start)s, %(page_len)s

    """
 
    result = frappe.db.sql(

        query,

        {

            "project": project,

            "txt": f"%{txt}%",

            "start": start,

            "page_len": page_len

        }

    )
 
    # ---- DEBUG: log result ----

    frappe.log_error(

        title="Item Group Filter Result",

        message=str(result)

    )
 
    return result

 
 #
 
#api for scr and rlf item_code
import frappe
 
@frappe.whitelist()


@frappe.whitelist()

def get_items_by_project(doctype, txt, searchfield, start, page_len, filters):

    filters = filters or {}

    project = filters.get("project")           # Project PK like "22"

    item_group = filters.get("item_group")     # Item Group like "Cables & Wires"
 
    if not project:

        return []
 
    # Map Project PK -> project_name (needed because Stock Entry stores project_name in custom_select_project)

    project_name = frappe.db.get_value("Project", project, "project_name")

    if not project_name:

        return []
 
    return frappe.db.sql("""

        SELECT DISTINCT i.name

        FROM `tabItem` i

        WHERE i.name IN (
 
            /* Purchase Order */

            SELECT poi.item_code

            FROM `tabPurchase Order` po

            JOIN `tabPurchase Order Item` poi ON poi.parent = po.name

            WHERE po.project = %(project)s

              AND po.docstatus = 1
 
            UNION
 
            /* Purchase Receipt */

            SELECT pri.item_code

            FROM `tabPurchase Receipt` pr

            JOIN `tabPurchase Receipt Item` pri ON pri.parent = pr.name

            WHERE pr.project = %(project)s

              AND pr.docstatus = 1
 
            UNION
 
            /* Stock Entry (matches by Project Name) */

            SELECT sed.item_code

            FROM `tabStock Entry` se

            JOIN `tabStock Entry Detail` sed ON sed.parent = se.name

            WHERE se.custom_select_project = %(project_name)s

              AND se.stock_entry_type = 'Stock Entry'

              AND se.docstatus = 1

        )

        AND (%(item_group)s IS NULL OR i.item_group = %(item_group)s)

        AND i.name LIKE %(txt)s

        LIMIT %(start)s, %(page_len)s

    """, {

        "project": project,

        "project_name": project_name,

        "item_group": item_group,

        "txt": f"%{txt}%",

        "start": start,

        "page_len": page_len

    })

 
 