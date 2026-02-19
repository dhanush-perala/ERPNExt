frappe.listview_settings['ADD PROJECT SUBSYSTEM'] = {
    onload: function(listview) {
        if (!listview.active_filter_applied) {
            listview.active_filter_applied = true;

            const hasFilter = listview.filter_area.get().some(f =>
                f[0] === 'ADD PROJECT SUBSYSTEM' &&
                f[1] === 'status' &&
                f[2] === '=' &&
                f[3] === 'Active'
            );

            if (!hasFilter) {
                listview.filter_area.add([
                    ['ADD PROJECT SUBSYSTEM', 'status', '=', 'Active']
                ]);
            }
        }
    }
};
