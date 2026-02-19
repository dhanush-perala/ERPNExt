/*frappe.ui.form.on("PRJ_CARDS", {
refresh(frm) {
// --- Filter Subsystems by Project ---
frm.set_query("select_sub_system", () => {
return {
query: "ursc_cms_app.api.get_subsystems_for_project",
filters: {
select_project: frm.doc.select_project
}
};
});

// --- Filter Packages by Project + Subsystem ---
frm.set_query("pack_code", () => {
return {
query: "ursc_cms_app.api.get_packages_for_project_and_subsystem",
filters: {
select_project: frm.doc.select_project,
select_sub_system: frm.doc.select_sub_system
}
};
});
},

// --- When Project changes ---
select_project(frm) {
// Clear dependent fields
frm.set_value("select_sub_system", "");
frm.set_value("pack_code", "");
frm.set_value("prj_save", frm.doc.select_project || "");
frm.refresh_field("select_sub_system");
frm.refresh_field("pack_code");
},

// --- When Subsystem changes ---
select_sub_system(frm) {
// Clear dependent package since subsystem changed
frm.set_value("pack_code", "");
frm.set_value("subsystem_save", frm.doc.select_sub_system || "");
frm.refresh_field("pack_code");
},

// --- When Package changes ---
pack_code(frm) {
frm.set_value("packsave", frm.doc.pack_code || "");
}
});
*/
frappe.ui.form.on("PRJ_CARDS", {
refresh(frm) {
// --- Filter Packages ---
frm.set_query("pack_code", () => {
return {
query: "ursc_cms_app.api.get_packages_for_project_and_subsystem",
filters: {
sub_system: frm.doc.sub_system // optional, if you later reintroduce subsystem
}
};
});

load_ecad_card_names(frm);
},

// --- When Package changes ---
pack_code(frm) {
// Auto-fetch package info from selected package
if (frm.doc.pack_code) {
frappe.db.get_doc("PROJECT_PACKAGE", frm.doc.pack_code)
.then(pkg => {
// Automatically fill related details
frm.set_value("pack_name", pkg.pack_name);
frm.set_value("sub_system", pkg.sub_system); // if field exists
frm.set_value("project", pkg.project); // if field exists
frm.refresh_field("pack_name");
});
} else {
// If package cleared, reset dependent fields
frm.set_value("pack_name", "");
frm.set_value("sub_system", "");
frm.set_value("project", "");
}
}
});

function load_ecad_card_names(frm) {
frappe.call({
method: "ursc_cms_app.api.get_add_project_card_names",
callback(r) {
if (!r.message) {
return;
}

const names = r.message
.map(d => d.card_name)
.filter(Boolean);

frm.set_df_property("ecad_card_names", "options", ["", ...names]);
frm.refresh_field("ecad_card_names");
}
});
}

