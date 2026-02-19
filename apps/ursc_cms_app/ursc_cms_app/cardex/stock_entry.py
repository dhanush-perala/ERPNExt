import frappe

# Create a dedicated logger
logger = frappe.logger("cardex_stock_entry", allow_site=True)


def on_submit(doc, method=None):
    logger.info("on_submit CALLED for Stock Entry %s", doc.name)
    print(f"[CARDEX] on_submit called for {doc.name}")

    if not _is_target_stock_entry(doc):
        logger.info("Stock Entry %s ignored (stock_entry_type != 'Stock Entry')", doc.name)
        print("[CARDEX] stock_entry_type mismatch")
        return

    _process(doc, is_cancel=False)


def on_cancel(doc, method=None):
    logger.info("on_cancel CALLED for Stock Entry %s", doc.name)
    print(f"[CARDEX] on_cancel called for {doc.name}")

    if not _is_target_stock_entry(doc):
        return

    _process(doc, is_cancel=True)


def _is_target_stock_entry(doc):
    val = getattr(doc, "stock_entry_type", None)
    logger.info("stock_entry_type = %s", val)
    return val == "Stock Entry"


def _process(doc, is_cancel):
    if not getattr(doc, "items", None):
        logger.warning("No items found in Stock Entry %s", doc.name)
        return

    for row in doc.items:
        try:
            _process_row(row, is_cancel)
        except Exception:
            frappe.log_error(
                frappe.get_traceback(),
                "Cardex Stock Entry Processing Failed"
            )
            raise


def _process_row(row, is_cancel):
    store = getattr(row, "custom_target_store_", None)
    program = getattr(row, "custom_target_program", None)
    stock = getattr(row, "custom_target_stock", None)
    mdb = (getattr(row, "custom_mdb_part_no", None) or "").strip()

    logger.info(
        "Processing row %s | store=%s program=%s stock=%s mdb=%s",
        row.name, store, program, stock, mdb
    )

    print(
        f"[CARDEX] Row {row.name} | "
        f"store={store}, program={program}, stock={stock}, mdb={mdb}"
    )

    if not (store and program and stock and mdb):
        logger.warning("Missing required fields in row %s", row.name)
        return

    # 🔍 FIND CARDEX BY CHILD MAPPING
    cardex_name = frappe.db.get_value(
        "Warehouse Location Stock Grade",
        {
            "select_store": store,
            "select_program": program,
            "select_stock": stock,
        },
        "parent"
    )

    logger.info("Matched Cardex = %s", cardex_name)
    print(f"[CARDEX] Matched Cardex = {cardex_name}")

    if not cardex_name:
        frappe.throw(
            "No Cardex mapping found for selected Store / Program / Stock"
        )

    cardex = frappe.get_doc("Warehouse Location Master", cardex_name)

    # 🔐 VALIDATE / SET MDB
    if cardex.mdb_part_no:
        if cardex.mdb_part_no != mdb:
            frappe.throw(
                f"Cardex {cardex.name} already assigned to MDB {cardex.mdb_part_no}"
            )
        logger.info("MDB already matches for Cardex %s", cardex.name)
    else:
        logger.info("Assigning MDB %s to Cardex %s", mdb, cardex.name)
        cardex.mdb_part_no = mdb
        cardex.save(ignore_permissions=True)

    # 🔗 LINK STOCK ENTRY DETAIL
    frappe.db.set_value(
        "Stock Entry Detail",
        row.name,
        "custom_select_location",
        cardex.name,
        update_modified=False
    )

    logger.info(
        "Linked Stock Entry Detail %s -> Cardex %s",
        row.name, cardex.name
    )
    print(
        f"[CARDEX] Linked row {row.name} to Cardex {cardex.name}"
    )
