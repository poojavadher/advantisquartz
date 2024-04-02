# Copyright (c) 2024, pooja@sanskartechnolab.com and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns(filters)
    purchase_data = get_purchase_data(filters)
    issue_data = get_issue_data(filters)
    data = []
    for purchase in purchase_data:
        for issue in issue_data:
            if purchase.item_code == issue.item_code:
                data.append({
                    "item_code":purchase.item_code,
                    "item_name":purchase.item_name,
                    "qty":purchase.qty,
                    "issue_qty":issue.issue_qty,
                    "max_of_required":purchase.qty - issue.issue_qty,
                    "min_of_average_cum":issue.issue_qty/3
                })
        
            
    return columns, data


def get_columns(filters):
    columns=[
		{"label": _("Item Code"), "fieldname": "item_code", "fieldtype": "Link", "options":"Item","width":200},
  		{"label": _("Item Name"), "fieldname": "item_name", "fieldtype": "Data"},
    {"label": _("Max of Stock"), "fieldname": "qty", "fieldtype": "Float"},
    {"label": _("Issue Stock"), "fieldname": "issue_qty", "fieldtype": "Float"},
    {"label": _("Max of Required"), "fieldname": "max_of_required", "fieldtype": "Float"},
    {"label": _("Min of average cum"), "fieldname": "min_of_average_cum", "fieldtype": "Float"}
	]
    
    return columns

def get_purchase_data(filters):
    from_date = filters.get('from_date')
    to_date = filters.get('to_date')
    supplier = filters.get('supplier_name')
    data_query = f"""
        SELECT
            poi.item_code,
            poi.item_name,
            SUM(poi.qty) AS "qty",
            po.supplier
            
        FROM
            `tabPurchase Receipt` po 
            JOIN `tabPurchase Receipt Item` poi ON po.name = poi.parent 
            
        WHERE
            po.posting_date BETWEEN '{from_date}' AND '{to_date}'
    """
    
    if supplier:
        data_query += f" AND po.supplier = '{supplier}'"

    data_query += " GROUP BY poi.item_code"

    return frappe.db.sql(data_query, as_dict=True)


def get_issue_data(filters):
    from_date = filters.get('from_date')
    to_date = filters.get('to_date')
    data_query = f"""
        SELECT
            sed.item_code,
            sed.item_name,
            SUM(sed.qty) AS "issue_qty"
            
        FROM
            `tabStock Entry` se 
            JOIN `tabStock Entry Detail` sed ON se.name = sed.parent 
            
        WHERE
            se.posting_date BETWEEN '{from_date}' AND '{to_date}'
            AND sed.t_warehouse IS NULL
    """
    
    

    data_query += " GROUP BY sed.item_code"

    return frappe.db.sql(data_query, as_dict=True)



