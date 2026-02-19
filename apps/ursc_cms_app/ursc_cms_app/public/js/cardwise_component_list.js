//for only sat hierachy filter
/*frappe.ui.form.on("Cardwise Component List", {
    refresh(frm) {
        // --- Filter Subsystems by Project ---
        frm.set_query("select_sub_system", () => ({
            query: "ursc_cms_app.api.get_subsystems_for_project",
            filters: {
                select_project: frm.doc.select_project
            }
        }));

        // --- Filter Packages by Project + Subsystem ---
        frm.set_query("pack_code", () => ({
            query: "ursc_cms_app.api.get_packages_for_project_and_subsystem",
            filters: {
                select_project: frm.doc.select_project,
                select_sub_system: frm.doc.select_sub_system
            }
        }));

        // --- Filter ECAD Cards by Project + Subsystem + Package ---
        frm.set_query("ecard_card_name", () => ({
            query: "ursc_cms_app.api.get_cards_for_project_sub_pack",
            filters: {
                select_project: frm.doc.select_project,
                select_sub_system: frm.doc.select_sub_system,
                pack_code: frm.doc.pack_code
            }
        }));
    },

    // --- When Project changes ---
    select_project(frm) {
        frm.set_value("select_sub_system", "");
        frm.set_value("pack_code", "");
        frm.set_value("ecard_card_name", "");
        frm.set_value("prj_save", frm.doc.select_project || "");
    },

    // --- When Subsystem changes ---
    select_sub_system(frm) {
        frm.set_value("pack_code", "");
        frm.set_value("ecard_card_name", "");
        frm.set_value("subsystem_save", frm.doc.select_sub_system || "");
    },

    // --- When Package changes ---
    pack_code(frm) {
        frm.set_value("ecard_card_name", "");
        frm.set_value("packsave", frm.doc.pack_code || "");
    },

    // --- When ECAD card changes ---
    ecard_card_name(frm) {
        frm.set_value("cardsave", frm.doc.ecard_card_name || "");
    }
});
*/
//NEW
//ADDED AT OCT 27
// ============================================================
// Cardwise Component List Hierarchy Filter
// PROJECT_MASTER → PRJ_SUB → PROJECT_PACKAGE → PRJ_CARDS
// ============================================================
frappe.ui.form.on("Cardwise Component List", {
    refresh(frm) {
        // --- Filter: Subsystems by Project ---
        frm.set_query("select_sub_system", () => {
            if (!frm.doc.select_project) {
                return { filters: { name: "__none__" } };
            }
            return {
                query: "ursc_cms_app.api.get_subsystems_for_project",
                filters: { select_project: frm.doc.select_project }
            };
        });

        // --- Filter: Packages by Subsystem ---
        frm.set_query("select_pack_code", () => {
            if (!frm.doc.select_sub_system) {
                return { filters: { name: "__none__" } };
            }
            return {
                query: "ursc_cms_app.api.get_packages_for_subsystem",
                filters: { select_sub_system: frm.doc.select_sub_system }
            };
        });

        // --- Filter: Cards by Package ---
        frm.set_query("ecard_card_name", () => {
            if (!frm.doc.select_pack_code) {
                return { filters: { name: "__none__" } };
            }
            return {
                query: "ursc_cms_app.api.get_cards_for_package",
                filters: { select_pack_code: frm.doc.select_pack_code }
            };
        });
    },

    // --- When Project changes ---
    select_project(frm) {
        frm.set_value("select_sub_system", null);
        frm.set_value("select_pack_code", null);
        frm.set_value("ecard_card_name", null);
    },

    // --- When Subsystem changes ---
    select_sub_system(frm) {
        frm.set_value("select_pack_code", null);
        frm.set_value("ecard_card_name", null);
    },

    // --- When Package changes ---
    select_pack_code(frm) {
        frm.set_value("ecard_card_name", null);
    }
});
frappe.ui.form.on("Cardwise Component List", {
    after_save(frm) {
        // Clear MDB List preview area
        if (frm.fields_dict.mdb_preview_html && frm.fields_dict.mdb_preview_html.$wrapper) {
            frm.fields_dict.mdb_preview_html.$wrapper.empty();
        }

        // ptionally clear child table selections or temporary data
        if (frm.mdb_list_data) {
            frm.mdb_list_data = [];
        }

        // Refresh to reflect saved child table items cleanly
        frm.refresh_field("component_list");

        //  User feedback
        //frappe.show_alert({
        //    message: __("MDB List cleared after save"),
        //    indicator: "green"
        //});
    }
});

