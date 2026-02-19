frappe.listview_settings['PROJECT_MASTER'] = {
    onload: function(listview) {
        if (listview.active_filter_applied) return;
        listview.active_filter_applied = true;

        const filters = listview.filter_area.get();

        // --- Status filter ---
        const hasStatusFilter = filters.some(f =>
            f[1] === 'status' && f[2] === '=' && f[3] === 'Active'
        );

        if (!hasStatusFilter) {
            listview.filter_area.add([['PROJECT_MASTER', 'status', '=', 'Active']]);
        }

        // --- Workflow filter ---
        const hasWorkflowField = listview.meta.fields.some(df => df.fieldname === 'work_flow_status');
        const hasWorkflowFilter = filters.some(f =>
            f[1] === 'work_flow_status' && f[2] === 'in'
        );

        if (hasWorkflowField && !hasWorkflowFilter) {
            listview.filter_area.add([['PROJECT_MASTER', 'work_flow_status', 'in', 'Pending for Approve,Approve,Reject']]);
        }
    },

    // --- Color formatting ---
    formatters: {
        work_flow_status(val) {
            if (val === 'Pending for Approve') {
                return `<span style="background:#ff9800;color:#fff;padding:2px 6px;border-radius:8px;font-weight:bold;">${val}</span>`;
            }
            if (val === 'Approve') {
                return `<span style="background:#28a745;color:#fff;padding:2px 6px;border-radius:8px;font-weight:bold;">${val}</span>`;
            }
            if (val === 'Reject') {
                return `<span style="background:#dc3545;color:#fff;padding:2px 6px;border-radius:8px;font-weight:bold;">${val}</span>`;
            }
            return val;
        },

        select_project_status(val) {
            if (val === 'ON GOING') {
                return `<span style="background:#007bff;color:#fff;padding:2px 6px;border-radius:8px;font-weight:bold;">${val}</span>`;
            }
            if (val === 'LUNCHED') {
                return `<span style="background:#6c757d;color:#fff;padding:2px 6px;border-radius:8px;font-weight:bold;">${val}</span>`;
            }
            return val;
        }
    }
};

