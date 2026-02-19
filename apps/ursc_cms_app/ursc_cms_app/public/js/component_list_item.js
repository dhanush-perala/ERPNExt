// ---------------------------------------------------------------------------
// COMPONENT LIST ITEM - SHOW MDB ITEMS BASED ON ITEM GROUP + CATEGORY
// ---------------------------------------------------------------------------

frappe.ui.form.on('Component List Item', {
    category(frm, cdt, cdn) {
        const row = locals[cdt][cdn];
        maybe_show_mdb_items(frm, row);
    },
    component_type(frm, cdt, cdn) {
        const row = locals[cdt][cdn];
        maybe_show_mdb_items(frm, row);
    }
});

// ---------------------------------------------------------------------------
// Helper: Show MDB Item list when category = "MDB List"
// ---------------------------------------------------------------------------
function maybe_show_mdb_items(frm, row) {
    if (!row.component_type || row.category !== "MDB List") {
        frappe.model.set_value(row.doctype, row.name, "part_no_details",
            `<p class="text-muted">Select category = MDB List and an Item Group.</p>`);
        return;
    }

    frappe.call({
        method: "ursc_cms_app.api.get_items_for_group",
        args: { item_group: row.component_type },
        callback: (r) => {
            const items = r.message || [];
            let html = `
                <div style="max-height:280px;overflow:auto;">
                    <h5 style="color:#007bff;margin:5px 0;">
                        Items in Group: ${frappe.utils.escape_html(row.component_type)}
                    </h5>
                    <table class="table table-bordered table-sm">
                        <thead class="table-light">
                            <tr>
                                <th>Item Code</th>
                                <th>Description</th>
                                <th>Package</th>
                            </tr>
                        </thead><tbody>`;

            if (items.length) {
                items.forEach(i => {
                    const desc = frappe.utils.escape_html(i.description || "");
                    html += `
                        <tr class="selectable-item"
                            data-item="${i.name}"
                            data-desc="${desc}">
                            <td>${i.name}</td>
                            <td>${desc}</td>
                            <td>${frappe.utils.escape_html(frm.doc.pack_code || '')}</td>
                        </tr>`;
                });
            } else {
                html += `<tr><td colspan="3" class="text-center text-muted">
                    No items found for Item Group ${row.component_type}.
                </td></tr>`;
            }

            html += "</tbody></table></div>";

            // Update child’s HTML
            frappe.model.set_value(row.doctype, row.name, "part_no_details", html);

            // Also reflect in parent HTML (if exists)
            if (frm.fields_dict.mdb_preview_html) {
                frm.fields_dict.mdb_preview_html.$wrapper.html(html);
            }

            // Attach click handler
            setTimeout(() => {
                const grid_form = frappe.dom.get_open_grid_form();
                if (!grid_form) return;

                const wrapper = grid_form.fields_dict.part_no_details.$wrapper;
                wrapper.find('.selectable-item').on('click', function () {
                    const item_code = $(this).data('item');
                    const desc = $(this).data('desc');
                    const pack = frm.doc.pack_code || "";

                    frappe.model.set_value(row.doctype, row.name, "part_no", item_code);
                    frappe.model.set_value(row.doctype, row.name, "part_desc", desc);
                    frappe.model.set_value(row.doctype, row.name, "package", pack);

                    wrapper.find('tr').removeClass('table-primary');
                    $(this).addClass('table-primary');
                    frappe.show_alert({ message: `Selected ${item_code}`, indicator: 'green' });
                });
            }, 400);
        }
    });

}
