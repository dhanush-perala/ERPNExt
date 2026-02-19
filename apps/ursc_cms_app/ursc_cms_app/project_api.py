import frappe
 
@frappe.whitelist()

def get_project_warehouses(project):

    """

    Fetch warehouses from Project warhouse child table

    """

    if not project:

        return []
 
    return frappe.db.sql("""

        SELECT pw.stock

        FROM `tabProject warhouse` pw

        WHERE pw.parent = %(project)s

          AND pw.parenttype = 'Project'

    """, {"project": project})

 
@frappe.whitelist()

def get_warehouse_by_stock_grade(doctype, txt, searchfield, start, page_len, filters):

    filters = filters or {}

    grade = (filters.get("stock_grade") or "").lower()
 
    if not grade:

        return []
 
    # Build LIKE conditions based on grade

    conditions = []
 
    if "g1" in grade:

        conditions = [

            "%flight g1%",

            "%flight-g1%",

            "%fg1%",

            "%to scr%"

        ]

    elif "g2" in grade:

        conditions = [

            "%flight g2%",

            "%flight-g2%",

            "%fg2%",

            "%to scr%"

        ]

    else:

        return []
 
    like_sql = " OR ".join(["LOWER(w.name) LIKE %s"] * len(conditions))
 
    return frappe.db.sql(f"""

        SELECT w.name

        FROM `tabWarehouse` w

        WHERE ({like_sql})

          AND LOWER(w.name) LIKE %s

        LIMIT %s, %s

    """, tuple(conditions + [f"%{txt.lower()}%", start, page_len]))

 