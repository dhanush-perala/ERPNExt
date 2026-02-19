frappe.ui.form.on("SIV", {
	refresh: function (frm) {
		if (frm.doc.work_flow_status === "Approved" && frm.doc.status === "Active") {
			start_countdown(frm);
		} else {
			// Ensure timer box is cleared if conditions aren't met
			frm.set_df_property("timer_html", "options", "");
			frm.refresh_field("timer_html");
			if (frm.timer_interval) {
				clearInterval(frm.timer_interval);
				frm.timer_interval = null;
			}
		}

		// Requirement: Read-only when Inactive
		if (frm.doc.status === "Inactive") {
			frm.set_read_only();
		}
	},
});

function start_countdown(frm) {
	if (!frm.doc.approved_on) {
		console.log("[SIV] No approved_on found on doc, waiting for a second...");
		setTimeout(() => {
			if (!frm.doc.approved_on) frm.reload_doc();
		}, 1000);
		return;
	}

	const approved_on = frappe.datetime.str_to_obj(frm.doc.approved_on);
	const target_time = new Date(approved_on.getTime() + 60 * 24 * 60 * 60 * 1000); // 60 days later

	const update_timer = () => {
		const now = new Date();
		const diff_ms = target_time - now;

		if (diff_ms <= 0) {
			frm.set_df_property(
				"timer_html",
				"options",
				'<div style="padding: 8px; background-color: #fff5f5; color: #c53030; border: 1px solid #fecaca; border-radius: 8px; font-weight: bold; text-align: center; margin-top: 10px;">Processing Inactivation...</div>'
			);
			clearInterval(frm.timer_interval);
			// Daily jobs might take time, so we just reload to check status
			setTimeout(() => frm.reload_doc(), 1000);
			return;
		}

		// Calculate Days, Hours, Minutes
		const diff_s = Math.floor(diff_ms / 1000);
		const days = Math.floor(diff_s / (24 * 3600));
		const hours = Math.floor((diff_s % (24 * 3600)) / 3600);
		const mins = Math.floor((diff_s % 3600) / 60);
		const secs = diff_s % 60;

		let time_str = `${days}d ${hours}h ${mins}m ${secs}s`;

		frm.set_df_property(
			"timer_html",
			"options",
			`<div style="padding: 8px 15px; background-color: #fff5f5; color: #c53030; border: 1px solid #fecaca; border-radius: 8px; font-weight: bold; text-align: center; margin-top: 10px; display: flex; align-items: center; justify-content: center; gap: 10px;">
				<span style="font-size: 1.2em;">🕙</span>
				<span>Request becomes <span style="text-transform: uppercase;">Inactive</span> in: <span style="font-size: 1.3em; margin-left: 5px;">${time_str}</span></span>
			</div>`
		);
	};

	if (frm.timer_interval) clearInterval(frm.timer_interval);
	update_timer();
	frm.timer_interval = setInterval(update_timer, 1000);
}

