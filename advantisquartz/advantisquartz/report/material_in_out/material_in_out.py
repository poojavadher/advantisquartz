# Copyright (c) 2024, pooja@sanskartechnolab.com and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns(filters)
    purchase_data = get_purchase_data(filters)
    issue_data = get_issue_data(filters)
    stock_data = get_stock_data(filters)
    data = []
    
    for purchase in purchase_data:
        for issue in issue_data:
            for stock in stock_data:
                if purchase.item_code == issue.item_code and purchase.item_code == stock.item_code:
                    
                    data.append({
                    "item_code":purchase.item_code,
                    "item_name":purchase.item_name,
                    "current_stock":stock.stock_qty,
                    "issue_qty":issue.issue_qty,
                    
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
            poi.item_code,
            poi.item_name,
            SUM(poi.qty) AS "qty",
            po.supplier,
            po.posting_date
            
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



def get_stock_data(filters):
    data_query = f"""
        SELECT
            bin.item_code,
            SUM(bin.actual_qty) AS "stock_qty"
            
        FROM
            `tabBin` bin 
           
        WHERE 
        bin.actual_qty > 0     
     
          
    """
    
    

    data_query += " GROUP BY bin.item_code"

    return frappe.db.sql(data_query, as_dict=True)
