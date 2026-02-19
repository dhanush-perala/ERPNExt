console.log("ursc_cms_app: purchase_order_custom.js loaded ✅");

/**
 * Populate custom_select_srv_part_no (Select) dynamically
 */
function refresh_srv_part_options(frm, cdt, cdn) {
  const row = locals[cdt][cdn];
  if (!row.item_code) return;

  frappe.call({
    method: "ursc_cms_app.api.get_srv_parts_options",
    args: {
      item_code: row.item_code,
      supplier: frm.doc.supplier || null
    },
    callback: function(r) {
      if (!r.exc) {
        const options = r.message || [];
        const grid_field = frm.fields_dict.items.grid.get_field("custom_select_srv_part_no");
        if (grid_field) {
          grid_field.df.options = [""].concat(options);
          grid_field.refresh();
        }
      }
    }
  });
}



/**
 * On item_code change:
 *  - auto-fill custom_link_part_no if empty
 *  - refresh SRV part options
 */
function on_item_code_change(frm, cdt, cdn) {
  const row = locals[cdt][cdn];
  if (!row.item_code) return;

  // Always fetch fresh link part no, not only when empty
  frappe.call({
    method: "ursc_cms_app.api.get_linkpart_by_item",
    args: { item_code: row.item_code },
    callback: (r) => {
      if (!r.exc && r.message) {
        frappe.model.set_value(cdt, cdn, "custom_link_part_no", r.message);
      }
    }
  });

  refresh_srv_part_options(frm, cdt, cdn);
}


/**
 * On link part change: restrict item_code by Link Part + refresh SRV part options
 */
function on_link_part_change(frm, cdt, cdn) {
  const row = locals[cdt][cdn];
  if (!row.custom_link_part_no) return;

  const gf = frm.fields_dict.items?.grid?.get_field("item_code");
  if (gf) {
    gf.get_query = () => ({
      query: "ursc_cms_app.api.get_base_parts_by_link",
      filters: { link_part_no: row.custom_link_part_no }
    });
  }

  refresh_srv_part_options(frm, cdt, cdn);
}
function set_srv_options_for_row(frm, cdt, cdn, options) {
  const grid = frm.fields_dict.items?.grid;
  if (!grid) return;

  const gr = grid.grid_rows_by_docname[cdn];
  if (gr && gr.fields_dict && gr.fields_dict.custom_select_srv_part_no) {
    const ctrl = gr.fields_dict.custom_select_srv_part_no;
    ctrl.df.options = [""].concat(options || []);
    ctrl.refresh();

    // Clear invalid selection
    const current = locals[cdt][cdn].custom_select_srv_part_no;
    if (current && !ctrl.df.options.includes(current)) {
      frappe.model.set_value(cdt, cdn, "custom_select_srv_part_no", "");
    }
  }
}
function refresh_srv_for_row(frm, cdt, cdn) {
  const row = locals[cdt][cdn];
  if (!row.item_code) return;

  frappe.call({
    method: "ursc_cms_app.api.get_srv_parts_options",
    args: {
      item_code: row.item_code,
      supplier: frm.doc.supplier || null
    },
    callback(r) {
      if (!r.exc) {
        set_srv_options_for_row(frm, cdt, cdn, r.message || []);
      }
    }
  });
}
/**
 * Form events
 */
frappe.ui.form.on("Purchase Order", {
  onload(frm) {
    (frm.doc.items || []).forEach(d => refresh_srv_part_options(frm, d.doctype, d.name));
  },
  refresh(frm) {
    (frm.doc.items || []).forEach(d => refresh_srv_part_options(frm, d.doctype, d.name));
  },
  items_on_form_rendered(frm) {
    (frm.doc.items || []).forEach(d => refresh_srv_part_options(frm, d.doctype, d.name));
        (frm.doc.items || []).forEach(d => refresh_srv_for_row(frm, d.doctype, d.name));

  },
  supplier(frm) {
    // Re-run SRV part options for all rows when supplier changes
    (frm.doc.items || []).forEach(d => refresh_srv_part_options(frm, d.doctype, d.name));
        (frm.doc.items || []).forEach(d => refresh_srv_for_row(frm, d.doctype, d.name));

  }
});

/**
 * Child table events
 */
frappe.ui.form.on("Purchase Order Item", {
  item_code(frm, cdt, cdn) {
    on_item_code_change(frm, cdt, cdn);
      refresh_srv_for_row(frm, cdt, cdn);
  },
  custom_link_part_no(frm, cdt, cdn) {
    on_link_part_change(frm, cdt, cdn);
  }
});
// apps/your_app/your_app/public/js/purchase_order_custom.js

// Helper: set supplier-aware query on the grid's item_code field
function set_supplier_item_filter(frm) {
  const grid_field = frm.fields_dict.items?.grid?.get_field("item_code");
  if (!grid_field) return;

  grid_field.get_query = function (doc, cdt, cdn) {
    if (!frm.doc.supplier) {
      frappe.msgprint(__("Please select a Supplier first"));
      return false;
    }
    // Call our server method which only returns items linked to this supplier
    return {
      query: "ursc_cms_app.api.item_by_supplier",
      filters: {
        supplier: frm.doc.supplier
      }
    };
  };
}

frappe.ui.form.on("Purchase Order", {
  onload(frm) {
    // bind early so new rows also get the filter
    set_supplier_item_filter(frm);
  },
  refresh(frm) {
    set_supplier_item_filter(frm);
  },
  supplier(frm) {
    // rebind when supplier changes
    set_supplier_item_filter(frm);
  },
  items_on_form_rendered(frm) {
    // ensure filter applies after child rows render
    set_supplier_item_filter(frm);
  },
});

