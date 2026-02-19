// Copyright (c) 2025, neemus and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Update_MDB_PartNo_with_Alerts", {
// 	refresh(frm) {

// 	},
// });
frappe.listview_settings['UPDATE MDB PARTNO WITH ALERTS'] = {
    onload: function(listview) {
        // Store flag so we only set the filter once per page load
        if (!listview.active_filter_applied) {
            listview.active_filter_applied = true;

            const hasFilter = listview.filter_area.get().some(f =>
                f[0] === 'UPDATE MDB PARTNO WITH ALERTS' &&
                f[1] === 'status' &&
                f[2] === '=' &&
                f[3] === 'Active'
            );

            if (!hasFilter) {
                listview.filter_area.add([
                    ['UPDATE MDB PARTNO WITH ALERTS', 'status', '=', 'Active']
                ]);
            }
        }
    }
};
