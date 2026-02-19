frappe.listview_settings['PROJECT MASTER APPROVE'] = {
    onload: function(listview) {
        if (!listview.active_filter_applied) {
            listview.active_filter_applied = true;

            const filters = listview.filter_area.get();

            // ✅ Status filter (Active)
            const hasStatusFilter = filters.some(f =>
                f[0] === 'PROJECT MASTER APPROVE' &&
                f[1] === 'status' &&
                f[2] === '=' &&
                f[3] === 'Active'
            );

            if (!hasStatusFilter) {
                listview.filter_area.add([
                    ['PROJECT MASTER APPROVE', 'status', '=', 'Active']
                ]);
            }

            // ✅ Workflow filter (only if work_flow_status field exists)
            const hasWorkflowField = listview.meta.fields.some(df => df.fieldname === 'work_flow_status');
            const hasWorkflowFilter = filters.some(f =>
                f[0] === 'PROJECT MASTER APPROVE' &&
                f[1] === 'work_flow_status' &&
                f[2] === 'in'
            );

            if (hasWorkflowField && !hasWorkflowFilter) {
                listview.filter_area.add([
                    ['PROJECT MASTER APPROVE', 'work_flow_status', 'in', ['Pending for Approve', 'Approve', 'Reject']]
                ]);
            }
        }
    },

    // ✅ Color formatting for workflow status
    formatters: {
        work_flow_status(val) {
            if (val === 'Pending for Approve') {
                return `<span style="color:orange; font-weight:bold;">${val}</span>`;
            }
            if (val === 'Approve') {
                return `<span style="color:orange; font-weight:bold;">${val}</span>`;  // Blue for Approved
            }
            if (val === 'Reject') {
                return `<span style="color:red; font-weight:bold;">${val}</span>`;   // Red for Rejected
            }
            return val;
        }
    }
};

