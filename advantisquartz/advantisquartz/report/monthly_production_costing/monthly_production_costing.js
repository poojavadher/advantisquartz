frappe.query_reports["Monthly Production Costing"] = {
	"filters": [
		{
			label: __("From Date"),
			fieldname: "from_date",
			fieldtype: "Date",
			default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			reqd: 1
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
			reqd: 1
		},
		{
			fieldname: "item_group",
			label: __("Item Group"),
			fieldtype: "Link",
			options: "Item Group",
			reqd: 0,
			get_query: function() {
				return {
					filters: [
						["Item Group", "is_group", "=", 1],
						
					]
				};
			}
		},
		{
			fieldname: "sub_item_group",
			label: __("Sub Item Group"),
			fieldtype: "Link",
			options: "Item Group",
			reqd: 0,
			get_query: function() {
				return {
					filters: [
						["Item Group", "is_group", "=", 0],
						
					]
				};
			}
		},
		{
			fieldname: "attribute_value",
			label: __("Attribute Value"),
			fieldtype: "Data",
			reqd: 0
		},
		{
			fieldname: "item_code",
			label: __("Finish Item Code"),
			fieldtype: "Link",
			options: "Item",
			reqd: 0,
			get_query: function() {
				return {
					filters: [
						["Item", "item_group", "=", "FINISH GOODS"],
						
					]
				};
			}
			
		},
	],

};
