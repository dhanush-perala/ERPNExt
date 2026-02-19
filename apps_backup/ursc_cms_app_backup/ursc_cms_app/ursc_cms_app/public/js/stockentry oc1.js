/*console.log("ursc_cms_app: stock_entry_custom.js loaded ✅");

// ===========================================================
// 🔹 MDB HELPERS (linked to item_code)
// ===========================================================
function make_mdb(srv, qual) {
  if (srv && qual) return `${srv}-${qual}`;
  return srv || qual || "";
}

function update_mdb(frm, cdt, cdn) {
  const row = locals[cdt][cdn];
  frappe.model.set_value(
    cdt,
    cdn,
    "custom_mdb_part_no",
    make_mdb(row.custom_srv_number, row.custom_quality_save)
  );
}

function apply_srv_number_options_to_row(frm, rowname, values) {
  const opts = ["", ...values].join("\n");
  const grid_row = frm.fields_dict.items.grid.get_row(rowname);

  if (grid_row?.grid_form?.fields_dict.custom_srv_number) {
    let fld = grid_row.grid_form.fields_dict.custom_srv_number;
    fld.df.options = opts;
    fld.refresh();
  }

  frm.fields_dict.items.grid.update_docfield_property(
    "custom_srv_number",
    "options",
    opts
  );
}

function load_basic_mdb_options_for_row(frm, cdt, cdn) {
  const row = locals[cdt][cdn];
  if (!row?.item_code) return;

  frappe.call({
    method: "ursc_cms_app.api.get_basic_mdb_options",
    args: { item_code_or_group: row.item_code },
    callback: function (r) {
      if (!r.message || !Array.isArray(r.message)) return;

      apply_srv_number_options_to_row(frm, row.name, r.message);

      if (r.message.length === 1) {
        frappe.model.set_value(cdt, cdn, "custom_srv_number", r.message[0]);
      }
      frm.refresh_field("items");
    },
  });
}

function load_basic_mdb_options_for_all_rows(frm) {
  (frm.doc.items || []).forEach((d) => {
    if (d.item_code) load_basic_mdb_options_for_row(frm, d.doctype, d.name);
  });
}

// ===========================================================
// 🔹 WAREHOUSE HELPERS
// ===========================================================
function ensureMaps(frm) {
  frm._whMaps = frm._whMaps || { src: {}, tgt: {} };
}

// ===========================================================
// 🔹 CHILD TABLE EVENTS
// ===========================================================
frappe.ui.form.on("Stock Entry Detail", {
  // --- Item code (only update options, no manual restore needed) ---
  item_code(frm, cdt, cdn) {
    load_basic_mdb_options_for_row(frm, cdt, cdn);
    update_mdb(frm, cdt, cdn);
  },

  // --- Update MDB part no ---
  custom_srv_number(frm, cdt, cdn) {
    update_mdb(frm, cdt, cdn);
  },
  custom_quality_save(frm, cdt, cdn) {
    update_mdb(frm, cdt, cdn);
  },

  // --- Source parent → refresh child options ---
  custom_source_parent_warehouse(frm, cdt, cdn) {
    ensureMaps(frm);
    const row = locals[cdt][cdn];
    if (!row.custom_source_parent_warehouse) return;

    frappe.call({
      method: "ursc_cms_app.api.get_child_warehouses",
      args: { parent: row.custom_source_parent_warehouse },
      callback(r) {
        const list = r.message || [];
        const labels = ["", ...list.map((x) => x.label)];

        const map = {};
        list.forEach((x) => {
          map[x.label] = x.name;
        });
        frm._whMaps.src[row.name] = map;

        const grid_row = frm.fields_dict.items.grid.get_row(row.name);
        if (grid_row?.grid_form?.fields_dict.custom_warehouse_s_program) {
          let fld = grid_row.grid_form.fields_dict.custom_warehouse_s_program;
          fld.df.options = labels.join("\n");
          fld.refresh();
        }

        if (
          row.custom_source_parent_warehouse !==
          frm._last_src_parent?.[row.name]
        ) {
          frappe.model.set_value(cdt, cdn, "custom_warehouse_s_program", "");
          frappe.model.set_value(cdt, cdn, "s_warehouse", "");
          frappe.model.set_value(cdt, cdn, "custom_sprogram_save", "");
        }
        frm._last_src_parent = frm._last_src_parent || {};
        frm._last_src_parent[row.name] = row.custom_source_parent_warehouse;
      },
    });
  },

  // --- Target parent → refresh child options ---
  custom_target_parent_warhouse(frm, cdt, cdn) {
    ensureMaps(frm);
    const row = locals[cdt][cdn];
    if (!row.custom_target_parent_warhouse) return;

    frappe.call({
      method: "ursc_cms_app.api.get_child_warehouses",
      args: { parent: row.custom_target_parent_warhouse },
      callback(r) {
        const list = r.message || [];
        const labels = ["", ...list.map((x) => x.label)];

        const map = {};
        list.forEach((x) => {
          map[x.label] = x.name;
        });
        frm._whMaps.tgt[row.name] = map;

        const grid_row = frm.fields_dict.items.grid.get_row(row.name);
        if (grid_row?.grid_form?.fields_dict.custom_target_stock_select) {
          let fld = grid_row.grid_form.fields_dict.custom_target_stock_select;
          fld.df.options = labels.join("\n");
          fld.refresh();
        }

        if (
          row.custom_target_parent_warhouse !==
          frm._last_tgt_parent?.[row.name]
        ) {
          frappe.model.set_value(cdt, cdn, "custom_target_stock_select", "");
          frappe.model.set_value(cdt, cdn, "t_warehouse", "");
          frappe.model.set_value(cdt, cdn, "custom_tprogram_save", "");
        }
        frm._last_tgt_parent = frm._last_tgt_parent || {};
        frm._last_tgt_parent[row.name] = row.custom_target_parent_warhouse;
      },
    });
  },

  // --- Sync selects into ERPNext warehouses + save fields ---
  custom_warehouse_s_program(frm, cdt, cdn) {
    ensureMaps(frm);
    const row = locals[cdt][cdn];
    const label = row.custom_warehouse_s_program;
    const name = frm._whMaps?.src?.[row.name]?.[label] || label;
    if (label) {
      frappe.model.set_value(cdt, cdn, "s_warehouse", name);
      frappe.model.set_value(cdt, cdn, "custom_sprogram_save", label);
    }
  },

  custom_target_stock_select(frm, cdt, cdn) {
    ensureMaps(frm);
    const row = locals[cdt][cdn];
    const label = row.custom_target_stock_select;
    const name = frm._whMaps?.tgt?.[row.name]?.[label] || label;
    if (label) {
      frappe.model.set_value(cdt, cdn, "t_warehouse", name);
      frappe.model.set_value(cdt, cdn, "custom_tprogram_save", label);
    }
  },
});

// ===========================================================
// 🔹 PARENT FORM EVENTS
// ===========================================================
frappe.ui.form.on("Stock Entry", {
  onload(frm) {
    load_basic_mdb_options_for_all_rows(frm);
    (frm.doc.items || []).forEach((d) =>
      update_mdb(frm, d.doctype, d.name)
    );
  },
  refresh(frm) {
    load_basic_mdb_options_for_all_rows(frm);
    (frm.doc.items || []).forEach((d) =>
      update_mdb(frm, d.doctype, d.name)
    );

    if (frm.doc.docstatus === 0) {
      frm.add_custom_button(
        __("Purchase Receipt"),
        function () {
          erpnext.utils.map_current_doc({
            method: "ursc_cms_app.api.make_stock_entry_with_srv",
            source_doctype: "Purchase Receipt",
            target: frm,
            setters: { supplier: frm.doc.supplier || undefined },
            get_query_filters: { docstatus: 1 },
          });
        },
        __("Get Items From")
      );
    }
  },
  items_on_form_rendered(frm) {
    setTimeout(() => {
      load_basic_mdb_options_for_all_rows(frm);
      (frm.doc.items || []).forEach((d) =>
        update_mdb(frm, d.doctype, d.name)
      );
    }, 120);
  },
  items_add(frm, cdt, cdn) {
    load_basic_mdb_options_for_row(frm, cdt, cdn);
    update_mdb(frm, cdt, cdn);
  },
});
(function () {
  const PROTECTED = new Set([
    "custom_srv_number",
    "custom_warehouse_s_program",
    "custom_target_stock_select",
    "s_warehouse",
    "t_warehouse",
  ]);

  // Keep original set_value
  const _orig_set_value = frappe.model.set_value;

  // A short-lived guard enabled by our item_code handler
  window.__ursc_block_blanks_once__ = false;

  frappe.model.set_value = function (doctype, name, fieldname, value, ...rest) {
    if (window.__ursc_block_blanks_once__ && PROTECTED.has(fieldname)) {
      const row = locals[doctype] && locals[doctype][name];
      const already = row && row[fieldname];

      // If ERPNext tries to blank a field that already had a value, skip it
      if ((value === "" || value === null || typeof value === "undefined") && already) {
        console.log("⛔ blocked blanking:", fieldname, "keeping:", already);
        return Promise.resolve(); // no-op
      }
    }
    return _orig_set_value.apply(this, arguments);
  };
})();
// --- Reapply after row refresh (once only) ---
frappe.ui.form.on("Stock Entry", {
  items_on_form_rendered(frm) {
    setTimeout(() => {
      (frm.doc.items || []).forEach(d => {
        // Reapply MDB options
        if (d.item_code) {
          load_basic_mdb_options_for_row(frm, d.doctype, d.name);
        }
        // Reapply warehouse dropdowns
        if (d.custom_source_parent_warehouse) {
          frm.trigger("custom_source_parent_warehouse", d.doctype, d.name);
        }
        if (d.custom_target_parent_warhouse) {
          frm.trigger("custom_target_parent_warhouse", d.doctype, d.name);
        }
        // Always rebuild MDB part number
        update_mdb(frm, d.doctype, d.name);
      });
    }, 200);
  }
});
*/
//changed on oct 1 and which do not remove selectable options to the custom selections
console.log("ursc_cms_app: stock_entry_custom.js loaded ✅");

// ===========================================================
// 🔹 MDB HELPERS (linked to item_code)
// ===========================================================
function make_mdb(srv, qual) {
  if (srv && qual) return `${srv}-${qual}`;
  return srv || qual || "";
}

function update_mdb(frm, cdt, cdn) {
  const row = locals[cdt][cdn];
  frappe.model.set_value(cdt, cdn, "custom_mdb_part_no", make_mdb(row.custom_srv_number, row.custom_quality_save));
}

// Set options only on the open row field + cache them
function set_row_select_options(frm, rowname, fieldname, values) {
  const optsStr = ["", ...values].join("\n");
  const grid_row = frm.fields_dict.items.grid.get_row(rowname);
  const fld = grid_row?.grid_form?.fields_dict?.[fieldname];
  if (fld && fld.df.options !== optsStr) {
    fld.df.options = optsStr;
    fld.refresh();
  }
  const row = locals["Stock Entry Detail"]?.[rowname];
  if (row) row[`__opts_${fieldname}`] = optsStr; // cache
}

function load_basic_mdb_options_for_row(frm, cdt, cdn) {
  const row = locals[cdt][cdn];
  if (!row?.item_code) return;

  frappe.call({
    method: "ursc_cms_app.api.get_basic_mdb_options",
    args: { item_code_or_group: row.item_code },
    callback: function (r) {
      const arr = Array.isArray(r.message) ? r.message : [];
      set_row_select_options(frm, row.name, "custom_srv_number", arr);
      if (!row.custom_srv_number && arr.length === 1) {
        frappe.model.set_value(cdt, cdn, "custom_srv_number", arr[0]);
      }
    },
  });
}

function load_basic_mdb_options_for_all_rows(frm) {
  (frm.doc.items || []).forEach(d => {
    if (d.item_code) load_basic_mdb_options_for_row(frm, d.doctype, d.name);
  });
}

// ===========================================================
// 🔹 WAREHOUSE HELPERS
// ===========================================================
function ensureMaps(frm) {
  frm._whMaps = frm._whMaps || { src: {}, tgt: {} };
}

function safe_set_value(frm, cdt, cdn, fieldname, value) {
  window.__ursc_block_blanks_once__ = true;
  return frappe.model.set_value(cdt, cdn, fieldname, value).finally(() => {
    window.__ursc_block_blanks_once__ = false;
  });
}

function reload_child_wh_options(frm, cdt, cdn, parent_field, target_field, save_field, mapKey) {
  const row = locals[cdt][cdn];
  if (!row[parent_field]) return;

  frappe.call({
    method: "ursc_cms_app.api.get_child_warehouses",
    args: { parent: row[parent_field] },
    callback(r) {
      const list = r.message || [];
      const labels = ["", ...list.map(x => x.label)];
      const optsStr = labels.join("\n");

      // build map label → name
      ensureMaps(frm);
      frm._whMaps[mapKey][row.name] = {};
      list.forEach(x => (frm._whMaps[mapKey][row.name][x.label] = x.name));

      set_row_select_options(frm, row.name, target_field, labels.slice(1));

      const lastKey = `__last_${mapKey}_parent`;
      frm[lastKey] = frm[lastKey] || {};
      const parentChanged = row[parent_field] !== frm[lastKey][row.name];

      if (parentChanged) {
        const current = row[target_field] || "";
        const stillExists = labels.includes(current);
        if (!stillExists) {
          safe_set_value(frm, cdt, cdn, target_field, "");
          safe_set_value(frm, cdt, cdn, save_field, "");
          if (mapKey === "src") safe_set_value(frm, cdt, cdn, "s_warehouse", "");
          if (mapKey === "tgt") safe_set_value(frm, cdt, cdn, "t_warehouse", "");
        }
        frm[lastKey][row.name] = row[parent_field];
      }
    },
  });
}
/*
// ===========================================================
// 🔹 CHILD TABLE EVENTS
// ===========================================================
frappe.ui.form.on("Stock Entry Detail", {
  item_code(frm, cdt, cdn) {
    load_basic_mdb_options_for_row(frm, cdt, cdn);
    update_mdb(frm, cdt, cdn);

    const row = locals[cdt][cdn];
    if (row.custom_source_parent_warehouse) {
      reload_child_wh_options(frm, cdt, cdn, "custom_source_parent_warehouse", "custom_warehouse_s_program", "custom_sprogram_save", "src");
    }
    if (row.custom_target_parent_warhouse) {
      reload_child_wh_options(frm, cdt, cdn, "custom_target_parent_warhouse", "custom_target_stock_select", "custom_tprogram_save", "tgt");
    }
  },

  custom_srv_number(frm, cdt, cdn) {
    update_mdb(frm, cdt, cdn);
  },
  custom_quality_save(frm, cdt, cdn) {
    update_mdb(frm, cdt, cdn);
  },

  custom_source_parent_warehouse(frm, cdt, cdn) {
    reload_child_wh_options(frm, cdt, cdn, "custom_source_parent_warehouse", "custom_warehouse_s_program", "custom_sprogram_save", "src");
  },

  custom_target_parent_warhouse(frm, cdt, cdn) {
    reload_child_wh_options(frm, cdt, cdn, "custom_target_parent_warhouse", "custom_target_stock_select", "custom_tprogram_save", "tgt");
  },

  custom_warehouse_s_program(frm, cdt, cdn) {
    ensureMaps(frm);
    const row = locals[cdt][cdn];
    const lbl = row.custom_warehouse_s_program;
    const name = frm._whMaps?.src?.[row.name]?.[lbl] || lbl;
    if (lbl) {
      safe_set_value(frm, cdt, cdn, "s_warehouse", name);
      safe_set_value(frm, cdt, cdn, "custom_sprogram_save", lbl);
    }
  },

  custom_target_stock_select(frm, cdt, cdn) {
    ensureMaps(frm);
    const row = locals[cdt][cdn];
    const lbl = row.custom_target_stock_select;
    const name = frm._whMaps?.tgt?.[row.name]?.[lbl] || lbl;
    if (lbl) {
      safe_set_value(frm, cdt, cdn, "t_warehouse", name);
      safe_set_value(frm, cdt, cdn, "custom_tprogram_save", lbl);
    }
  },
});
*/

frappe.ui.form.on("Stock Entry Detail", {
  // --- Item code (only update options, no manual restore needed) ---
  item_code(frm, cdt, cdn) {
    load_basic_mdb_options_for_row(frm, cdt, cdn);
    update_mdb(frm, cdt, cdn);

    const row = locals[cdt][cdn];
    if (row.custom_source_parent_warehouse) {
      reload_child_wh_options(frm, cdt, cdn,
        "custom_source_parent_warehouse", "custom_warehouse_s_program", "custom_sprogram_save", "src");
    }
    if (row.custom_target_parent_warhouse) {
      reload_child_wh_options(frm, cdt, cdn,
        "custom_target_parent_warhouse", "custom_target_stock_select", "custom_tprogram_save", "tgt");
    }
  },

  custom_srv_number(frm, cdt, cdn) {
    update_mdb(frm, cdt, cdn);
  },
  custom_quality_save(frm, cdt, cdn) {
    update_mdb(frm, cdt, cdn);
  },

  custom_source_parent_warehouse(frm, cdt, cdn) {
    reload_child_wh_options(frm, cdt, cdn,
      "custom_source_parent_warehouse", "custom_warehouse_s_program", "custom_sprogram_save", "src");
  },

  custom_target_parent_warhouse(frm, cdt, cdn) {
    reload_child_wh_options(frm, cdt, cdn,
      "custom_target_parent_warhouse", "custom_target_stock_select", "custom_tprogram_save", "tgt");
  },

  custom_warehouse_s_program(frm, cdt, cdn) {
    ensureMaps(frm);
    const row = locals[cdt][cdn];
    const lbl = row.custom_warehouse_s_program;
    const name = frm._whMaps?.src?.[row.name]?.[lbl] || lbl;
    if (lbl) {
      safe_set_value(frm, cdt, cdn, "s_warehouse", name);
      safe_set_value(frm, cdt, cdn, "custom_sprogram_save", lbl);
    }
  },

  custom_target_stock_select(frm, cdt, cdn) {
    ensureMaps(frm);
    const row = locals[cdt][cdn];
    const lbl = row.custom_target_stock_select;
    const name = frm._whMaps?.tgt?.[row.name]?.[lbl] || lbl;
    if (lbl) {
      safe_set_value(frm, cdt, cdn, "t_warehouse", name);
      safe_set_value(frm, cdt, cdn, "custom_tprogram_save", lbl);
    }
  },

  // --- ✅ Expiry Date Validation ---
  custom_exp_date(frm, cdt, cdn) {
    const row = locals[cdt][cdn];
    if (!row.custom_exp_date) return;

    const exp_date = frappe.datetime.str_to_obj(row.custom_exp_date);
    const today = frappe.datetime.str_to_obj(frappe.datetime.get_today());
    const max_date = frappe.datetime.add_years(today, 5);

    if (exp_date > max_date) {
      frappe.model.set_value(cdt, cdn, "custom_exp_date", "");
      frappe.msgprint({
        message: __("Expiry Date cannot be more than 5 years from today."),
        indicator: "red"
      });
    }
  },
  //cs validation
  form_render: function(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    let grid_row = frm.fields_dict.items.grid.get_row(row.name);
    if (grid_row?.grid_form?.fields_dict?.custom_exp_date) {
      let field = grid_row.grid_form.fields_dict.custom_exp_date;
      field.df.max_date = frappe.datetime.add_years(frappe.datetime.get_today(), 5);
      field.refresh();
    }
  },

  custom_exp_date: function(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    if (!row.custom_exp_date) return;

    const exp = frappe.datetime.str_to_obj(row.custom_exp_date);
    const limit = frappe.datetime.add_years(frappe.datetime.get_today(), 5);

    if (exp > limit) {
      frappe.model.set_value(cdt, cdn, "custom_exp_date", "");
    }
  }
});

// ===========================================================
// 🔹 PARENT FORM EVENTS
// ===========================================================
frappe.ui.form.on("Stock Entry", {
  onload(frm) {
    load_basic_mdb_options_for_all_rows(frm);
    (frm.doc.items || []).forEach(d => update_mdb(frm, d.doctype, d.name));
  },
  refresh(frm) {
    load_basic_mdb_options_for_all_rows(frm);
    (frm.doc.items || []).forEach(d => update_mdb(frm, d.doctype, d.name));

    if (frm.doc.docstatus === 0) {
      frm.add_custom_button(__("Purchase Receipt"), function () {
        erpnext.utils.map_current_doc({
          method: "ursc_cms_app.api.make_stock_entry_with_srv",
          source_doctype: "Purchase Receipt",
          target: frm,
          setters: { supplier: frm.doc.supplier || undefined },
          get_query_filters: { docstatus: 1 },
        });
      }, __("Get Items From"));
    }
  },

  items_on_form_rendered(frm) {
    setTimeout(() => {
      const grid = frm.fields_dict.items.grid;
      const open = grid?.grid_rows?.find(r => r?.grid_form?.visible);
      if (!open) return;
      const row = open.doc;

      ["custom_srv_number", "custom_warehouse_s_program", "custom_target_stock_select"].forEach(f => {
        const cached = row[`__opts_${f}`];
        const fld = open.grid_form?.fields_dict?.[f];
        if (cached && fld && fld.df.options !== cached) {
          fld.df.options = cached;
          fld.refresh();
        }
      });
    }, 80);
  },

  items_add(frm, cdt, cdn) {
    load_basic_mdb_options_for_row(frm, cdt, cdn);
    update_mdb(frm, cdt, cdn);
  },
});

// ===========================================================
// 🔹 PROTECT AGAINST BLANKING
// ===========================================================
(function () {
  const PROTECTED = new Set(["custom_srv_number","custom_warehouse_s_program","custom_target_stock_select","s_warehouse","t_warehouse"]);
  const _orig_set_value = frappe.model.set_value;
  window.__ursc_block_blanks_once__ = false;

  frappe.model.set_value = function (doctype, name, fieldname, value, ...rest) {
    if (window.__ursc_block_blanks_once__ && PROTECTED.has(fieldname)) {
      const row = locals[doctype]?.[name];
      const already = row && row[fieldname];
      if ((value === "" || value == null) && already) {
        console.log("⛔ blocked blanking:", fieldname, "keeping:", already);
        return Promise.resolve();
      }
    }
    return _orig_set_value.apply(this, arguments);
  };
})();
