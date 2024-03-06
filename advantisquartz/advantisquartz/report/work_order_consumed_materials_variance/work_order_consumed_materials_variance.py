# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from collections import defaultdict
from datetime import datetime
import frappe
from frappe import _


# ... (existing code)

def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    wo_data = get_work_order_data(filters)
    wo_sum_data = get_sum_work_order_data(filters)
    wo_rate_data = get_rate_order_data(filters)
    fo_qty = 0
    cons_qty = 0
    data = []
    formula_total = 0
    previous_wo_name = ''
    wo_group_data = []  # List to hold data grouped by work order
    
    for wo_datas in wo_data:
        fo_qty += (wo_datas.required_qty / wo_datas.qty)
        cons_qty += wo_datas.consumed_qty
        formula_total += (wo_datas.required_qty / wo_datas.qty)
    for wo_data_name in wo_data:
            qty_rate = 0
            
            if wo_data_name.name != previous_wo_name :
                
                if wo_group_data:
                # If there is data for the previous work order, add a total row
                    total_row = get_total_row(wo_group_data, ["qty", "produced_qty","formula_qty","formula_qty_per","cons_qty_per","required_qty","consumed_qty","rm_rate","rm_cost","cost_slab","qty_prop","var_formula","var_qty"])
                    data.extend(wo_group_data)
                    data.append(total_row)
                    wo_group_data = []  # Reset the group for the new work order
                formula_qty_per = 0
                consumed_qty_per = 0
                for work_data in wo_sum_data:
                    if work_data.name == wo_data_name.name:
                        formula_qty_per += work_data.qty
                        consumed_qty_per += work_data.consumed_qty
                rates = 0
                for rate_data in wo_rate_data:
                    wo_creation_date = wo_data_name.posting_date
                    if wo_data_name.item_code == rate_data.item_code and wo_creation_date > rate_data.posting_date:
                        rates = rate_data.valuation_rate
                        print("\n\n", rate_data, "\n\n")
                wo_group_data.append({
						"name": wo_data_name.name,
                		"status": wo_data_name.status,
                		"production_item":  wo_data_name.production_item,
                		"qty": wo_data_name.qty,
                		"produced_qty": wo_data_name.produced_qty,
						"required_qty":wo_data_name.required_qty,
						"consumed_qty":wo_data_name.consumed_qty,
						"uom":wo_data_name.uom,
						"raw_material_item_code":wo_data_name.item_code,
                         "raw_material_name":wo_data_name.item_name,
                         "consumed_material_item_code":wo_data_name.raw_code,
                         
						"formula_qty":(wo_data_name.required_qty/wo_data_name.qty),
						"formula_qty_per": (((wo_data_name.required_qty/wo_data_name.qty)/formula_qty_per)*wo_data_name.qty)*100 if formula_qty_per != 0 else 0,
"cons_qty_per": (wo_data_name.consumed_qty/consumed_qty_per)*100 if consumed_qty_per != 0 else 0,
						"rm_rate":rates,
						"rm_cost":(wo_data_name.consumed_qty * rates),
						"cost_slab":((wo_data_name.consumed_qty * rates)/wo_data_name.qty),
						
						"var_formula":(((wo_data_name.required_qty/wo_data_name.qty)/(formula_qty_per/wo_data_name.qty))*100)-( (wo_data_name.consumed_qty/consumed_qty_per)*100) if formula_qty_per != 0 and consumed_qty_per !=0 else 0,
						"var_qty":wo_data_name.required_qty - wo_data_name.consumed_qty if  consumed_qty_per !=0 else 0,
                        "var_amt":(wo_data_name.required_qty - wo_data_name.consumed_qty if  consumed_qty_per !=0 else 0)*(rates),
                        
			    })
               
            else:
                rates_no = 0
                for rate_data in wo_rate_data:
                    wo_creation_date = wo_data_name.posting_date
                    if wo_data_name.item_code == rate_data.item_code and wo_creation_date > rate_data.posting_date:
                        rates_no = rate_data.valuation_rate
                        print("\n\n", rate_data, "\n\n") 
                item_code_row = {
                "name": '',
                "status": '',
                "production_item": '',
                "qty": '',
                "produced_qty":'',
                "raw_material_item_code": wo_data_name.item_code,
                "raw_material_name":wo_data_name.item_name,
                "consumed_material_item_code":wo_data_name.raw_code,
                
                "consumed_qty":wo_data_name.consumed_qty,
                "transferred_qty":wo_data_name.transferred_qty,
                "required_qty":wo_data_name.required_qty,
                "formula_qty":(wo_data_name.required_qty/wo_data_name.qty),
                "formula_qty_per": (((wo_data_name.required_qty/wo_data_name.qty)/formula_qty_per)*wo_data_name.qty)*100 if formula_qty_per != 0 else 0,
"cons_qty_per": (wo_data_name.consumed_qty/consumed_qty_per)*100 if consumed_qty_per != 0 else 0,
                "uom":wo_data_name.uom,
                "rm_rate":rates_no,
                "rm_cost":wo_data_name.consumed_qty * rates_no,
                "cost_slab":((wo_data_name.consumed_qty * rates_no)/wo_data_name.qty),
                
                "var_formula":(((wo_data_name.required_qty/wo_data_name.qty)/(formula_qty_per/wo_data_name.qty))*100)-( (wo_data_name.consumed_qty/consumed_qty_per)*100) if formula_qty_per != 0 and consumed_qty_per !=0 else 0,
                "var_qty":wo_data_name.required_qty - wo_data_name.consumed_qty if  consumed_qty_per !=0 else 0,
                "var_amt":(wo_data_name.required_qty - wo_data_name.consumed_qty if  consumed_qty_per !=0 else 0)*(rates),
            }
                wo_group_data.append(item_code_row)

            previous_wo_name = wo_data_name.name

    # Add the total row for the last work order in the data
    if wo_group_data:
        total_row = get_total_row(wo_group_data, ["qty", "produced_qty","formula_qty","formula_qty_per","cons_qty_per","required_qty","consumed_qty","rm_rate","rm_cost","cost_slab","qty_prop","var_formula","var_qty"])
        data.extend(wo_group_data)
        data.append(total_row)

    return columns, data

def get_total_row(wo_group_data, fields_to_sum):
    total_row = {}

    # Initialize the total_row with 0 for all fields
    for fieldname in wo_group_data[0].keys():
        total_row[fieldname] = 0

    # Calculate totals for the specified fields and add them to the total_row dictionary
    for row in wo_group_data:
        for key, value in row.items():
            if key in fields_to_sum and value is not None:
                try:
                    total_row[key] += float(value)
                except ValueError:
                    pass  # Ignore non-numeric values

    total_row["name"] = "Total"
    return total_row




def get_columns():
	return [
		{
			"label": _("Id"),
			"fieldname": "name",
			"fieldtype": "Link",
			"options": "Work Order",
			"width": 180,
			
		},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
		{
			"label": _("Production Item"),
			"fieldname": "production_item",
			"fieldtype": "Link",
			"options": "Item",
			"width": 130,
		},
		{"label": _("Qty to Produce"), "fieldname": "qty", "fieldtype": "Float", "width": 120},
		{"label": _("Produced Qty"), "fieldname": "produced_qty", "fieldtype": "Float", "width": 110},
		{
			"label": _("Raw Material Item"),
			"fieldname": "raw_material_item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 200,
		},
		{"label": _("Item Name"), "fieldname": "raw_material_name", "width": 130},
  {
			"label": _("Consumed Material Item"),
			"fieldname": "consumed_material_item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 200,
		},
		
  		{"label": _("Formula Qty"), "fieldname": "formula_qty", "fieldtype": "Float", "width": 100,"precision":2},
  		{"label": _("Formula %"), "fieldname": "formula_qty_per", "fieldtype": "Float", "width": 100,"precision":2},
		{"label": _("Cons %"), "fieldname": "cons_qty_per", "fieldtype": "Float", "width": 100,"precision":2},
		{"label": _("Required Qty"), "fieldname": "required_qty", "fieldtype": "Float", "width": 100,"precision":2},
		{"label": _("Consumed Qty"), "fieldname": "consumed_qty", "fieldtype": "Float", "width": 100,"precision":2},
  		{"label": _("UOM"), "fieldname": "uom", "width": 130},
    	{"label": _("RM RATE"), "fieldname": "rm_rate", "fieldtype": "Float", "width": 100,"precision":2},
		{"label": _("RM Cost"), "fieldname": "rm_cost", "fieldtype": "Float", "width": 100,"precision":2},
  		{"label": _("COST/SLAB"), "fieldname": "cost_slab", "fieldtype": "Float", "width": 100,"precision":2},
      	{"label": _("VAR. FORMULA"), "fieldname": "var_formula", "fieldtype": "Float", "width": 150,"precision":2},
      	{"label": _("VAR.Qty"), "fieldname": "var_qty", "fieldtype": "Float", "width": 100,"precision":2},
       {"label": _("VAR.AMT"), "fieldname": "var_amt", "fieldtype": "Float", "width": 100,"precision":2},


		
	]
 
def get_work_order_data(filters):
    wo = frappe.qb.DocType("Work Order")
    woi = frappe.qb.DocType("Work Order Item")
    item = frappe.qb.DocType("Item")
    stock = frappe.qb.DocType("Stock Entry")
    work_order = filters.get('name')
    production_item = filters.get('production_item')
    status = filters.get('status')
    query = (
        frappe.qb.from_(wo)
        .join(woi)
        .on(wo.name == woi.parent)
        .left_join(item)
        .on(woi.custom_consumed_item_code == item.name and woi.item_code == item.name)
		.join(stock)
        .on(wo.name == stock.work_order)
        .select(
            wo.name,
            wo.status,
            wo.production_item,
            wo.qty,
            wo.produced_qty,
            woi.item_code,
            woi.item_name,
            woi.required_qty,
            woi.transferred_qty,
            woi.consumed_qty,
            woi.custom_consumed_item_code.as_("raw_code"),
            item.stock_uom.as_("uom"),
            woi.rate,
            wo.creation,
            stock.posting_date
        )
        .where(
            (wo.docstatus == 1)
            & (stock.posting_date.between(filters.from_date, filters.to_date))
            & ((wo.status == "Completed") | (wo.status == "Stopped") | (wo.status == "In Process"))
             &(stock.stock_entry_type == "Manufacture")
        )
    )
    
    if work_order:
        query = query.where(wo.name == work_order)
    if production_item:
        query = query.where(wo.production_item == production_item)
    if status:
        query = query.where(wo.status == status)

    return query.run(as_dict=True)

def get_sum_work_order_data(filters):
    from_date = filters.get('from_date')
    to_date = filters.get('to_date')
    
    data_query = f"""
        SELECT wo.name,
        SUM(woi.required_qty) AS "qty",
        SUM(woi.consumed_qty) AS "consumed_qty"
        FROM `tabWork Order` wo 
        JOIN `tabWork Order Item` woi ON wo.name = woi.parent 
        JOIN `tabStock Entry` se ON wo.name = se.work_order
        WHERE wo.docstatus = 1
        AND (wo.status = "Completed" OR wo.status = "Stopped" OR wo.status = "In Process")
        AND se.posting_date BETWEEN '{from_date}' AND '{to_date}'
        GROUP BY wo.name
    """

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


def get_filter_condition(report_filters):
	filters = {
		"docstatus": 1,
		"status": ("in", ["In Process", "Completed", "Stopped"]),
		"creation": ("between", [report_filters.from_date, report_filters.to_date]),
	}

	for field in ["name", "production_item", "company", "status"]:
		value = report_filters.get(field)
		if value:
			key = f"{field}"
			filters.update({key: value})

	return filters