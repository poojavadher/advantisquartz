# Copyright (c) 2023, pooja@sanskartechnolab.com and contributors
# For license information, please see license.txt
import frappe
from frappe import _



def execute(filters=None):
    columns = get_columns(filters)
    sl_name_entries = get_supplier_name_entries(filters)
    sl_entries = get_buying_purchase_entries(filters)

    data = []
    prev_supplier = None  # Keep track of the previous supplier

    for slm in sl_entries:
        if slm.supplier != prev_supplier:
            data.append({
                "supplier": slm.supplier,
                "item_code": slm.item_code,
                "item_name": slm.item_name,
                "remarks": slm.remarks,
                "sum_order_qty": slm.sum_order_qty,
                "sum_of_rate": slm.sum_of_rate,
                "sum_of_amount": slm.sum_of_amount
            })
            prev_supplier = slm.supplier
        else:
            data.append({
                "item_code": slm.item_code,
                "item_name": slm.item_name,
                "remarks": slm.remarks,
                "sum_order_qty": slm.sum_order_qty,
                "sum_of_rate": slm.sum_of_rate,
                "sum_of_amount": slm.sum_of_amount
            })

    return columns, data

	

def get_columns(filters):
	columns = [
		{"label": _("Supplier Name"), "fieldname": "supplier", "fieldtype": "Link", "options":"Supplier"},
		{
			"label": _("Item Code"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 150,
		},
	
		
	]

	

	columns.extend(
		[
			{
				"label": _("Item Name"),
				"fieldname": "item_name",
				"fieldtype": "Data",
				"width": 80,
			
			},
			{
				"label": _("Remarks"),
				"fieldname": "remarks",
				"fieldtype": "Data",
				"width": 80,
			
			},
			
			{
				"label": _("Sum Of Order Qty"),
				"fieldname": "sum_order_qty",
				"fieldtype": "Float",
				
				"width": 150,
			},
		
			{
				"label": _("Sum Of Rate"),
				"fieldname": "sum_of_rate",
				"fieldtype": "Float",
				
				"width": 180,
			},
   {
				"label": _("Sum Of Amount"),
				"fieldname": "sum_of_amount",
				"fieldtype": "Float",
				
				"width": 180,
			},
			
			
			
			
			
		]
	)

	return columns

def get_supplier_name_entries(filters):
	sle = frappe.qb.DocType("Purchase Order")
	
	query = (
		frappe.qb.from_(sle)
	
		.select(
			sle.supplier,
   
		)
	)
	

	return query.run(as_dict=True)




def get_buying_purchase_entries(filters):
    sle = frappe.qb.DocType("Purchase Order")
    sed = frappe.qb.DocType("Purchase Order Item")
    query = (
        frappe.qb.from_(sle)
        .join(sed)
        .on(sle.name == sed.parent)
        .select(
            sle.supplier,
            sed.item_code,
            sed.item_name,
          
        )
      
    )

    return query.run(as_dict=True)



