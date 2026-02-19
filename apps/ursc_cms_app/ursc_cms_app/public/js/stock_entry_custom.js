console.log("✅ ursc_cms_app: stock_entry_custom.js loaded safely");

// ===========================================================
// 🔹 Helper: MDB Part No
// ===========================================================
function make_mdb(srv, qual) {
  if (srv && qual) 
    return `${srv}-${qual}`;
return `${srv}-${qual}`;  
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

// ===========================================================
// 🔹 Helper: Set Row Select Options
// ===========================================================
function set_row_select_options(frm, rowname, fieldname, values) {
  const optsStr = ["", ...values].join("\n");
  const grid = frm.fields_dict.items.grid;
  const grid_row = grid.get_row(rowname);
  const row = locals["Stock Entry Detail"]?.[rowname];

  if (row) row[`__opts_${fieldname}`] = optsStr;

  const fld = grid_row?.grid_form?.fields_dict?.[fieldname];
  if (fld) {
    fld.df.options = optsStr;
    fld.refresh();
  }

  const df = grid_row?.docfields?.find((d) => d.fieldname === fieldname);
  if (df) df.options = optsStr;
}

// ===========================================================
// 🔹 Helper: Load MDB Options
// ===========================================================
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
  (frm.doc.items || []).forEach((d) => {
    if (d.item_code) load_basic_mdb_options_for_row(frm, d.doctype, d.name);
  });
}

// ===========================================================
// 🔹 Helper: Warehouse Maps
// ===========================================================
function ensureMaps(frm) {
  frm._whMaps = frm._whMaps || { src: {}, tgt: {} };
}

function safe_set_value(frm, cdt, cdn, fieldname, value) {
  if (value === undefined) return;
  return frappe.model.set_value(cdt, cdn, fieldname, value);
}

function reload_child_wh_options(
  frm,
  cdt,
  cdn,
  parent_field,
  target_field,
  save_field,
  mapKey
) {
  const row = locals[cdt][cdn];
  if (!row[parent_field]) return;

  frappe.call({
    //method: "ursc_cms_app.api.get_child_warehouses",
    args: { parent: row[parent_field] },
    callback(r) {
      const list = r.message || [];
      const labels = ["", ...list.map((x) => x.label)];

      ensureMaps(frm);
      frm._whMaps[mapKey][row.name] = {};
      list.forEach((x) => (frm._whMaps[mapKey][row.name][x.label] = x.name));

      set_row_select_options(frm, row.name, target_field, labels.slice(1));
    },
  });
}

// ===========================================================
// 🔹 CHILD TABLE EVENTS
// ===========================================================
frappe.ui.form.on("Stock Entry Detail", {
  item_code(frm, cdt, cdn) {
    load_basic_mdb_options_for_row(frm, cdt, cdn);
    update_mdb(frm, cdt, cdn);
  },

  custom_srv_number(frm, cdt, cdn) {
    update_mdb(frm, cdt, cdn);
  },

  custom_quality_save(frm, cdt, cdn) {
    update_mdb(frm, cdt, cdn);
  },

  custom_source_parent_warehouse(frm, cdt, cdn) {
    reload_child_wh_options(
      frm,
      cdt,
      cdn,
      "custom_source_parent_warehouse",
      "custom_warehouse_s_program",
      "custom_sprogram_save",
      "src"
    );
  },

  custom_target_parent_warhouse(frm, cdt, cdn) {
    reload_child_wh_options(
      frm,
      cdt,
      cdn,
      "custom_target_parent_warhouse",
      "custom_target_stock_select",
      "custom_tprogram_save",
      "tgt"
    );
  },

  custom_warehouse_s_program(frm, cdt, cdn) {
    ensureMaps(frm);
    const row = locals[cdt][cdn];
    const lbl = row.custom_warehouse_s_program;
    const name = frm._whMaps?.src?.[row.name]?.[lbl] || lbl;
    safe_set_value(frm, cdt, cdn, "s_warehouse", name);
    safe_set_value(frm, cdt, cdn, "custom_sprogram_save", lbl);
  },

  custom_target_stock_select(frm, cdt, cdn) {
    ensureMaps(frm);
    const row = locals[cdt][cdn];
    const lbl = row.custom_target_stock_select;
    const name = frm._whMaps?.tgt?.[row.name]?.[lbl] || lbl;
    safe_set_value(frm, cdt, cdn, "t_warehouse", name);
    safe_set_value(frm, cdt, cdn, "custom_tprogram_save", lbl);
  },
});

// ===========================================================
// 🔹 PARENT FORM EVENTS
// ===========================================================
frappe.ui.form.on("Stock Entry", {
  onload(frm) {
    load_basic_mdb_options_for_all_rows(frm);
    setup_stock_entry_type_field(frm);
  },

  refresh(frm) {
    load_basic_mdb_options_for_all_rows(frm);
    setup_stock_entry_type_field(frm);

    if (frm.doc.docstatus === 0) {
      // Button: Get Items from Purchase Receipt
      frm.add_custom_button(
        __("Purchase Receipt"),
        function () {
          erpnext.utils.map_current_doc({
            method: "ursc_cms_app.api.make_stock_entry_with_srv",
            source_doctype: "Purchase Receipt",
            target: frm,
            setters: { supplier: frm.doc.supplier || undefined },
            get_query_filters: { docstatus: 1 },
            callback: function () {
              frappe.after_ajax(() => {
                setTimeout(() => {
                  (frm.doc.items || []).forEach((d) => {
                    if (d.item_code) {
                      console.log("🔁 Reloading MDB options for:", d.item_code);
                      load_basic_mdb_options_for_row(frm, d.doctype, d.name);
                      update_mdb(frm, d.doctype, d.name);
                    }
                  });
                  frm.refresh_field("items");
                }, 400);
              });
            },
          });
        },
        __("Get Items From")
      );

      // Button: Get Items from Stock Entry
      frm.add_custom_button(
        __("Stock Entry"),
        function () {
          frappe.prompt(
            {
              fieldtype: "Link",
              fieldname: "source_se",
              label: "Source Stock Entry",
              options: "Stock Entry",
              reqd: 1,
            },
            async ({ source_se }) => {
              const r = await frappe.call({
                method: "ursc_cms_app.api.fetch_stock_entry_payload",
                args: { source_name: source_se },
              });
              const payload = r && r.message;
              if (!payload) return;

              const parent = payload.parent || {};
              const items = payload.items || [];

              // Update parent fields
              Object.keys(parent).forEach((k) => {
                if (parent[k] !== null && parent[k] !== undefined) {
                  frm.doc[k] = parent[k];
                }
              });

              // 🔁 Swap warehouse logic:
              // old.to_warehouse -> new.from_warehouse
              // old.custom_linked_warehouse -> new.to_warehouse
              if (parent.to_warehouse) {
                frm.doc.from_warehouse = parent.to_warehouse;
              }

              if (parent.custom_linked_warehouse) {
                frm.doc.to_warehouse = parent.custom_linked_warehouse;
              } else {
                frm.doc.to_warehouse = "";
              }

              // Clear and rebuild child table
              frm.clear_table("items");
              items.forEach((row) => {
                const d = frm.add_child("items");

                // Swap standard warehouses: old t_warehouse -> new s_warehouse
                if (row.t_warehouse) {
                  d.s_warehouse = row.t_warehouse;
                }

                // Map old custom linked warehouse to new target warehouse
                if (row.custom_linked_warehouse) {
                  d.t_warehouse = row.custom_linked_warehouse;
                  d.custom_target_parent_warhouse = row.custom_linked_warehouse;
                }

                // Copy all other fields safely
                Object.keys(row || {}).forEach((k) => {
                  if (
                    row[k] !== null &&
                    row[k] !== undefined &&
                    ![
                      "t_warehouse",
                      "custom_target_parent_warhouse",
                      "custom_target_stock_select",
                      "custom_tprogram_save",
                    ].includes(k)
                  ) {
                    if (k === "s_warehouse" && d.s_warehouse) return;
                    d[k] = row[k];
                  }
                });
              });

              frm.refresh();

              // Reload MDB & warehouses
              frappe.after_ajax(() => {
                setTimeout(() => {
                  (frm.doc.items || []).forEach((d) => {
                    if (d.item_code) {
                      console.log("🔁 Reloading MDB options for:", d.item_code);
                      load_basic_mdb_options_for_row(frm, d.doctype, d.name);
                      update_mdb(frm, d.doctype, d.name);

                      if (d.custom_source_parent_warehouse) {
                        reload_child_wh_options(
                          frm,
                          d.doctype,
                          d.name,
                          "custom_source_parent_warehouse",
                          "custom_warehouse_s_program",
                          "custom_sprogram_save",
                          "src"
                        );
                      }
                    }
                  });
                  frm.refresh_field("items");
                }, 400);
              });
            },
            "Select Stock Entry",
            "Fetch"
          );
        },
        __("Get Items From")
      );
    }
  },

  items_add(frm, cdt, cdn) {
    load_basic_mdb_options_for_row(frm, cdt, cdn);
  },
});

// ===========================================================
// 🔹 Ensure all stock entry types (including custom) are available
// ===========================================================
function setup_stock_entry_type_field(frm) {
  const stock_entry_type_field = frm.fields_dict.stock_entry_type;
  if (!stock_entry_type_field) return;
  stock_entry_type_field.get_query = function () {
    return { filters: {} };
  };
}