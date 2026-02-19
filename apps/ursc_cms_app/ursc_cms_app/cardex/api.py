import frappe
 
@frappe.whitelist()

def get_cardex_by_mapping(select_store, select_program, select_stock, mdb_part_no=None):

    """

    Fetch Cardex ONLY if mapping AND MDB match.

    """
 
    if not (select_store and select_program and select_stock):

        return None
 
    # Base query

    filters = {

        "select_store": select_store,

        "select_program": select_program,

        "select_stock": select_stock,

    }
 
    # Find candidate Cardex parents

    rows = frappe.get_all(

        "Warehouse Location Stock Grade",

        filters=filters,

        fields=["parent"]

    )
 
    if not rows:

        return None
 
    # If MDB provided, filter by MDB

    for r in rows:

        cardex = frappe.db.get_value(

            "Warehouse Location Master",

            r.parent,

            ["name", "mdb_part_no"],

            as_dict=True

        )
 
        # If MDB not yet assigned → allow it

        if not cardex.mdb_part_no:

            return cardex
 
        # If MDB matches → correct Cardex

        if mdb_part_no and cardex.mdb_part_no == mdb_part_no:

            return cardex
 
    # No matching MDB Cardex found

    return None

 