frappe.ui.form.on('SRN POST', {
	refresh: function(frm) {
		// Auto-fill SRN Reference number when creating a new document
		if (frm.is_new()) {
			// Generate a random 4-digit number for preview
			// The actual unique number will be generated server-side
			const previewNumber = Math.floor(Math.random() * 9000) + 1000;
			frm.set_value('srn_ref_no', previewNumber);
			
			// Add a button to generate SRN Reference number
			frm.add_custom_button(__('Generate SRN Ref No'), function() {
				frm.call('generate_srn_ref_no').then(r => {
					if (r.message) {
						frm.set_value('srn_ref_no', r.message);
						frappe.show_alert({
							message: __('SRN Reference Number generated: {0}', [r.message]),
							indicator: 'green'
						});
					}
				});
			}, __('Actions'));
		}
	},
	
	srn_ref_no: function(frm) {
		// Validate that the SRN Reference number is 4 digits
		if (frm.doc.srn_ref_no) {
			const srnRefNo = frm.doc.srn_ref_no.toString();
			if (srnRefNo.length !== 4 || !/^\d{4}$/.test(srnRefNo)) {
				frappe.msgprint({
					title: __('Invalid SRN Reference Number'),
					message: __('SRN Reference Number must be a 4-digit number (1000-9999)'),
					indicator: 'red'
				});
				frm.set_value('srn_ref_no', '');
			}
		}
	}
});
