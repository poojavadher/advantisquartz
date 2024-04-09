# Copyright (c) 2024, pooja@sanskartechnolab.com and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns(filters)
    purchase_data = get_purchase_data(filters)
  
    issue_data = get_issue_data(filters)
    data = []
    # for item in purchase_data:
    #     for bin in bin_data:
    #         # for issue in issue_data:
    #             if item.item_code == bin.item_code :
    #                 data.append({"item_code":item.item_code,
    #                          "item_name":item.item_name,
    #                          "current_stock":bin.bin_qty})

    for item in purchase_data:
        for issue in issue_data:
            if item.item_code == issue.item_code:
                data.append({
                    "item_code":item.item_code,
                             "item_name":item.item_name,
                             "current_stock":item.bin_qty,
                             "issue_qty":issue.issue_qty
                })    
    
            
    return columns, data


def get_columns(filters):
    columns=[
       
		{"label": _("Item Code"), "fieldname": "item_code", "fieldtype": "Link", "options":"Item","width":200},
  		{"label": _("Item Name"), "fieldname": "item_name", "fieldtype": "Data"},
    {"label": _("Current Stock"), "fieldname": "current_stock", "fieldtype": "Float"},
    {"label": _("Issue Stock"), "fieldname": "issue_qty", "fieldtype": "Float"},
   
	]
    
    return columns

def get_purchase_data(filters):
    from_date = filters.get('from_date')
    to_date = filters.get('to_date')
    supplier = filters.get('supplier_name')
    data_query = f"""
        SELECT
           po.name,
           poi.item_code,
           poi.item_name,
           COALESCE(bin_qty, 0) AS "bin_qty"
        FROM
            `tabPurchase Receipt` po
            JOIN `tabPurchase Receipt Item` poi ON po.name = poi.parent
            LEFT JOIN (
                SELECT item_code, SUM(actual_qty) AS bin_qty
                FROM `tabBin`
                GROUP BY item_code
            ) bin ON poi.item_code = bin.item_code
        WHERE
            po.posting_date BETWEEN '{from_date}' AND '{to_date}'
            AND po.status != "Cancelled"
            AND poi.item_code = bin.item_code
    """
    if supplier:
        data_query += f" AND po.supplier = '{supplier}'"
    data_query += " GROUP BY poi.item_code, po.supplier, bin.item_code"
    return frappe.db.sql(data_query, as_dict=True)



def get_issue_data(filters):
    from_date = filters.get('from_date')
    to_date = filters.get('to_date')
    data_query = f"""
		SELECT
		sle.item_code,
		ABS(sum(sle.actual_qty)) AS "issue_qty"
        FROM `tabStock Ledger Entry` sle
		WHERE
		sle.posting_date BETWEEN '{from_date}' AND '{to_date}'
		AND sle.actual_qty < 0
        AND sle.is_cancelled = 0
    """
    data_query += " GROUP BY sle.item_code"
    
    return frappe.db.sql(data_query, as_dict=True)