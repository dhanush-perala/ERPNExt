// Copyright (c) 2025, neemus and contributors
// For license information, please see license.txt

frappe.ui.form.on("Radiation_Shield_Approve", {
	refresh(frm) {
		// Add button to fetch data from Radiation_Test_Data_Entry
		if (frm.doc.project && frm.doc.subsystem && frm.doc.package && frm.doc.card) {
			frm.add_custom_button(__("Fetch Test Data"), function() {
				frappe.call({
					method: "ursc_cms_app.isro_cms.doctype.radiation_shield_approve.radiation_shield_approve.fetch_test_data",
					args: {
						docname: frm.doc.name
					},
					callback: function(r) {
						if (r.message) {
							frm.reload_doc();
						}
					},
					freeze: true,
					freeze_message: __("Fetching test data...")
				});
			}, __("Actions"));
		}

		// Add button to auto approve/reject
		if (frm.doc.table_appr && frm.doc.table_appr.length > 0) {
			frm.add_custom_button(__("Auto Approve"), function() {
				frappe.confirm(
					__("This will automatically approve or reject items based on thresholds. Continue?"),
					function() {
						frappe.call({
							method: "ursc_cms_app.isro_cms.doctype.radiation_shield_approve.radiation_shield_approve.auto_approve",
							args: {
								docname: frm.doc.name
							},
							callback: function(r) {
								if (r.message) {
									frm.reload_doc();
								}
							},
							freeze: true,
							freeze_message: __("Processing approval...")
						});
					}
				);
			}, __("Actions"));
		}
	}
});
