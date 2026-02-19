// Copyright (c) 2025, neemus and contributors
// For license information, please see license.txt

frappe.ui.form.on("Cardwise Component List Update and Approve - Designer", {
	refresh(frm) {
		load_card_names(frm);
	},

	pack_name(frm) {
		if (!frm.doc.pack_name) {
			update_card_options(frm, []);
			return;
		}

		load_card_names(frm);
	},
});

function load_card_names(frm) {
	if (!frm.doc.pack_name) {
		update_card_options(frm, []);
		return;
	}

	frappe.call({
		method: "ursc_cms_app.api.get_card_names_for_pack",
		args: { pack_name: frm.doc.pack_name },
		callback: (r) => {
			const names = (r.message || []).filter(Boolean);
			update_card_options(frm, names);

			if (!names.length) {
				frappe.msgprint({
					title: __("No Card Names"),
					message: __("No card names found for the selected package."),
					indicator: "orange",
				});
			}
		},
	});
}

function update_card_options(frm, options) {
	const final_options = ["", ...options];
	frm.set_df_property("card_name", "options", final_options);
	frm.refresh_field("card_name");
	if (!options.length) {
		frm.set_value("card_name", "");
	}
}

