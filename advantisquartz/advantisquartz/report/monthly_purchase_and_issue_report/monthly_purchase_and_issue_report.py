# Copyright (c) 2023, pooja@sanskartechnolab.com and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns(filters)
	item = get_item(filters)
	data = []
	for it in item:
		data.append(it)
	return columns, data


def get_columns(filters):
    columns = [
		{"label": _("Item Code"), "fieldname": "item_code", "fieldtype": "Link", "options":"Item"},
		{"label": _("Item Name"), "fieldname": "item_name", "fieldtype": "Data"},
  		{"label": _("Unit"), "fieldname": "stock_uom", "fieldtype": "Link", "options":"UOM"},
	]
    return columns

def get_item(filters):
    item = frappe.qb.DocType("Item")
    query = (
        frappe.qb.from_(item)
        .select(
			item.item_code,
			item.item_name,
            item.stock_uom
   
		)
        )
    return query.run(as_dict= True)
		