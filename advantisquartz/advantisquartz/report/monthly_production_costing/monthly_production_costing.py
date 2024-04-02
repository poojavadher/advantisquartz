# Copyright (c) 2024, pooja@sanskartechnolab.com and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = [], []
	return columns, data


def get_columns(filters):
    column =[
		{"lable":"Raw Material","fieldname":"raw_material","fieldtype":"Link","options":"Item"}
	]
    
    return column