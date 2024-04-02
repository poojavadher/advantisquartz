# Copyright (c) 2024, pooja@sanskartechnolab.com and contributors
# For license information, please see license.txt
import frappe
from frappe import _
from datetime import datetime, date

def execute(filters=None):
    columns = get_columns(filters)
    work_order_data = get_work_order_data(filters)
    rate_data = get_rate_order_data(filters)
    data = []
    total_qty = 0
    total_ratio = 0
    total_qty_manufacture = 0 
    total_qty_slab = 0
    total_amt = 0
    for work_data in work_order_data:
        total_qty += work_data.qty
        total_qty_manufacture += work_data.manufacture_qty
    for work_data in work_order_data:
        wo_creation_date = work_data.actual_end_date.date()
        for rates_data in rate_data:
            if work_data.item_code == rates_data.item_code and wo_creation_date > rates_data.posting_date:
                rates = rates_data.valuation_rate
            
        
        data.append({
            "raw_material": work_data.item_code,
            "rate": rates,
            "ratio":(work_data.qty / total_qty)*100,
            "qty": work_data.qty,
            "qty_kg_slab":work_data.qty/total_qty_manufacture,
            "amt":(work_data.qty/total_qty_manufacture)*rates
        })
        total_ratio += (work_data.qty / total_qty)*100
        total_qty_slab += float(work_data.qty/total_qty_manufacture)
        total_amt += (work_data.qty/total_qty_manufacture)*rates
    # Append total row
    data.append({
        "raw_material": _("Total"),
        "ratio": total_ratio,
        "qty": total_qty,
        "qty_kg_slab":total_qty_slab,
        "amt":total_amt
    })

    return columns, data



def get_columns(filters):
    column =[
		{"label":_("Raw Material"),"fieldname":"raw_material","fieldtype":"Link","options":"Item","width":200},
  		{"label":_("Grade"),"fieldname":"grade","fieldtype":"Data","width":120},
		{"label":_("Rate"),"fieldname":"rate","fieldtype":"Float","width":120},
  		{"label":_("Ratio"),"fieldname":"ratio","fieldtype":"Float","width":120},
		{"label":_("Qty(Kg)"),"fieldname":"qty","fieldtype":"Float","width":120},
		{"label":_("Qty(Kg/Slab)"),"fieldname":"qty_kg_slab","fieldtype":"Float","width":120},
		{"label":_("Amt.(Rs.)"),"fieldname":"amt","fieldtype":"Float","width":120}
  
	]
    
    return column

def get_work_order_data(filters):
    from_date = filters.get('from_date')
    to_date = filters.get('to_date')
    sub_item_group = filters.get('sub_item_group')
    attribute_value = filters.get('attribute_value')
    data_query = f"""
        SELECT
            wo.production_item,
            woi.item_code,
            woi.item_name,
            SUM(woi.consumed_qty) AS "qty",
            wo.actual_end_date,
            SUM(wo.produced_qty) AS "manufacture_qty"
        FROM
            `tabWork Order` wo
         JOIN
            `tabWork Order Item` woi ON wo.name = woi.parent
            
		JOIN `tabItem` item ON wo.production_item = item.name
        WHERE
            wo.actual_end_date BETWEEN '{from_date}' AND '{to_date}'
            AND item.item_sub_group = '{sub_item_group}'
            AND item.thickness = '{attribute_value}'
    """
    
    
        
    data_query += " GROUP BY wo.production_item, woi.item_code"
    return frappe.db.sql(data_query, as_dict=True)

def get_rate_order_data(filters):
    
    data_query = f"""
        SELECT
            stl.item_code,
            stl.valuation_rate,
            stl.posting_date,
            stl.name
        FROM
            `tabStock Ledger Entry` stl 
        WHERE
        
             stl.valuation_rate IS NOT NULL
        
    """

    return frappe.db.sql(data_query, as_dict=True)
