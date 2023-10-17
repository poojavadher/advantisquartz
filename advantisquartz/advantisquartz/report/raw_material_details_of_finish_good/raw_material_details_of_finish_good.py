# Copyright (c) 2023, pooja@sanskartechnolab.com and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns(filters)
    finish_data = get_finish_data(filters)
    raw_material_data = get_raw_data(filters)
    raw_repack_data = get_repack_data(filters)
    data = []
    for finished_data in finish_data:
        for raw_item in raw_material_data:
            for repack_item in raw_repack_data:  
                if finished_data.name == raw_item.name:
                    if raw_item.item_code == repack_item.repack_main_material_code and finished_data.posting_date == repack_item.posting_date:         
                        data.append({
			    "fg_item_code":finished_data.item_code,
                "fg_item_name":finished_data.item_name,
                "manufacture_date":finished_data.posting_date,
                "use_material_code":raw_item.item_code,
                "use_material_name":raw_item.item_name,
                "repack_material_name":repack_item.repack_material_names,
                "repack_material_code":repack_item.repack_material_codes,
                "repack_material_date":repack_item.posting_date
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
    sle = frappe.qb.DocType("Stock Entry")
    sed = frappe.qb.DocType("Stock Entry Detail")
    query = (
		frappe.qb.from_(sle)
		.join(sed)
		.on(sle.name == sed.parent)
		.select(
				
			sed.item_name,
			sle.posting_date,
			sed.item_code,
            sle.name
			
		)
		.where(
			(sle.stock_entry_type == "Manufacture")
			&(sed.is_finished_item == 1)
				& (sle.docstatus == 1)
			
		)
		
	)
    return query.run(as_dict=True)

def get_raw_data(filters):
    sle = frappe.qb.DocType("Stock Entry")
    sed = frappe.qb.DocType("Stock Entry Detail")
    query = (
		frappe.qb.from_(sle)
		.join(sed)
		.on(sle.name == sed.parent)
		.select(
			sle.name,	
			sed.item_name,
			sle.posting_date,
			sed.item_code
			
		)
		.where(
			(sle.stock_entry_type == "Manufacture")
			&(sed.s_warehouse != "")
				& (sle.docstatus == 1)
			
		)
		
	)
    return query.run(as_dict=True)




def get_repack_data(filters):
    query = (
        f"""
        SELECT 
            
           
           (CASE WHEN  sed.is_finished_item = 1  THEN sed.item_code ELSE "" END) AS 'repack_main_material_code',
            (CASE WHEN  sed.is_finished_item = 0  THEN sed.item_name ELSE "" END) AS 'repack_material_names',
            (CASE WHEN  sed.is_finished_item = 0 THEN sed.item_code ELSE "" END) AS 'repack_material_codes',
            se.posting_date
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
