# Copyright (c) 2023, pooja@sanskartechnolab.com and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class GateEntry(Document):
	def before_save(self):
		doc = self
		if doc.entry_type == "Inward" and doc.purpose == 'Raw Material':
			if doc.gate_in_date:
				doc.in_operation = "Gate In"
			if doc.gate_in_date and doc.is_weight_in == 1:
				doc.in_operation = "Weighment"
			if doc.gate_in_date and doc.is_weight_in == 1 and doc.sampling_done == 1:
				doc.in_operation = "Sampling"
			if doc.gate_in_date and doc.is_weight_in == 1 and doc.sampling_done and doc.qc_details:
				doc.in_operation = "Quality Check"
			if doc.gate_in_date and doc.is_weight_in == 1 and doc.sampling_done and doc.qc_details and doc.grn == 1:
				doc.in_operation = "GRN"
			if doc.gate_in_date and doc.is_weight_in == 1 and doc.sampling_done and doc.qc_details and doc.is_unloaded == 1:
				doc.in_operation = "Unloading"
			if doc.gate_in_date and doc.is_weight_in == 1 and doc.sampling_done and doc.qc_details and doc.is_unloaded == 1 and doc.net_weight:
				doc.in_operation = "Tare Weight"
			if doc.gate_in_date and doc.is_weight_in == 1 and doc.sampling_done and doc.qc_details and doc.is_unloaded == 1 and doc.net_weight and doc.is_gate_out:
				doc.in_operation = "Gate Out"

