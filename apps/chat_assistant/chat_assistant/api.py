import frappe

@frappe.whitelist()
def ping():
    return {"ok": True, "msg": "pong"}

import frappe
from frappe import _

DOC_PATTERNS = [
    # --- STOCK / INVENTORY ---
    ("Item", "Item", ["name", "item_code"], ["item_name", "item_group", "stock_uom"]),
    ("Warehouse", "Warehouse", ["name"], ["warehouse_name", "company"]),
    ("Stock Entry", "Stock Entry", ["name"], ["purpose", "posting_date", "docstatus"]),
    ("Stock Reconciliation", "Stock Reconciliation", ["name"], ["posting_date"]),
    ("Delivery Note", "Delivery Note", ["name"], ["customer", "status", "posting_date"]),
    ("Purchase Receipt", "Purchase Receipt", ["name"], ["supplier", "status", "posting_date"]),

    # --- MANUFACTURING ---
    ("BOM", "BOM", ["name"], ["item", "is_active", "is_default"]),
    ("Work Order", "Work Order", ["name"], ["production_item", "status", "qty", "planned_start_date"]),
    ("Job Card", "Job Card", ["name"], ["operation_id", "work_order", "status"]),
    ("Operation", "Operation", ["name"], ["workstation", "description"]),
    ("Workstation", "Workstation", ["name"], ["workstation_name", "production_capacity"]),

    # --- BUYING ---
    ("Supplier", "Supplier", ["name"], ["supplier_name", "supplier_group"]),
    ("Purchase Order", "Purchase Order", ["name"], ["supplier", "status", "transaction_date"]),
    ("Purchase Invoice", "Purchase Invoice", ["name"], ["supplier", "posting_date", "status"]),
    ("Material Request", "Material Request", ["name"], ["material_request_type", "status", "transaction_date"]),

    # --- SELLING ---
    ("Customer", "Customer", ["name"], ["customer_name", "customer_group"]),
    ("Quotation", "Quotation", ["name"], ["customer_name", "status", "transaction_date"]),
    ("Sales Order", "Sales Order", ["name"], ["customer", "status", "transaction_date"]),
    ("Sales Invoice", "Sales Invoice", ["name"], ["customer", "status", "posting_date"]),
]

def _format_row(label, doc):
    """Return a compact, readable summary string for one doc."""
    # -----------------------------
    # MATERIALS & INVENTORY
    # -----------------------------
    if doc.doctype == "Material Request":
        lines = [
            f"Material Request: {doc.name}",
            f"Type: {doc.get('material_request_type')}, Status: {doc.get('status')}",
            f"Date: {doc.get('transaction_date')}",
            "Items:",
        ]
        for d in doc.get("items", []):
            lines.append(f"  - {d.item_code} | Qty: {d.qty} {d.uom} | For: {d.schedule_date}")
        return "\n".join(lines)

    if doc.doctype == "Stock Entry":
        lines = [
            f"Stock Entry: {doc.name}",
            f"Purpose: {doc.get('purpose')}",
            f"Posting: {doc.get('posting_date')} {doc.get('posting_time')}",
            "Items:",
        ]
        for d in doc.get("items", []):
            s = f"  - {d.item_code} | Qty: {d.qty}"
            if d.get("s_warehouse"): s += f" | From: {d.s_warehouse}"
            if d.get("t_warehouse"): s += f" | To: {d.t_warehouse}"
            lines.append(s)
        return "\n".join(lines)

    if doc.doctype == "Stock Reconciliation":
        lines = [
            f"Stock Reconciliation: {doc.name}",
            f"Posting Date: {doc.get('posting_date')}",
            "Items:",
        ]
        for d in doc.get("items", []):
            lines.append(f"  - {d.item_code} | Qty: {d.qty} | Valuation Rate: {d.valuation_rate}")
        return "\n".join(lines)

    if doc.doctype == "Warehouse":
        return f"Warehouse: {doc.warehouse_name} | Company: {doc.company}"

    if doc.doctype == "Item":
        lines = [
            f"Item: {doc.get('item_code') or doc.name}",
            f"Name: {doc.get('item_name')} | Group: {doc.get('item_group')}",
            f"UoM: {doc.get('stock_uom')} | Disabled: {doc.get('disabled')}",
        ]
        return "\n".join(lines)

    # -----------------------------
    # MANUFACTURING
    # -----------------------------
    if doc.doctype == "BOM":
        lines = [
            f"BOM: {doc.name}",
            f"Item: {doc.get('item')} | Qty: {doc.get('quantity')}",
            f"Active: {doc.get('is_active')} | Default: {doc.get('is_default')}",
            "Components:",
        ]
        for d in doc.get("items", []):
            lines.append(f"  - {d.item_code} | Qty: {d.qty} {d.uom}")
        return "\n".join(lines)

    if doc.doctype == "Work Order":
        lines = [
            f"Work Order: {doc.name}",
            f"Item: {doc.get('production_item')} | Qty: {doc.get('qty')}",
            f"Status: {doc.get('status')} | Planned Start: {doc.get('planned_start_date')}",
        ]
        if doc.get("operations"):
            lines.append("Operations:")
            for op in doc.get("operations"):
                lines.append(f"  - {op.operation} | Planned: {op.planned_start_time} → {op.planned_end_time}")
        return "\n".join(lines)

    if doc.doctype == "Job Card":
        lines = [
            f"Job Card: {doc.name}",
            f"Work Order: {doc.work_order} | Operation: {doc.operation}",
            f"Status: {doc.status} | Employee: {doc.for_employee}",
            f"Time Logs:",
        ]
        for log in doc.get("time_logs", []):
            lines.append(f"  - From: {log.from_time} | To: {log.to_time} | Hours: {log.time_in_mins / 60:.2f}")
        return "\n".join(lines)

    # -----------------------------
    # BUYING
    # -----------------------------
    if doc.doctype == "Supplier":
        return f"Supplier: {doc.supplier_name} | Group: {doc.supplier_group} | Type: {doc.supplier_type}"

    if doc.doctype == "Purchase Order":
        lines = [
            f"Purchase Order: {doc.name}",
            f"Supplier: {doc.get('supplier')} | Status: {doc.get('status')}",
            f"Date: {doc.get('transaction_date')} | Company: {doc.get('company')}",
            "Items:",
        ]
        for d in doc.get("items", []):
            lines.append(f"  - {d.item_code} | {d.item_name} | Qty: {d.qty} | Rate: {d.rate}")
        return "\n".join(lines)

    if doc.doctype == "Purchase Receipt":
        lines = [
            f"Purchase Receipt: {doc.name}",
            f"Supplier: {doc.supplier} | Date: {doc.posting_date}",
            "Items:",
        ]
        for d in doc.get("items", []):
            lines.append(f"  - {d.item_code} | Received: {d.received_qty} | Rate: {d.rate}")
        return "\n".join(lines)

    if doc.doctype == "Purchase Invoice":
        lines = [
            f"Purchase Invoice: {doc.name}",
            f"Supplier: {doc.supplier} | Posting Date: {doc.posting_date}",
            f"Status: {doc.status} | Grand Total: {doc.grand_total} {doc.currency}",
        ]
        return "\n".join(lines)

    # -----------------------------
    # SELLING
    # -----------------------------
    if doc.doctype == "Customer":
        return f"Customer: {doc.customer_name} | Group: {doc.customer_group} | Type: {doc.customer_type}"

    if doc.doctype == "Quotation":
        lines = [
            f"Quotation: {doc.name}",
            f"Customer: {doc.customer_name} | Date: {doc.transaction_date}",
            f"Status: {doc.status}",
            "Items:",
        ]
        for d in doc.get("items", []):
            lines.append(f"  - {d.item_code} | Qty: {d.qty} | Rate: {d.rate}")
        return "\n".join(lines)

    if doc.doctype == "Sales Order":
        lines = [
            f"Sales Order: {doc.name}",
            f"Customer: {doc.customer} | Status: {doc.status}",
            f"Date: {doc.transaction_date} | Company: {doc.company}",
            "Items:",
        ]
        for d in doc.get("items", []):
            lines.append(f"  - {d.item_code} | {d.item_name} | Qty: {d.qty} | Rate: {d.rate}")
        return "\n".join(lines)

    if doc.doctype == "Delivery Note":
        lines = [
            f"Delivery Note: {doc.name}",
            f"Customer: {doc.customer} | Date: {doc.posting_date} | Status: {doc.status}",
            "Items:",
        ]
        for d in doc.get("items", []):
            lines.append(f"  - {d.item_code} | Delivered: {d.qty} | Warehouse: {d.warehouse}")
        return "\n".join(lines)

    if doc.doctype == "Sales Invoice":
        lines = [
            f"Sales Invoice: {doc.name}",
            f"Customer: {doc.customer} | Date: {doc.posting_date}",
            f"Status: {doc.status} | Total: {doc.grand_total} {doc.currency}",
        ]
        return "\n".join(lines)

    # -----------------------------
    # FALLBACK
    # -----------------------------
    return f"{label}: {doc.name}"

def _guess_targets(q: str):
    s = (q or "").strip().upper()
    if not s:
        return []

    # --- QUICK PREFIX GUESSING ---
    if s.startswith("MR-"):  return [("Material Request", "Material Request")]
    if s.startswith("PO-"):  return [("Purchase Order", "Purchase Order")]
    if s.startswith("PR-"):  return [("Purchase Receipt", "Purchase Receipt")]
    if s.startswith("PINV-") or s.startswith("PI-"): return [("Purchase Invoice", "Purchase Invoice")]
    if s.startswith("SO-"):  return [("Sales Order", "Sales Order")]
    if s.startswith("SINV-") or s.startswith("SI-"): return [("Sales Invoice", "Sales Invoice")]
    if s.startswith("DN-"):  return [("Delivery Note", "Delivery Note")]
    if s.startswith("QTN-"): return [("Quotation", "Quotation")]
    if s.startswith("STE-") or s.startswith("SE-"):  return [("Stock Entry", "Stock Entry")]
    if s.startswith("SR-"):  return [("Stock Reconciliation", "Stock Reconciliation")]
    if s.startswith("BOM-"): return [("BOM", "BOM")]
    if s.startswith("WO-") or s.startswith("WORK-"): return [("Work Order", "Work Order")]
    if s.startswith("JC-"):  return [("Job Card", "Job Card")]

    # --- GENERIC FALLBACK ORDER (broad search) ---
    return [
        ("Item", "Item"),
        ("Warehouse", "Warehouse"),
        ("Customer", "Customer"),
        ("Supplier", "Supplier"),
        ("Material Request", "Material Request"),
        ("Purchase Order", "Purchase Order"),
        ("Purchase Receipt", "Purchase Receipt"),
        ("Purchase Invoice", "Purchase Invoice"),
        ("Sales Order", "Sales Order"),
        ("Sales Invoice", "Sales Invoice"),
        ("Delivery Note", "Delivery Note"),
        ("BOM", "BOM"),
        ("Work Order", "Work Order"),
        ("Job Card", "Job Card"),
        ("Operation", "Operation"),
        ("Workstation", "Workstation"),
    ]


def _search_docs(doctype, q):
    like = f"%{q}%"
    names = frappe.get_all(doctype, filters=[["name", "like", like]], pluck="name", limit=5)

    # Special fields for key doctypes
    if doctype == "Item":
        names += frappe.get_all("Item", filters=[["item_code", "like", like]], pluck="name", limit=5)
    elif doctype == "Warehouse":
        names += frappe.get_all("Warehouse", filters=[["warehouse_name", "like", like]], pluck="name", limit=5)
    elif doctype == "Customer":
        names += frappe.get_all("Customer", filters=[["customer_name", "like", like]], pluck="name", limit=5)
    elif doctype == "Supplier":
        names += frappe.get_all("Supplier", filters=[["supplier_name", "like", like]], pluck="name", limit=5)

    # Remove duplicates
    return list(dict.fromkeys(names))[:5]


def _load_and_format(doctype, name):
    # Enforce normal permissions; raises if user cannot read
    if not frappe.has_permission(doctype, "read", doc=name):
        frappe.throw(_("Not permitted to read {0} {1}").format(doctype, name), frappe.PermissionError)

    # Pull a reasonably complete doc
    doc = frappe.get_doc(doctype, name)
    doc.load_from_db()  # ensure children pulled
    return _format_row(doctype, doc)
def _get_item_stock_summary(item_code: str):
    """Return warehouse-wise stock balance for a given Item."""
    # Ensure item exists
    if not frappe.db.exists("Item", item_code):
        return [f"Item '{item_code}' not found in the system."]

    # Fetch warehouse-wise stock balances
    stock_data = frappe.db.sql(
        """
        SELECT
            bin.warehouse,
            bin.actual_qty,
            bin.reserved_qty,
            bin.ordered_qty,
            bin.projected_qty
        FROM `tabBin` bin
        WHERE bin.item_code = %s
        ORDER BY bin.warehouse
        """,
        (item_code,),
        as_dict=True
    )

    if not stock_data:
        return [f"No stock records found for Item '{item_code}' in any warehouse."]

    lines = [f"Stock Summary for Item: {item_code}", ""]
    for row in stock_data:
        lines.append(
            f"🏢 {row.warehouse}: "
            f"Actual {row.actual_qty:.2f}, "
            f"Reserved {row.reserved_qty:.2f}, "
            f"Ordered {row.ordered_qty:.2f}, "
            f"Projected {row.projected_qty:.2f}"
        )
    return lines
@frappe.whitelist(allow_guest=True)
def chat_query(q: str):
    """
    Enhanced chat query:
    - Handles greetings & small talk
    - Handles 'tell me about ...' general queries
    - Handles help and ERPNext document lookups
    """
    try:
        q = (q or "").strip().lower()
        if not q:
            return {"ok": False, "error": "Empty query."}

        # --------------------------------
        # BASIC GREETINGS & SMALL TALK
        # --------------------------------
        greetings = {
            "hi": "👋 Hi there! How can I help you today?",
            "hello": "👋 Hello! What would you like to know?",
            "hey": "Hey! 😊 Need help finding something?",
            "good morning": "☀️ Good morning! Hope your day is great!",
            "good afternoon": "🌞 Good afternoon! How can I assist you?",
            "good evening": "🌇 Good evening! How’s everything going?",
            "how are you": "I’m just a bot 🤖 but I’m doing great! How about you?",
            "thank you": "You’re welcome! 😊",
            "thanks": "Anytime! 🙏",
        }

        for k, v in greetings.items():
            if q == k or q.startswith(k):
                return {"ok": True, "answers": [v]}

        # --------------------------------
        # "TELL ME ABOUT" INFORMATIONAL QUERIES
        # --------------------------------
        if q.startswith("tell me about"):
            topic = q.replace("tell me about", "").strip()

            info_responses = {
                "isro": (
                    "🛰️ **ISRO (Indian Space Research Organisation)**\n"
                    "ISRO is India’s national space agency, founded in 1969. "
                    "It designs, launches, and manages satellites and rockets for communication, "
                    "earth observation, navigation, and scientific exploration. "
                    "Headquarters: Bengaluru, India."
                ),
                "ursc": (
                    "🏢 **URSC (U R Rao Satellite Centre)**\n"
                    "URSC, part of ISRO, is the main center for designing and building satellites. "
                    "It develops satellites for communication, remote sensing, meteorology, and interplanetary missions. "
                    "Located in Bengaluru, Karnataka."
                ),
                "nasa": (
                    "🚀 **NASA (National Aeronautics and Space Administration)**\n"
                    "NASA is the United States’ civil space agency, responsible for space exploration, "
                    "aeronautics, and scientific research. Founded in 1958 and headquartered in Washington, D.C."
                ),
                "drdo": (
                    "🧪 **DRDO (Defence Research and Development Organisation)**\n"
                    "DRDO is India’s defense R&D organization. It develops defense systems, missiles, "
                    "radars, and technologies for the Indian Armed Forces."
                ),
            }

            if topic in info_responses:
                return {"ok": True, "answers": [info_responses[topic]]}
            else:
                return {
                    "ok": True,
                    "answers": [
                        f"🤔 I don’t have specific info about *{topic.title()}*, "
                        "but I can tell you about ISRO, URSC, DRDO, or NASA."
                    ],
                }

        # --------------------------------
        # HELP COMMAND
        # --------------------------------
        if q in {"help", "?", "commands", "usage"}:
            help_text = [
                "🤖 **Chat Assistant Help**",
                "",
                "You can ask about ERPNext documents or use commands like:",
                "",
                "📦 **Inventory & Stock**",
                "- `ITEM-0001` → Show item details and stock summary",
                "- `item list`, `component list`, or `part list` → Show recent items",
                "- `warehouse list` → Show list of warehouses",
                "",
                "🏭 **Manufacturing**",
                "- `BOM-001`, `WO-0001` → BOM or Work Order details",
                "- `work order list` → List recent Work Orders",
                "",
                "🛒 **Buying / Selling**",
                "- `supplier list`, `customer list` → Quick master data lists",
                "- `PO-0003`, `SO-0007` → View Purchase or Sales Orders",
                "",
                "💬 **Chat & Info**",
                "- `hi`, `hello`, `how are you` → Friendly conversation",
                "- `tell me about isro` → Learn about ISRO, URSC, etc.",
                "",
                "✨ **Tip:** You can also search by part of a name or code.",
            ]
            return {"ok": True, "answers": ["\n".join(help_text)]}

        # --------------------------------
        # LIST COMMANDS
        # --------------------------------
        if any(word in q for word in ["item list", "component list", "part list"]):
            return {"ok": True, "answers": [_get_item_list()]}

        if "warehouse" in q and "list" in q:
            return {"ok": True, "answers": [_get_warehouse_list()]}

        if "supplier" in q and "list" in q:
            return {"ok": True, "answers": [_get_supplier_list()]}

        if "customer" in q and "list" in q:
            return {"ok": True, "answers": [_get_customer_list()]}

        # --------------------------------
        # ITEM STOCK QUICK LOOKUP
        # --------------------------------
        if frappe.db.exists("Item", q.upper()):
            lines = _get_item_stock_summary(q.upper())
            return {"ok": True, "answers": ["\n".join(lines)]}

        # --------------------------------
        # NORMAL ERP SEARCH
        # --------------------------------
        targets = _guess_targets(q)
        answers = []
        tried = set()

        for _label, dt in targets:
            if dt in tried:
                continue
            tried.add(dt)
            if frappe.db.exists(dt, q.upper()):
                answers.append(_load_and_format(dt, q.upper()))
                return {"ok": True, "answers": answers}

        for _label, dt in targets:
            for name in _search_docs(dt, q):
                try:
                    answers.append(_load_and_format(dt, name))
                except frappe.PermissionError:
                    continue
            if answers:
                break

        if not answers:
            return {"ok": True, "answers": [f"No results found for: {q}"]}

        return {"ok": True, "answers": answers[:5]}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "chat_assistant.chat_query")
        return {"ok": False, "error": str(e)}

