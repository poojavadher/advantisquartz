# Copyright (c) 2023, pooja@sanskartechnolab.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Packinglist(Document):
	def before_save(self):
		if self.items:
			for item in self.items:
				serial_doc = frappe.get_doc('Serial No', item.serial_no)
				if serial_doc.status != "Hold":
					frappe.db.set_value('Serial No',item.serial_no,{
							"status":"Hold",
							"serial_type":"",
							"packing_list":self.name,
							"custom_sales_grade":item.sales_grade,
							"custom_sales_weight":item.sales_weight,
							"custom_saleable_measurement":item.saleable_measurement,
							"custom_sales_width":item.sales_width,
							"custom_sales_length":item.sales_length
						})
			so_doc = frappe.get_doc('Sales Order', self.sales_order)
			update_picking_status(so_doc)
			frappe.msgprint("Following Items Are Now Hold Against This Order")

	def before_cancel(self):
		for item in self.items:
			serial_doc = frappe.get_doc('Serial No', item.serial_no)
			if serial_doc.status == "Hold":
				frappe.db.set_value('Serial No',item.serial_no,{
						"status":"Active",
						"serial_type":"",
						"packing_list":"",
						"custom_sales_grade":"",
						"custom_sales_weight":0,
						"custom_saleable_measurement":0,
						"custom_sales_width":0,
						"custom_sales_length":0
					})
				
def update_picking_status(so_doc):
		total_picked_qty = 0.0
		total_qty = 0.0
		for so_item in so_doc.items:
			total_picked_qty += float(so_item.picked_qty)
			total_qty += float(so_item.stock_qty)
		per_picked = total_picked_qty / total_qty * 100

		so_doc.db_set("per_picked", float(per_picked), update_modified=False)