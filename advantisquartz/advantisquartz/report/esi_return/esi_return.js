// Copyright (c) 2023, pooja@sanskartechnolab.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["ESI Return"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date"
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date"
		}
	],
	"onload": function (report) {
		report.page.add_inner_button(__('ESI Return'), function () {
			let d = new frappe.ui.Dialog({
				title: 'Select Date for ESI Return',
				fields: [
					{
						label: 'From Date',
						fieldname: 'from_date',
						fieldtype: 'Date',
						reqd: 1
					},
					{
						label: 'To Date',
						fieldname: 'to_date',
						fieldtype: 'Date',
						reqd: 1
					}
				],
				size: 'small',
				primary_action_label: 'Submit',
				primary_action(values) {
					frappe.call({
						method: 'advantisquartz.advantisquartz.doctype.api.create_xlsx',
						args: {
							from_date: values.from_date,
							to_date: values.to_date
						},
						callback: function (response) {
							console.log(response);
						}
					});
					d.hide();
				}
			});

			d.show();
		});
	}
};
