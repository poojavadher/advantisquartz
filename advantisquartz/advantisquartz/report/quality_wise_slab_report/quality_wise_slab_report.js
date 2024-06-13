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
            "default": frappe.defaults.get_user_default("Company")
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
            "fieldname": "batch_no",
            "label": __("Batch No"),
            "fieldtype": "Link",
            "options": "Batch"
        },
		{
            "fieldname": "status",
            "label": __("Status"),
            "fieldtype": "Select",
            "options": " \nActive\nHold"
        }
	]
};
