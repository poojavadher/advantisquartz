# Copyright (c) 2023, pooja@sanskartechnolab.com and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns(filters)
	finish_data = get_finish_data(filters)
	raw_material_data = get_raw_material_data(filters)
	data = []
	for finished_data in finish_data:
     for repack_data in raw_material_data:
             data.append({
			"fg_item_code":finished_data.fg_item_code,
			"fg_item_name":finished_data.fg_item_name,
			"manufacture_date":finished_data.manufacture_date,
			"use_material_code":finished_data.use_material_code,
  			"use_material_name":finished_data.use_material_name
		})
	return columns, data



def get_columns(filter=None):
    columns =[
		{"label": _("FG Item name "), "fieldname": "fg_item_name", "fieldtype": "Data"},
		{"label": _("FG Item code  "), "fieldname": "fg_item_code", "fieldtype": "Link","options":"Item"},
		{"label": _("Manufaturing date "), "fieldname": "manufacture_date", "fieldtype": "Date"},
		{"label": _("use material code"), "fieldname": "use_material_code", "fieldtype": "Link","options":"Item"},
		{"label": _("use material name "), "fieldname": "use_material_name", "fieldtype": "Data"},
		{"label": _("repack Material code "), "fieldname": "repack_material_code", "fieldtype": "Link","options":"Item"},
		{"label": _("repack Material name "), "fieldname": "repack_material_name", "fieldtype": "Data"},
		{"label": _("repack Material date "), "fieldname": "repack_material_date", "fieldtype": "Date"},
		{"label": _("repack Material brand name "), "fieldname": "repack_material_brand_name", "fieldtype": "Data"}
	

	]
    
    return columns

def get_finish_data(filters):
    query = (
        f"""
        SELECT 
            
            (CASE WHEN  sed.is_finished_item = 1  THEN sed.item_code ELSE "" END) AS 'fg_item_code',
            (CASE WHEN  sed.is_finished_item = 1  THEN sed.item_name ELSE "" END) AS 'fg_item_name',
           (CASE WHEN  sed.t_warehouse IS NOT NULL THEN se.posting_date ELSE "" END) AS 'manufacture_date',
           (CASE WHEN  sed.t_warehouse IS NULL  THEN sed.item_code ELSE "" END) AS 'use_material_code',
            (CASE WHEN  sed.t_warehouse IS NULL  THEN sed.item_name ELSE "" END) AS 'use_material_name'
            FROM
            `tabStock Entry` se JOIN `tabStock Entry Detail` sed on se.name = sed.parent 
            WHERE
            se.docstatus != 0
           and
            se.docstatus != 2
        	and
            se.stock_entry_type = "Manufacture"
         
        """
    )
    main_query = frappe.db.sql(query, as_dict=True)
    return main_query

def get_raw_material_data(filter=None):
    query = (
        f"""
        SELECT 
            
           
           (CASE WHEN  sed.t_warehouse IS NULL  THEN sed.item_code ELSE "" END) AS 'repack_material_code',
            (CASE WHEN  sed.t_warehouse IS NULL  THEN sed.item_name ELSE "" END) AS 'repack_material_name'
            FROM
            `tabStock Entry` se JOIN `tabStock Entry Detail` sed on se.name = sed.parent 
            WHERE
            se.docstatus != 0
           and
            se.docstatus != 2
        	and
            se.stock_entry_type = "Repack"
         
        """
    )
    main_query = frappe.db.sql(query, as_dict=True)
    return main_query