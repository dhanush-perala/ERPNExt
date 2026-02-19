/*frappe.ui.form.on("Purchase Receipt", {
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
});
frappe.ui.form.on('Purchase Receipt Item', {
    // Trigger on item_code change
    item_code: function(frm, cdt, cdn) {
        var row = locals[cdt][cdn];
    
        // Ensure both item_code and supplier are selected
        if (row.item_code && frm.doc.supplier) {
            fetch_supplier_part_number(row.item_code, frm.doc.supplier, cdt, cdn);
        }
    },
    
    // Trigger on supplier change
    supplier: function(frm, cdt, cdn) {
        var row = locals[cdt][cdn];
    
        // Ensure both item_code and supplier are selected
        if (row.item_code && frm.doc.supplier) {
            fetch_supplier_part_number(row.item_code, frm.doc.supplier, cdt, cdn);
        }
    }
});

// Function to fetch supplier part number based on item_code and supplier
function fetch_supplier_part_number(item_code, supplier, cdt, cdn) {
    frappe.call({
        method: "ursc_cms_app.api.fetch_supplier_part_number",  // Path to your whitelisted method
        args: {
            item_code: item_code,  // Pass the item_code
            supplier: supplier      // Pass the supplier
        },
        callback: function(response) {
            if (response.message) {
                // Set the supplier part number in the custom field
                frappe.model.set_value(cdt, cdn, 'custom_srv_part_number', response.message);
            } else {
                // Clear the custom field if no part number is found
                frappe.model.set_value(cdt, cdn, 'custom_srv_part_number', '');
                frappe.msgprint(__('No supplier part number found for this item with the selected supplier.'));
            }
        }
    });
}
frappe.ui.form.on('Purchase Receipt', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            // Add custom button to fetch supplier from PO
            frm.add_custom_button(__('Fetch Supplier from PO'), function() {
                // Trigger the function to fetch the supplier from PO
                fetch_supplier_from_po(frm);
            }, __('Get Items From'));
        }
    }
});

// Function to fetch the supplier from the selected PO and set it in the PR
function fetch_supplier_from_po(frm) {
    // Ensure that a PO is selected
    if (!frm.doc.purchase_order) {
        frappe.msgprint(__('Please select a Purchase Order first.'));
        return;
    }

    // Call the server-side method to get the supplier from PO
    frappe.call({
        method: 'ursc_cms_app.api.fetch_supplier_from_po',  // Whitelisted server-side method
        args: {
            purchase_order: frm.doc.purchase_order  // Pass the selected PO name
        },
        callback: function(response) {
            if (response.message) {
                // Set the fetched supplier in the Purchase Receipt (PR)
                frm.set_value('supplier', response.message);  // Set supplier field in PR
                frappe.msgprint(__('Supplier fetched successfully.'));
            } else {
                frappe.msgprint(__('No supplier found for this Purchase Order.'));
            }
        }
    });
}

*/
/*
frappe.ui.form.on('Purchase Receipt', {
    refresh(frm) {
        // Custom button for fetching PO items
        frm.add_custom_button("Get Items from PO", () => {
            frappe.prompt(
                [
                    {
                        fieldtype: "Link",
                        label: "Purchase Order",
                        fieldname: "po_name",
                        options: "Purchase Order",
                        reqd: 1,
                        get_query: () => {
                            return {
                                filters: {
                                    docstatus: 1,           // Only submitted POs
                                    custom_po_flag: 1       // Only active POs
                                }
                            };
                        }
                    }
                ],
                (values) => {
                    // Fetch PO Items using backend method
                    frappe.call({
                        method: "ursc_cms_app.api.get_po_items_for_pr",  // Adjust this with your method
                        args: { po_name: values.po_name },
                        callback: (r) => {
                            if (r.message && r.message.length) {
                                // Clear existing items to avoid duplication
                                frm.clear_table("items");

                                // Add filtered items to the Purchase Receipt
                                r.message.forEach((it) => {
                                    let child = frm.add_child("items");
                                    frappe.model.set_value(child.doctype, child.name, "item_code", it.item_code);
                                    frappe.model.set_value(child.doctype, child.name, "item_name", it.item_name);
                                    frappe.model.set_value(child.doctype, child.name, "description", it.description);
                                    frappe.model.set_value(child.doctype, child.name, "qty", it.qty);
                                    frappe.model.set_value(child.doctype, child.name, "uom", it.uom);
                                    frappe.model.set_value(child.doctype, child.name, "rate", it.rate);
                                    frappe.model.set_value(child.doctype, child.name, "amount", it.amount);
                                    frappe.model.set_value(child.doctype, child.name, "purchase_order_item", it.purchase_order_item); // Ensure this is set
                                    frappe.model.set_value(child.doctype, child.name, "warehouse", it.warehouse);
                                    
                                });

                                frm.refresh_field("items");
                                frappe.show_alert({
                                    message: `Loaded ${r.message.length} items from ${values.po_name}`,
                                    indicator: "green"
                                });
                            } else {
                                frappe.msgprint(`No items found for ${values.po_name}`);
                            }
                        }
                    });
                },
                __("Get Items from PO"),
                __("Fetch")
            );
        });
    }
});
*/
frappe.call({
    method: "ursc_cms_app.api.get_po_items_for_pr",
    args: { po_name: values.po_name },
    callback: (r) => {
        if (r.message && r.message.items && r.message.items.length) {
            // clear existing items
            frm.clear_table("items");

            // add new ones
            r.message.items.forEach((it) => {
                let child = frm.add_child("items");
                frappe.model.set_value(child.doctype, child.name, "item_code", it.item_code);
                frappe.model.set_value(child.doctype, child.name, "item_name", it.item_name);
                frappe.model.set_value(child.doctype, child.name, "description", it.description);
                frappe.model.set_value(child.doctype, child.name, "qty", it.qty);
                frappe.model.set_value(child.doctype, child.name, "uom", it.uom);
                frappe.model.set_value(child.doctype, child.name, "rate", it.rate);
                frappe.model.set_value(child.doctype, child.name, "amount", it.amount);
                frappe.model.set_value(child.doctype, child.name, "warehouse", it.warehouse);
                frappe.model.set_value(child.doctype, child.name, "purchase_order", it.purchase_order);
                frappe.model.set_value(child.doctype, child.name, "purchase_order_item", it.purchase_order_item);
                frappe.model.set_value(child.doctype, child.name, "cost_center", it.cost_center);
                frappe.model.set_value(child.doctype, child.name, "project", it.project);
                frappe.model.set_value(child.doctype, child.name, "item_group", it.item_group);
            });

            frm.refresh_field("items");

            // ✅ set project at parent level if provided
            if (r.message.parent_project) {
                frm.set_value("custom_project_save", r.message.parent_project);
            }

            frappe.show_alert({
                message: `Loaded ${r.message.items.length} active item(s) from ${values.po_name}`,
                indicator: "green"
            });
        } else {
            frappe.msgprint(`No active items found (custom_po_flag = 1) in ${values.po_name}`);
        }
    }
});
