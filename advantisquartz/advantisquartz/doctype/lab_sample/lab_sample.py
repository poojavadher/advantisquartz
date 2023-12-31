# Copyright (c) 2023, pooja@sanskartechnolab.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

from erpnext.stock.doctype.quality_inspection_template.quality_inspection_template import (
	get_template_details,
)

class LabSample(Document):
	@frappe.whitelist()
	def get_item_specification_details(self):
		if not self.quality_inspection_template:
			return

		self.set("readings", [])
		parameters = get_template_details(self.quality_inspection_template)
		for d in parameters:
			child = self.append("readings", {})
			child.update(d)
			child.status = "Accepted"
	

	@frappe.whitelist()
	def get_quality_inspection_template(self):
		template = ""

		self.quality_inspection_template = template
		self.get_item_specification_details()

	def validate_readings_status_mandatory(self):
		for reading in self.readings:
			if not reading.status:
				frappe.throw(_("Row #{0}: Status is mandatory").format(reading.idx))