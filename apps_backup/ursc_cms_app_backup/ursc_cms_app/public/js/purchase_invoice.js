frappe.ui.form.on("Purchase Invoice", {
  refresh(frm) {
    if (frm.doc.docstatus === 1) {
      // Override default "Make → Purchase Receipt"
      frm.add_custom_button(
        __("Purchase Receipt"),
        function () {
          frappe.model.open_mapped_doc({
            method: "ursc_cms_app.api.custom_make_purchase_receipt",
            frm: frm,
          });
        },
        __("Make")
      );
    }
  },
});
