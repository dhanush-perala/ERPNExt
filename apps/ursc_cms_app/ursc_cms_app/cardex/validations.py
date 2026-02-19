import frappe
 
def validate_location_master(doc, method=None):

    """

    Validation for Warehouse Location Master

    Child table fieldname = select_warehouse

    """
 
    logger = frappe.logger("cardex_validation", allow_site=True)
 
    logger.info("VALIDATE called for Cardex %s", doc.name)

    print(f"[CARDEX VALIDATE] Called for {doc.name}")
 
    # Child table rows (mapping)

    rows = doc.get("select_warehouse") or []
 
    # -------------------------------

    # RULE 1: No duplicate mapping INSIDE same Cardex

    # -------------------------------

    seen = set()

    for r in rows:

        key = (r.select_store, r.select_program, r.select_stock)

        if key in seen:

            frappe.throw(

                "Duplicate Store / Program / Stock row found inside the same Cardex."

            )

        seen.add(key)
 
    # -------------------------------

    # RULE 2: Global uniqueness ONLY when

    # physical location is SAME

    # -------------------------------

    for r in rows:

        if not (r.select_store and r.select_program and r.select_stock):

            continue
 
        # Look for same mapping in OTHER Cardex

        other = frappe.db.sql(

            """

            SELECT wls.parent

            FROM `tabWarehouse Location Stock Grade` wls

            JOIN `tabWarehouse Location Master` wlm

              ON wlm.name = wls.parent

            WHERE

                wls.select_store = %s

                AND wls.select_program = %s

                AND wls.select_stock = %s

                AND wls.parent != %s

                AND wlm.block = %s

                AND wlm.rack = %s

                AND IFNULL(wlm.enter_location, '') = IFNULL(%s, '')

            LIMIT 1

            """,

            (

                r.select_store,

                r.select_program,

                r.select_stock,

                doc.name,

                doc.block,

                doc.rack,

                doc.enter_location,

            ),

            as_dict=True

        )
 
        if other:

            logger.error(

                "Duplicate physical location detected for mapping %s/%s/%s",

                r.select_store, r.select_program, r.select_stock

            )
 
            frappe.throw(

                f"This Store / Program / Stock mapping already exists "

                f"at the same physical location "

                f"(Block: {doc.block}, Rack: {doc.rack}, Location: {doc.enter_location}) "

                f"in Cardex {other[0]['parent']}."

            )
 
    logger.info("VALIDATE successful for Cardex %s", doc.name)

    print(f"[CARDEX VALIDATE] Validation successful for {doc.name}")

 