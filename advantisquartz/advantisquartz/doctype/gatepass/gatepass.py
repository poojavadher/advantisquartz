# Copyright (c) 2023, pooja@sanskartechnolab.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class GatePass(Document):
	def before_submit(self):
		if self.select_type == "Visitor":
			owner_name = frappe.session.user
			self.approved_by = owner_name

	def on_submit(self):
		if self.select_type == "Employee" and self.workflow_state == "Approved":
			try:
				self.out_time = frappe.utils.now()
				self.save()
				self.reload()
			except Exception as e:
				frappe.msgprint(f"Error: {str(e)}")
