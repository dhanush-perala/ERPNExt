// Copyright (c) 2025, neemus and contributors
// For license information, please see license.txt

frappe.ui.form.on("PRJ_CARDS", {
	refresh(frm) {
		// Populate Project REF Number options and ECAD cards on load
		load_project_ref_options(frm);
		load_ecad_card_names(frm);
	},

	select_project(frm) {
		// When main Project is selected, prefer to auto-fill project_ref_name
		if (frm.doc.select_project_copy && frm.fields_dict.project_ref_name) {
			frm.set_value("project_ref_name", frm.doc.select_project_copy);
		}

		load_project_ref_options(frm);
		load_ecad_card_names(frm);
	},

	project_ref_name(frm) {
		// Whenever Project REF Number changes, refresh ECAD card list
		load_ecad_card_names(frm);
	},
});

/**
 * Load distinct Project REF values (based on Add Project Card.select_project_copy)
 * into the PRJ_CARDS.project_ref_name Select field.
 */
function load_project_ref_options(frm) {
	if (!frm.fields_dict.project_ref_name) {
		return;
	}

	frappe.call({
		method: "ursc_cms_app.api.get_project_ref_names",
		callback(r) {
			const refs = (r.message || []).filter(Boolean);

			// Set options for the Select field
			frm.set_df_property("project_ref_name", "options", ["", ...refs]);

			// Clear value if it's no longer valid
			if (!refs.includes(frm.doc.project_ref_name)) {
				frm.set_value("project_ref_name", "");
			}

			frm.refresh_field("project_ref_name");
		},
	});
}

/**
 * Populate ECAD Card Name options based on selected Project REF Number.
 * Only card_name values from Add Project Card Table whose parent Add Project Card
 * has matching select_project_copy / Project Ref will be shown.
 */
function load_ecad_card_names(frm) {
	if (!frm.fields_dict.ecad_card_name) {
		return;
	}

	const project_ref = frm.doc.project_ref_name;

	if (!project_ref) {
		frm.set_df_property("ecad_card_name", "options", [""]);
		frm.set_value("ecad_card_name", "");
		return;
	}

	frappe.call({
		method: "ursc_cms_app.api.get_ecad_card_names_by_project_ref",
		args: { project_ref_name: project_ref },
		callback(r) {
			const names = (r.message || []).filter(Boolean);

			frm.set_df_property("ecad_card_name", "options", ["", ...names]);

			if (!names.includes(frm.doc.ecad_card_name)) {
				frm.set_value("ecad_card_name", "");
			}

			frm.refresh_field("ecad_card_name");
		},
	});
}

// // Copyright (c) 2025, neemus and contributors
// // For license information, please see license.txt

// frappe.ui.form.on("PRJ_CARDS", {
// 	refresh(frm) {
// 		// Filter packages dynamically (optional subsystem context)
// 		frm.set_query("pack_name", () => ({
// 			query: "ursc_cms_app.api.get_packages_for_project_and_subsystem",
// 			filters: {
// 				sub_system: frm.doc.sub_system || frm.doc.select_sub_system,
// 			},
// 		}));

// 		load_ecad_card_names(frm);
// 	},

// 	select_project(frm) {
// 		load_ecad_card_names(frm);
// 	},

// 	pack_name(frm) {
// 		// pack_code field will automatically fetch from pack_name.pack_name via fetch_from
// 		// No need to manually set it here
// 		if (frm.doc.pack_name && frm.fields_dict.pack_code) {
// 			frm.refresh_field("pack_code");
// 		}
// 	},
// });

// function load_ecad_card_names(frm) {
// 	const project = frm.doc.select_project;

// 	if (!project) {
// 		frm.set_df_property("ecad_card_name", "options", [""]);
// 		frm.set_value("ecad_card_name", "");
// 		return;
// 	}

// 	frappe.call({
// 		method: "ursc_cms_app.api.get_ecad_card_names_for_project",
// 		args: { project },
// 		callback(r) {
// 			const names = (r.message || []).filter(Boolean);
// 			frm.set_df_property("ecad_card_name", "options", ["", ...names]);
// 			if (!names.includes(frm.doc.ecad_card_name)) {
// 				frm.set_value("ecad_card_name", "");
// 			}
// 			frm.refresh_field("ecad_card_name");
// 		},
// 	});
// }

// function set_field_if_exists(frm, fieldname, value) {
// 	if (frm.fields_dict[fieldname]) {
// 		frm.set_value(fieldname, value);
// 	}
// }
