# Copyright (c) 2023, pooja@sanskartechnolab.com and contributors
# For license information, please see license.txt
import frappe
from frappe import _



def execute(filters=None):
    columns = get_columns(filters)
    
    sl_entries = get_supplier_name_entries(filters)

    data = []
      # Keep track of the previous supplier

    for slm in sl_entries:
       
            data.append({
                "material_request": slm.name
            })
           
      
    return columns, data

	

def get_columns(filters):
	columns = [
		{"label": _("Indent No"), "fieldname": "material_request", "fieldtype": "Link", "options":"Material Request"},
	
	
		
	]

	

	columns.extend(
		[

			
			
		]
	)

	return columns

def get_supplier_name_entries(filters):
	sle = frappe.qb.DocType("Material Request")
	
	query = (
		frappe.qb.from_(sle)
	
		.select(
			sle.name,
   
		).where(sle.status != "Cancelled")
	)
	

	return query.run(as_dict=True)



