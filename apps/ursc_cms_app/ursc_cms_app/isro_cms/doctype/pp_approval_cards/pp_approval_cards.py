import frappe

from frappe.model.document import Document

from frappe.utils import cstr
 
LOGGER_NAME = "pp_approval_cards"

PARENT_ITEM_GROUP = "All Cards"

DEFAULT_UOM = "Nos"
 
 
# ------------------------------------------------------------

# Helpers

# ------------------------------------------------------------

def log():

    return frappe.logger(LOGGER_NAME)
 
 
def clean(val):

    return cstr(val).strip() if val else ""
 
 
# ------------------------------------------------------------

# Ensure PSTYLE

# ------------------------------------------------------------

def ensure_pstyle(package_style_name):

    package_style_name = clean(package_style_name)

    if not package_style_name:

        return None
 
    existing = frappe.db.get_value(

        "PSTYLE",

        {"package_style_name": package_style_name},

        "name",

    )

    if existing:

        return existing
 
    ps = frappe.new_doc("PSTYLE")

    ps.package_style_name = package_style_name

    ps.insert(ignore_permissions=True)
 
    log().info(f"PSTYLE created → {ps.name}")

    return ps.name
 
 
# ------------------------------------------------------------

# Ensure Item Group (leaf)

# ------------------------------------------------------------

def ensure_leaf_item_group(card_name):

    if not frappe.db.exists("Item Group", PARENT_ITEM_GROUP):

        frappe.throw(f"Item Group '{PARENT_ITEM_GROUP}' not found")
 
    parent_is_group = frappe.db.get_value(

        "Item Group", PARENT_ITEM_GROUP, "is_group"

    )
 
    if not parent_is_group:

        return PARENT_ITEM_GROUP
 
    existing = frappe.db.get_value(

        "Item Group",

        {

            "parent_item_group": PARENT_ITEM_GROUP,

            "item_group_name": card_name,

        },

        "name",

    )

    if existing:

        return existing
 
    ig = frappe.new_doc("Item Group")

    ig.item_group_name = card_name

    ig.parent_item_group = PARENT_ITEM_GROUP

    ig.is_group = 0
 
    try:

        ig.insert(ignore_permissions=True)

    except frappe.DuplicateEntryError:

        return frappe.db.get_value(

            "Item Group",

            {

                "parent_item_group": PARENT_ITEM_GROUP,

                "item_group_name": card_name,

            },

            "name",

        )
 
    return ig.name
 
 
# ------------------------------------------------------------

# Core Item Creation (2-phase, rollback-safe)

# ------------------------------------------------------------

def create_item_safely(card_name, package_style_name=None, basic_mdb=None):

    card_name = clean(card_name)

    if not card_name:

        return {"status": "skipped", "reason": "empty_card_name"}
 
    if frappe.db.exists("Item", card_name):

        return {"status": "exists", "item_code": card_name}
 
    item_group = ensure_leaf_item_group(card_name)
 
    def build_item():

        item = frappe.new_doc("Item")

        item.item_code = card_name

        item.item_name = card_name

        item.item_group = item_group

        item.stock_uom = DEFAULT_UOM

        item.is_stock_item = 0

        item.maintain_stock = 0

        item.is_pd_approval_card = 1

        return item
 
    # -------- Attempt 1: minimal --------

    try:

        item = build_item()

        item.insert(ignore_permissions=True)

        return {

            "status": "created",

            "item_code": card_name,

            "mode": "minimal",

        }
 
    except frappe.MandatoryError:

        log().warning(f"MandatoryError → retrying with dependencies: {card_name}")
 
    except frappe.ValidationError:

        log().warning(f"ValidationError → retrying with dependencies: {card_name}")
 
    except Exception:

        log().warning(

            f"Unknown error on minimal insert → retrying\n{frappe.get_traceback()}"

        )
 
    # -------- Ensure dependencies --------

    pstyle_name = ensure_pstyle(package_style_name)
 
    item = build_item()
 
    if pstyle_name:

        item.custom_package_style = pstyle_name
 
    if basic_mdb:

        row = item.append("basic_mdb_child_table", {})

        row.enter_basic_mdb = basic_mdb
 
    # -------- Attempt 2 --------

    item.insert(ignore_permissions=True)
 
    return {

        "status": "created",

        "item_code": card_name,

        "mode": "with_dependencies",

    }
 
 
# ------------------------------------------------------------

# Controller

# ------------------------------------------------------------

class PPApprovalCards(Document):

    def on_submit(self):

        rows = self.pp_approval_items or []

        log().info(f"[{self.name}] Submit start → rows={len(rows)}")
 
        for idx, row in enumerate(rows, start=1):

            try:

                result = create_item_safely(

                    card_name=row.card_name,

                    package_style_name=row.package_style_name,

                    basic_mdb=row.enter_basic_mdb,

                )

                log().info(f"[{self.name}] Row {idx} → {result}")
 
            except Exception:

                log().error(

                    f"[{self.name}] Row {idx} FAILED\n{frappe.get_traceback()}"

                )

                continue
 
        log().info(f"[{self.name}] Submit finished")

 