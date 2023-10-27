# Copyright (c) 2023, pooja@sanskartechnolab.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PackingListItem(Document):
	def after_delete(self):
		doc = frappe.get_doc('Serial No', self.serial_no)
		doc.packing_list = " "
		doc.save()
