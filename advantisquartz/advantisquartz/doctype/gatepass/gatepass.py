# Copyright (c) 2023, pooja@sanskartechnolab.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class GatePass(Document):
	def before_submit(self):
		if self.select_type == "Visitor":
			owner_name = frappe.session.user
			self.approved_by = owner_name

	# def before_update_after_submit(self):
	# 	if self.gate_out == 1:
	# 		self.out_time = frappe.datetime.now_time()
	# 		self.reload()