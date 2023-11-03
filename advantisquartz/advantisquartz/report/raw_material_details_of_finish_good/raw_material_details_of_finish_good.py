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
                if finished_data.name == raw_item.name and finished_data.item_code == repack_item.fg_good and finished_data.posting_date == repack_item.posting_date:
                    data.append({
                        "fg_item_code": finished_data.item_code,
                        "fg_item_name": finished_data.item_name,
                        "manufacture_date": finished_data.posting_date,
                        "use_material_code": raw_item.item_code,
                        "use_material_name": raw_item.item_name,
                        "repack_material_name": repack_item.repack_material_names,
                        "repack_material_code": repack_item.repack_material_codes,
                        "repack_material_date": repack_item.posting_date,
                        "repack_material_brand_name":repack_item.repack_material_brand_name
                    })
    # Filter out rows where 'repack_material_name' or 'repack_material_code' is empty
    data = [row for row in data if row["repack_material_name"] and row["repack_material_code"]]
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
            sed.item_code,
            sed.item_name,
            se.name,
            se.posting_date
        FROM
            `tabStock Entry` se
        JOIN `tabStock Entry Detail` sed on se.name = sed.parent
        WHERE
            se.docstatus != 0
            AND se.docstatus != 2
            AND se.stock_entry_type = "Manufacture"
            AND sed.is_finished_item = 1
       
        """
    )
    main_query = frappe.db.sql(query, as_dict=True)
    return main_query
    
    
def get_raw_data(filters):
    query = (
        f"""    
        SELECT 
            sed.item_code,
            sed.item_name,
            se.name,
            se.posting_date
        FROM
            `tabStock Entry` se
        JOIN `tabStock Entry Detail` sed on se.name = sed.parent
        WHERE
            se.docstatus != 0
            AND se.docstatus != 2
            AND se.stock_entry_type = "Manufacture"
            AND sed.is_finished_item = 0
        
        """
    )
    main_query = frappe.db.sql(query, as_dict=True)
    return main_query




def get_repack_data(filters):
    query = (
        f"""    
        SELECT 
            (CASE WHEN  sed.is_finished_item = 0  THEN sed.item_name ELSE "" END) AS 'repack_material_names',
            (CASE WHEN  sed.is_finished_item = 0 THEN sed.item_code ELSE "" END) AS 'repack_material_codes' ,
            (CASE WHEN  sed.is_finished_item = 0 THEN sed.brand ELSE "" END) AS 'repack_material_brand_name',
            fg.item_code AS 'fg_good',
            se.posting_date
            FROM
            `tabStock Entry` se JOIN `tabStock Entry Detail` sed on se.name = sed.parent
            JOIN `tabRepack Finish Good` fg on se.name = fg.parent
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