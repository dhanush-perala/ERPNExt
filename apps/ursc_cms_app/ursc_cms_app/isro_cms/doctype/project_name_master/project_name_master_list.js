frappe.listview_settings['Project_name_master'] = {
    onload: function(listview) {
        // Store flag so we only set the filter once per page load
        if (!listview.active_filter_applied) {
            listview.active_filter_applied = true;

            const hasFilter = listview.filter_area.get().some(f =>
                f[0] === 'Project_name_master' &&
                f[1] === 'status' &&
                f[2] === '=' &&
                f[3] === 'Active'
            );

            if (!hasFilter) {
                listview.filter_area.add([
                    ['Project_name_master', 'status', '=', 'Active']
                ]);
            }
        }
    }
};

