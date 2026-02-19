// Copyright (c) 2025, neemus and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Accept_DPA_Request", {
// 	refresh(frm) {

// 	},
// });

frappe.listview_settings['ACCEPT DPA REQUEST'] = {
    onload: function(listview) {
        // Store flag so we only set the filter once per page load
        if (!listview.active_filter_applied) {
            listview.active_filter_applied = true;

            const hasFilter = listview.filter_area.get().some(f =>
                f[0] === 'ACCEPT DPA REQUEST' &&
                f[1] === 'status' &&
                f[2] === '=' &&
                f[3] === 'Active'
            );

            if (!hasFilter) {
                listview.filter_area.add([
                    ['ACCEPT DPA REQUEST', 'status', '=', 'Active']
                ]);
            }
        }
    }
};
