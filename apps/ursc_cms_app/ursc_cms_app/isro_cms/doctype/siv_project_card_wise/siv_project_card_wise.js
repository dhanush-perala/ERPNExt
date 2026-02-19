// Copyright (c) 2025, neemus and contributors
// For license information, please see license.txt

frappe.ui.form.on("SIV Project Card Wise", {
	refresh(frm) {
		update_select_card_options(frm);
	},

	card_type(frm) {
		frm.set_value("select_card", "");
		update_select_card_options(frm);
	},
});

function update_select_card_options(frm) {
	if (!frm.fields_dict.select_card) {
		return;
	}

	const type = frm.doc.card_type;
	if (!type || type === "Select") {
		frm.set_df_property("select_card", "options", [""]);
		frm.set_value("select_card", "");
		return;
	}

	frappe.call({
		method: "ursc_cms_app.api.get_approved_cards_by_type",
		args: { card_type: type },
		callback: (r) => {
			const names = (r.message || []).filter(Boolean);
			frm.set_df_property("select_card", "options", ["", ...names]);
			if (!names.includes(frm.doc.select_card)) {
				frm.set_value("select_card", "");
			}
			frm.refresh_field("select_card");
		},
	});
}

