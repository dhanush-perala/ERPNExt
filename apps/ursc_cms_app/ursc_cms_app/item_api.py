import frappe
 
@frappe.whitelist()

def get_item_groups_by_project(doctype, txt, searchfield, start, page_len, filters):

    project = filters.get("project") if filters else None

    if not project:

        return []
 
    return frappe.db.sql("""

        SELECT DISTINCT ig.name

        FROM `tabItem Group` ig

        WHERE ig.name IN (
 
            SELECT i.item_group

            FROM `tabPurchase Order` po

            JOIN `tabPurchase Order Item` poi ON poi.parent = po.name

            JOIN `tabItem` i ON i.name = poi.item_code

            WHERE po.project = %(project)s AND po.docstatus = 1
 
            UNION
 
            SELECT i.item_group

            FROM `tabPurchase Receipt` pr

            JOIN `tabPurchase Receipt Item` pri ON pri.parent = pr.name

            JOIN `tabItem` i ON i.name = pri.item_code

            WHERE pr.project = %(project)s AND pr.docstatus = 1
 
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

    """, {

        "project": project,

        "txt": f"%{txt}%",

        "start": start,

        "page_len": page_len

    })

@frappe.whitelist()

def get_items_by_project(doctype, txt, searchfield, start, page_len, filters):

    filters = filters or {}

    project = filters.get("project")

    item_group = filters.get("item_group")
 
    if not project:

        return []
 
    project_name = frappe.db.get_value("Project", project, "project_name")
 
    return frappe.db.sql("""

        SELECT DISTINCT i.name

        FROM `tabItem` i

        WHERE i.name IN (
 
            SELECT poi.item_code

            FROM `tabPurchase Order` po

            JOIN `tabPurchase Order Item` poi ON poi.parent = po.name

            WHERE po.project = %(project)s AND po.docstatus = 1
 
            UNION
 
            SELECT pri.item_code

            FROM `tabPurchase Receipt` pr

            JOIN `tabPurchase Receipt Item` pri ON pri.parent = pr.name

            WHERE pr.project = %(project)s AND pr.docstatus = 1
 
            UNION
 
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


import frappe

@frappe.whitelist()
def get_stock_grades_by_project_and_component(
    doctype, txt, searchfield, start, page_len, filters
):
    project = filters.get("project") if filters else None
    component_type = filters.get("component_type") if filters else None

    if not project:
        return []

    return frappe.db.sql("""
        SELECT DISTINCT w.name
        FROM `tabWarehouse` w
        WHERE w.name IN (

            /* -------------------------------
             * Purchase Order
             * ------------------------------- */
            SELECT sed.t_warehouse
            FROM `tabPurchase Order` po
            JOIN `tabPurchase Order Item` poi ON poi.parent = po.name
            JOIN `tabStock Entry Detail` sed ON sed.item_code = poi.item_code
            WHERE po.project = %(project)s
              AND po.docstatus = 1

            UNION

            /* -------------------------------
             * Purchase Receipt
             * ------------------------------- */
            SELECT sed.t_warehouse
            FROM `tabPurchase Receipt` pr
            JOIN `tabPurchase Receipt Item` pri ON pri.parent = pr.name
            JOIN `tabStock Entry Detail` sed ON sed.item_code = pri.item_code
            WHERE pr.project = %(project)s
              AND pr.docstatus = 1

            UNION

            /* -------------------------------
             * Stock Entry
             * ------------------------------- */
            SELECT sed.t_warehouse
            FROM `tabStock Entry` se
            JOIN `tabStock Entry Detail` sed ON sed.parent = se.name
            JOIN `tabItem` i ON i.name = sed.item_code
            WHERE se.docstatus = 1
              AND se.custom_select_project = %(project)s
              AND (%(component_type)s IS NULL OR i.item_group = %(component_type)s)
        )
        AND w.name LIKE %(txt)s
        ORDER BY w.name
        LIMIT %(start)s, %(page_len)s
    """, {
        "project": project,
        "component_type": component_type,
        "txt": f"%{txt}%",
        "start": start,
        "page_len": page_len
    })


import frappe
 
@frappe.whitelist()

def get_target_warehouses_by_project(project):

    """

    Fetch DISTINCT Target Warehouses (t_warehouse)

    from Stock Entry Detail based on selected Project

    """
 
    if not project:

        return []
 
    rows = frappe.db.sql(

        """

        SELECT DISTINCT sed.t_warehouse

        FROM `tabStock Entry Detail` sed

        INNER JOIN `tabStock Entry` se

            ON se.name = sed.parent

        WHERE se.project = %s

          AND sed.t_warehouse IS NOT NULL

          AND sed.t_warehouse != ''

        """,

        project,

        as_list=True

    )
 
    # Convert [('WH-01',), ('WH-02',)] → ['WH-01', 'WH-02']

    return [r[0] for r in rows]

 



 
@frappe.whitelist()

def get_items_by_component_and_stock(doctype, txt, searchfield, start, page_len, filters):

    component_type = filters.get("component_type")

    stock = filters.get("stock")
 
    if not component_type or not stock:

        return []
 
    return frappe.db.sql("""

        SELECT DISTINCT i.name

        FROM `tabItem` i

        INNER JOIN `tabStock Entry Detail` sed

            ON sed.item_code = i.name

        WHERE i.item_group = %s

          AND sed.t_warehouse = %s

          AND i.disabled = 0

        ORDER BY i.name

        LIMIT %s OFFSET %s

    """, (component_type, stock, page_len, start))

 

 
@frappe.whitelist()

def get_date_codes_by_component_and_stock(component_type, stock):

    if not component_type or not stock:

        return []
 
    return frappe.db.sql("""

        SELECT DISTINCT sed.custom_date_code

        FROM `tabStock Entry Detail` sed

        INNER JOIN `tabItem` i

            ON i.name = sed.item_code

        WHERE i.item_group = %s

          AND sed.t_warehouse = %s

          AND sed.custom_date_code IS NOT NULL

          AND sed.custom_date_code != ''

        ORDER BY sed.custom_date_code

    """, (component_type, stock))

 
@frappe.whitelist()

def get_quality_by_component_and_stock(doctype, txt, searchfield, start, page_len, filters):
 
    component_type = filters.get("component_type")

    stock = filters.get("stock")
 
    if not component_type or not stock:

        return []
 
    return frappe.db.sql("""

        SELECT DISTINCT sed.custom_quality

        FROM `tabStock Entry Detail` sed

        INNER JOIN `tabItem` i

            ON i.name = sed.item_code

        WHERE i.item_group = %s

          AND sed.t_warehouse = %s

          AND sed.custom_quality IS NOT NULL

          AND sed.custom_quality != ''

        ORDER BY sed.custom_quality

        LIMIT %s OFFSET %s

    """, (component_type, stock, page_len, start))




import frappe
 
@frappe.whitelist()

def get_manufacturers_by_component_and_stock(

    doctype, txt, searchfield, start, page_len, filters

):

    component_type = filters.get("component_type")

    stock = filters.get("stock")
 
    if not component_type or not stock:

        return []
 
    return frappe.db.sql("""

        SELECT DISTINCT im.manufacturer

        FROM `tabItem Manufacturer` im

        INNER JOIN `tabItem` i

            ON i.name = im.item_code

        INNER JOIN `tabStock Entry Detail` sed

            ON sed.item_code = i.name

        WHERE i.item_group = %s

          AND sed.t_warehouse = %s

          AND im.manufacturer IS NOT NULL

          AND im.manufacturer != ''

        ORDER BY im.manufacturer

        LIMIT %s OFFSET %s

    """, (component_type, stock, page_len, start))

@frappe.whitelist()

def get_mfr_by_component_and_stock(component_type, stock):
 
    if not component_type or not stock:

        return []
 
    return frappe.db.sql("""

        SELECT DISTINCT im.manufacturer

        FROM `tabItem Manufacturer` im

        INNER JOIN `tabItem` i

            ON i.name = im.item_code

        INNER JOIN `tabStock Entry Detail` sed

            ON sed.item_code = i.name

        WHERE i.item_group = %s

          AND sed.t_warehouse = %s

          AND im.manufacturer IS NOT NULL

          AND im.manufacturer != ''

        ORDER BY im.manufacturer

    """, (component_type, stock))

 
@frappe.whitelist()

def get_datecode_by_mfr_component_stock(component_type, stock, mfr):
 
    if not component_type or not stock or not mfr:

        return []
 
    return frappe.db.sql("""

        SELECT DISTINCT sed.custom_date_code

        FROM `tabStock Entry Detail` sed

        INNER JOIN `tabItem` i

            ON i.name = sed.item_code

        INNER JOIN `tabItem Manufacturer` im

            ON im.item_code = i.name

        WHERE i.item_group = %s

          AND sed.t_warehouse = %s

          AND im.manufacturer = %s

          AND sed.custom_date_code IS NOT NULL

          AND sed.custom_date_code != ''

        ORDER BY sed.custom_date_code

    """, (component_type, stock, mfr))

 