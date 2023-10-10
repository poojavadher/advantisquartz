// Copyright (c) 2023, pooja@sanskartechnolab.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Machine Maintenance Log', {
	asset_maintenance: (frm) => {
		frm.set_query('task', function(doc) {
			return {
				query: "advantisquartz.machine_maintenance.doctype.machine_maintenance_schedule.machine_maintenance_log.get_maintenance_tasks",
				filters: {
					'asset_maintenance': doc.asset_maintenance
				}
			};
		});
	}
});
