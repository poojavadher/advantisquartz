// Copyright (c) 2023, pooja@sanskartechnolab.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Monthly Purchase And Issue report"] = {
	"filters": [
		{
			fieldname: "month",
			label: __("Month"),
			fieldtype: "Select",
			"options": [
				{ "value": 1, "label": __("Jan") },
				{ "value": 2, "label": __("Feb") },
				{ "value": 3, "label": __("Mar") },
				{ "value": 4, "label": __("Apr") },
				{ "value": 5, "label": __("May") },
				{ "value": 6, "label": __("June") },
				{ "value": 7, "label": __("July") },
				{ "value": 8, "label": __("Aug") },
				{ "value": 9, "label": __("Sep") },
				{ "value": 10, "label": __("Oct") },
				{ "value": 11, "label": __("Nov") },
				{ "value": 12, "label": __("Dec") },
			],
			"default": frappe.datetime.str_to_obj(frappe.datetime.get_today()).getMonth() + 1,	
			reqd: 0
		},
		{
			fieldname: "year",
			label: __("Year"),
			fieldtype: "Select",
			options: [
					{ value: 2022, label: __("2022") },
					{ value: 2023, label: __("2023") },
					{ value: 2024, label: __("2024") }
			],
			default: new Date().getFullYear(), // Get the current year using JavaScript
			reqd: 0
		}
	]		
};
