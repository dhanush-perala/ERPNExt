// Copyright (c) 2025, neemus and contributors
// For license information, please see license.txt

// frappe.ui.form.on("SRV ENTRY", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on("SRV ENTRY", {
    po_no: function(frm) {
        if (frm.doc.po_no) {
            frappe.call({
                method: "your_app_name.api.get_po_details",  // update with your app name
                args: {
                    purchase_order: frm.doc.po_no
                },
                callback: function(r) {
                    if (!r.message) return;

                    let po = r.message;

                    // ---- Set Parent Fields ----
                    frm.set_value("po_no", po.po_no);
                    frm.set_value("po_date", po.po_date);
                    frm.set_value("project", po.project);

                    // ---- Clear and Fill Child Table ----
                    frm.clear_table("srv_ent_table"); // replace with your child table fieldname if different
                    (po.items || []).forEach(function(d) {
                        let row = frm.add_child("srv_ent_table");
                        row.srv_part_no = d.srv_part_no;
                        row.ordered_qty = d.ordered_qty;
                        row.u_cost = d.u_cost;
                        // rec_qty and ret_qty left empty for manual entry
                    });

                    frm.refresh_field("srv_ent_table");
                }
            });
        }
    }
});
