# Copyright (c) 2023, pooja@sanskartechnolab.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Packinglist(Document):
	def before_save(self):
		for item in self.items:
			serial_doc = frappe.get_doc('Serial No', item.serial_no)
			if serial_doc.status != "Hold":
				frappe.db.set_value('Serial No',item.serial_no,{
						"status":"Hold",
						"serial_type":"",
						"packing_list":self.name
					})
		frappe.msgprint("Following Items Are Now Hold Against This Order")

	def before_cancel(self):
		for item in self.items:
			serial_doc = frappe.get_doc('Serial No', item.serial_no)
			if serial_doc.status == "Hold":
				frappe.db.set_value('Serial No',item.serial_no,{
						"status":"Active",
						"serial_type":"",
						"packing_list":""
					})

