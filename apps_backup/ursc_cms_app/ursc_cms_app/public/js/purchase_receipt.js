frappe.ui.form.on("Purchase Receipt", {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__("Get Items + Supplier Invoice No"), function() {
                frappe.call({
                    method: "ursc_cms_app.api.get_purchase_invoice_details",
                    args: {
                        purchase_invoice: frm.doc.purchase_invoice
                    },
                    callback: function(r) {
                        if (r.message) {
                            $.each(r.message.items, function(i, d) {
                                let child = frm.add_child("items");
                                frappe.model.set_value(child.doctype, child.name, "item_code", d.item_code);
                                frappe.model.set_value(child.doctype, child.name, "qty", d.qty);
                                frappe.model.set_value(child.doctype, child.name, "rate", d.rate);
                                frappe.model.set_value(child.doctype, child.name, "amount", d.amount);
                                frappe.model.set_value(child.doctype, child.name, "custom_srv_part_number", d.custom_srv_part_number);
                            });
                            frm.refresh_field("items");
                        }
                    }
                });
            }, __("Get Items From"));
        }
    }
});*/
