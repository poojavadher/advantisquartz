// Copyright (c) 2024, pooja@sanskartechnolab.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Quality Wise Slab Report"] = {
	"filters": [
		{
            "fieldname": "company",
            "label": __("Company"),
            "fieldtype": "Link",
            "options": "Company",
            "reqd": 1
        },
        {
            "fieldname": "warehouse",
            "label": __("Warehouse"),
            "fieldtype": "Link",
            "options": "Warehouse"
        },
		{
            "fieldname": "item",
            "label": __("Item"),
            "fieldtype": "Link",
            "options": "Item"
        },
		{
            "fieldname": "status",
            "label": __("Status"),
            "fieldtype": "Select",
            "options": " \nActive\nHold"
        }
	]
};
