frappe.ui.form.on("Purchase Order Item", {
  custom_item_group_save(frm, cdt, cdn) {
    const row = locals[cdt][cdn];
    if (!row.custom_item_group_save) return;
 
    console.log("Filtering items by group:", row.custom_item_group_save);
 
    frm.fields_dict.items.grid.get_field("item_code").get_query = function (doc, cdt2, cdn2) {
      return {
        query: "ursc_cms_app.api.get_items_by_group_name",
        filters: {
          custom_item_group_save: row.custom_item_group_save
        }
      };
    };
 
  }
});
 
 