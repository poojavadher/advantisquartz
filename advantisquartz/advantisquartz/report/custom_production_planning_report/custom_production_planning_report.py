
import frappe
from frappe import _
from pypika import Order

from erpnext.stock.doctype.warehouse.warehouse import get_child_warehouses


def execute(filters=None):
	return ProductionPlanReport(filters).execute_report()

 
class ProductionPlanReport(object):
	def __init__(self, filters=None):
		self.filters = frappe._dict(filters or {})
		self.raw_materials_dict = {}
		self.data = []

	def execute_report(self):
		self.get_open_orders()
		self.get_raw_materials()
		self.get_item_details()
		self.get_bin_details()
		self.get_purchase_details()
		self.prepare_data()
		self.get_columns()

		return self.columns, self.data

	def get_open_orders(self):
		doctype, order_by = self.filters.based_on, self.filters.order_by

		parent = frappe.qb.DocType(doctype)
		query = None

	
		if doctype == "Work Order":
			query = (
				frappe.qb.from_(parent)
				.select(
					parent.production_item,
					parent.item_name.as_("production_item_name"),
					parent.planned_start_date,
					parent.stock_uom,
					parent.qty.as_("qty_to_manufacture"),
					parent.name,
					parent.bom_no,
					parent.fg_warehouse.as_("warehouse"),
				)
				.where(parent.status.notin(["Completed", "Stopped", "Closed"]))
			)
			

			
			if order_by == "Planned Start Date":
				query = query.orderby(parent.planned_start_date, order=Order.asc)

			if self.filters.docnames:
				query = query.where(parent.name.isin(self.filters.docnames))

		else:
			child = frappe.qb.DocType(f"{doctype} Item")
			query = (
				frappe.qb.from_(parent)
				.from_(child)
				.select(
					child.bom_no,
					child.stock_uom,
					child.warehouse,
					child.parent.as_("name"),
					
					child.item_code.as_("production_item"),
					child.stock_qty.as_("qty_to_manufacture"),
					child.item_name.as_("production_item_name"),
					
				)
				.where(parent.name == child.parent)
			)

			if self.filters.docnames:
				query = query.where(child.parent.isin(self.filters.docnames))

			if doctype == "Sales Order":
				query = query.select(child.delivery_date, parent.base_grand_total,).where(
					(child.stock_qty > child.produced_qty)
					& (parent.per_delivered < 100.0)
					& (parent.status.notin(["Completed", "Closed"]))
				)

				if order_by == "Delivery Date":
					query = query.orderby(child.delivery_date, order=Order.asc)
				elif order_by == "Total Amount":
					query = query.orderby(parent.base_grand_total, order=Order.desc)

			elif doctype == "Material Request":
				query = query.select(child.schedule_date,).where(
					(parent.per_ordered < 100)
					& (parent.material_request_type == "Manufacture")
					& (parent.status != "Stopped")
				)

				if order_by == "Required Date":
					query = query.orderby(child.schedule_date, order=Order.asc)
		query = query.where(parent.docstatus == 1)

		if self.filters.company:
			query = query.where(parent.company == self.filters.company)

		self.orders = query.run(as_dict=True)
  
	def get_picked_qty(self):
		picked_qty_dict = {}
		if self.filters.based_on == "Sales Order":
			sales_order_names = [d.name for d in self.orders]
			for sales_order_name in sales_order_names:
				picked_qty = frappe.db.sql(
					"""
					SELECT item_code, SUM(picked_qty) as picked_qty, qty as sales_qty
					FROM `tabSales Order Item`
					WHERE parent = %s
					GROUP BY item_code
					""",
					sales_order_name,
					as_dict=True,
				)
				
				picked_qty_dict[sales_order_name] = {d.item_code: d.picked_qty for d in picked_qty}
    
				packing_list_creation_date = frappe.db.get_value("Packing list", {"sales_order": sales_order_name}, "creation")
				packing_list_date = packing_list_creation_date.date() if packing_list_creation_date else None
				picked_qty_dict[sales_order_name]['packing_list_date'] = packing_list_date
    
				production_plan_creation_date = frappe.db.get_value("Work Order", {"sales_order": sales_order_name}, "planned_start_date")
				production_list_date = production_plan_creation_date.date() if production_plan_creation_date else None
				picked_qty_dict[sales_order_name]['production_list_date'] = production_list_date
    
				production_actual_creation_date = frappe.db.get_value("Work Order", {"sales_order": sales_order_name}, "actual_start_date")
				production_actual_date = production_actual_creation_date.date() if production_actual_creation_date else None
				picked_qty_dict[sales_order_name]['production_actual_date'] = production_actual_date
				
				production_qty_list = frappe.db.get_value("Work Order",{"sales_order":sales_order_name},"produced_qty")
				production_qty = production_qty_list if production_qty_list else None
				picked_qty_dict[sales_order_name]['production_qty'] = production_qty

		
		
			
		return picked_qty_dict

	def get_raw_materials(self):
		if not self.orders:
			return
		self.warehouses = [d.warehouse for d in self.orders]
		self.item_codes = [d.production_item for d in self.orders]
		print("\n\n\n",self.orders,"\n\n\n")
		if self.filters.based_on == "Work Order":
			work_orders = [d.name for d in self.orders]

			raw_materials = (
				frappe.get_all(
					"Work Order Item",
					fields=[
						"parent",
						"item_code",
						"item_name as raw_material_name",
						"source_warehouse as warehouse",
						"required_qty",
					],
					filters={"docstatus": 1, "parent": ("in", work_orders), "source_warehouse": ("!=", "")},
				)
				or []
			)
			self.warehouses.extend([d.source_warehouse for d in raw_materials])
			
		else:
			bom_nos = []

			for d in self.orders:
				bom_no = d.bom_no or frappe.get_cached_value("Item", d.production_item, "default_bom")

				if not d.bom_no:
					d.bom_no = bom_no

				bom_nos.append(bom_no)

			bom_item_doctype = (
				"BOM Explosion Item" if self.filters.include_subassembly_raw_materials else "BOM Item"
			)

			bom = frappe.qb.DocType("BOM")
			bom_item = frappe.qb.DocType(bom_item_doctype)

			if self.filters.include_subassembly_raw_materials:
				qty_field = bom_item.qty_consumed_per_unit
			else:
				qty_field = bom_item.qty / bom.quantity

			raw_materials = (
				frappe.qb.from_(bom)
				.from_(bom_item)
				.select(
					bom_item.parent,
					bom_item.item_code,
					bom_item.item_name.as_("raw_material_name"),
					qty_field.as_("required_qty_per_unit"),
				)
				.where((bom_item.parent.isin(bom_nos)) & (bom_item.parent == bom.name) & (bom.docstatus == 1))
			).run(as_dict=True)
			
		if not raw_materials:
			return

		self.item_codes.extend([d.item_code for d in raw_materials])

		for d in raw_materials:
			if d.parent not in self.raw_materials_dict:
				self.raw_materials_dict.setdefault(d.parent, [])

			rows = self.raw_materials_dict[d.parent]
			rows.append(d)
		
		
	def get_item_details(self):
		if not (self.orders and self.item_codes):
			return

		self.item_details = {}
		for d in frappe.get_all(
			"Item Default",
			fields=["parent", "default_warehouse"],
			filters={"company": self.filters.company, "parent": ("in", self.item_codes)},
		):
			self.item_details[d.parent] = d
		
	def get_bin_details(self):
		if not (self.orders and self.raw_materials_dict):
			return

		self.bin_details = {}
		self.mrp_warehouses = []
		if self.filters.raw_material_warehouse:
			self.mrp_warehouses.extend(get_child_warehouses(self.filters.raw_material_warehouse))
			self.warehouses.extend(self.mrp_warehouses)

		for d in frappe.get_all(
			"Bin",
			fields=["warehouse", "item_code", "actual_qty", "ordered_qty", "projected_qty"],
			filters={"item_code": ("in", self.item_codes), "warehouse": ("in", self.warehouses)},
		):
			key = (d.item_code, d.warehouse)
			if key not in self.bin_details:
				self.bin_details.setdefault(key, d)
		
	def get_purchase_details(self):
		if not (self.orders and self.raw_materials_dict):
			return

		self.purchase_details = {}

		purchased_items = frappe.get_all(
			"Purchase Order Item",
			fields=["item_code", "min(schedule_date) as arrival_date", "qty as arrival_qty", "warehouse"],
			filters={
				"item_code": ("in", self.item_codes),
				"warehouse": ("in", self.warehouses),
				"docstatus": 1,
			},
			group_by="item_code, warehouse",
		)
		for d in purchased_items:
			key = (d.item_code, d.warehouse)
			if key not in self.purchase_details:
				self.purchase_details.setdefault(key, d)
		
	def prepare_data(self):
		picked_qty_dict = self.get_picked_qty()
		if not self.orders:
			return

		for d in self.orders:
			key = d.name if self.filters.based_on == "Work Order" else d.bom_no

			if not self.raw_materials_dict.get(key):
				continue

			bin_data = self.bin_details.get((d.production_item, d.warehouse)) or {}
			
			d.update({"for_warehouse": d.warehouse, "available_qty": 0})

			if bin_data and bin_data.get("actual_qty") > 0 and d.qty_to_manufacture:
				d.available_qty = (
					bin_data.get("actual_qty")
					if (d.qty_to_manufacture > bin_data.get("actual_qty"))
					else d.qty_to_manufacture
				)

				bin_data["actual_qty"] -= d.available_qty
			
			picked_qty = picked_qty_dict.get(d.name, {}).get(d.production_item, 0)
			d.reserve_stock = picked_qty
			d.pending_to_be_produce = d.qty_to_manufacture - d.reserve_stock
			d.bom = d.bom_no
			
			packing_list_date = picked_qty_dict.get(d.name, {}).get('packing_list_date')
			d.packing_list_date = packing_list_date
   
			production_list_date = picked_qty_dict.get(d.name,{}).get('production_list_date')
			d.production_planning_date = production_list_date
   
			production_actual_date = picked_qty_dict.get(d.name,{}).get('production_actual_date')
			d.production_actual_date = production_actual_date
   
			production_qty = picked_qty_dict.get(d.name,{}).get('production_qty')
			d.production_qty = production_qty
			self.update_raw_materials(d, key)
			
	def update_raw_materials(self, data, key):
		self.index = 0
		self.raw_materials_dict.get(key)

		warehouses = self.mrp_warehouses or []
		for d in self.raw_materials_dict.get(key):
			if self.filters.based_on != "Work Order":
				d.required_qty = d.required_qty_per_unit * data.qty_to_manufacture
				
			if not warehouses:
				warehouses = [data.warehouse]

			if self.filters.based_on == "Work Order" and d.warehouse:
				warehouses = [d.warehouse]
			else:
				item_details = self.item_details.get(d.item_code)
				if item_details:
					warehouses = [item_details["default_warehouse"]]

			if self.filters.raw_material_warehouse:
				warehouses = get_child_warehouses(self.filters.raw_material_warehouse)
			
			d.remaining_qty = d.required_qty
			self.pick_materials_from_warehouses(d, data, warehouses)

			if (
				d.remaining_qty and self.filters.raw_material_warehouse and d.remaining_qty != d.required_qty
			):
				row = self.get_args()
				d.warehouse = self.filters.raw_material_warehouse
				d.required_qty = d.remaining_qty
				d.allotted_qty = 0
				row.update(d)
				self.data.append(row)
			
	def pick_materials_from_warehouses(self, args, order_data, warehouses):
		for index, warehouse in enumerate(warehouses):
			if not args.remaining_qty:
				return

			row = self.get_args()

			key = (args.item_code, warehouse)
			bin_data = self.bin_details.get(key)

			if bin_data:
				row.update(bin_data)

			args.allotted_qty = 0
			if bin_data and bin_data.get("actual_qty") > 0:
				args.allotted_qty = (
					bin_data.get("actual_qty")
					if (args.required_qty > bin_data.get("actual_qty"))
					else args.required_qty
				)

				args.remaining_qty -= args.allotted_qty
				bin_data["actual_qty"] -= args.allotted_qty

			if (
				self.mrp_warehouses and (args.allotted_qty or index == len(warehouses) - 1)
			) or not self.mrp_warehouses:
				if not self.index:
					row.update(order_data)
					self.index += 1

				args.warehouse = warehouse
				row.update(args)
				if self.purchase_details.get(key):
					row.update(self.purchase_details.get(key))

				self.data.append(row)

	def get_args(self):
		return frappe._dict(
			{
				"work_order": "",
				"sales_order": "",
				"production_item": "",
				"production_item_name": "",
				"qty_to_manufacture": "",
				"produced_qty": "",

			}
		)

	def get_columns(self):
		based_on = self.filters.based_on

		self.columns = [
			{"label": _("ID"), "options": based_on, "fieldname": "name", "fieldtype": "Link", "width": 100},
			{
				"label": _("Item Code"),
				"fieldname": "production_item",
				"fieldtype": "Link",
				"options": "Item",
				"width": 120,
			},
			{
				"label": _("Item Name"),
				"fieldname": "production_item_name",
				"fieldtype": "Data",
				"width": 130,
			},
			{
				"label": _("Warehouse"),
				"options": "Warehouse",
				"fieldname": "for_warehouse",
				"fieldtype": "Link",
				"width": 100,
			},
			{"label": _("Order Qty"), "fieldname": "qty_to_manufacture", "fieldtype": "Float", "width": 80},
			{"label": _("Available Stock"), "fieldname": "available_qty", "fieldtype": "Float", "width": 80},
			{"label": _("Reserve Stock against order"), "fieldname": "reserve_stock", "fieldtype": "Float", "width": 80},
			{"label": _("Packing List Date"), "fieldname": "packing_list_date", "fieldtype": "Date", "width": 80},
   			{"label": _("Pending to Be Produce"), "fieldname": "pending_to_be_produce", "fieldtype": "Float", "width": 80},
   			{"label": _("BOM"),"options": "BOM","fieldname": "bom","fieldtype": "Link","width": 100,},
      		{"label": _("Production Planning Date"), "fieldname": "production_planning_date", "fieldtype": "Date", "width": 80},
        {"label": _("Production Actual Date"), "fieldname": "production_actual_date", "fieldtype": "Date", "width": 80},
        {"label": _("Production Qty"), "fieldname": "production_qty", "fieldtype": "Float", "width": 80},
		]

		fieldname, fieldtype = "delivery_date", "Date"
		if self.filters.based_on == "Sales Order" and self.filters.order_by == "Total Amount":
			fieldname, fieldtype = "base_grand_total", "Currency"
		elif self.filters.based_on == "Material Request":
			fieldname = "schedule_date"
		elif self.filters.based_on == "Work Order":
			fieldname = "planned_start_date"

		self.columns.append(
			{
				"label": _(self.filters.order_by),
				"fieldname": fieldname,
				"fieldtype": fieldtype,
				"width": 100,
			}
		)

		self.columns.extend(
			[
				{
					"label": _("Raw Material Code"),
					"fieldname": "item_code",
					"fieldtype": "Link",
					"options": "Item",
					"width": 120,
				},
				{
					"label": _("Raw Material Name"),
					"fieldname": "raw_material_name",
					"fieldtype": "Data",
					"width": 130,
				},
				{
					"label": _("Warehouse"),
					"options": "Warehouse",
					"fieldname": "warehouse",
					"fieldtype": "Link",
					"width": 110,
				},
				{"label": _("Required Qty"), "fieldname": "required_qty", "fieldtype": "Float", "width": 100},
    			{"label": _("Raw Material Required"), "fieldname": "raw_required_qty", "fieldtype": "Float", "width": 100},
				{"label": _("Allotted Qty"), "fieldname": "allotted_qty", "fieldtype": "Float", "width": 100},
				{
					"label": _("Expected Arrival Date"),
					"fieldname": "arrival_date",
					"fieldtype": "Date",
					"width": 160,
				},
				{
					"label": _("Arrival Quantity"),
					"fieldname": "arrival_qty",
					"fieldtype": "Float",
					"width": 140,
				},
			]
		)


# # Copyright (c) 2023, pooja@sanskartechnolab.com and contributors
# # For license information, please see license.txt

# # import frappe


# # def execute(filters=None):
# # 	columns, data = [], []
# # 	return columns, data


# import frappe
# import math
# from datetime import datetime, timedelta
# from dateutil.relativedelta import relativedelta

# def execute(filters=None):
#     columns = [
# 		{
#             "label": "Sales Order", 
#             "fieldname": "sales_order", 
#             "fieldtype": "Data", 
#             "width": 100
#         },
#         {
#             "label": "Item Code",
#             "fieldname": "item_code",
#             "fieldtype": "Data",
#             "width": 100
#         },
#         {
#             "label": "Item Name",
#             "fieldname": "item_name",
#             "fieldtype": "Data",
#             "width": 100
#         },
#         {
#             "label": "Warehouse",
#             "fieldname": "warehouse",
#             "fieldtype": "Data",
#             "width": 100
#         },
#         {
#             "label": "Order Qty",
#             "fieldname": "order_qty",
#             "fieldtype": "Data",
#             "width": 100
#         },
#         {
#             "label": "Planned Delivery Date",
#             "fieldname": "planned_delivery_date",
#             "fieldtype": "Data",
#             "width": 100
#         },
#         {
#             "label": "Available Stock",
#             "fieldname": "available_stock",
#             "fieldtype": "Data",
#             "width": 100
#         },
#         {
#             "label": "Reserve Stock against order",
#             "fieldname": "reserve_stock_against_order",
#             "fieldtype": "Data",
#             "width": 100
#         },
#         {
#             "label": "Packing List Date",
#             "fieldname": "packing_list_date",
#             "fieldtype": "Data",
#             "width": 100
#         },
#         {
#             "label": "Pending to Be Produce",
#             "fieldname": "pending_to_be_produce",
#             "fieldtype": "Data",
#             "width": 100
#         },
#         {
#             "label": "BOM",
#             "fieldname": "bom",
#             "fieldtype": "Data",
#             "width": 100
#         },
#         {
#             "label": "Production Planning Date",
#             "fieldname": "production_planning_date",
#             "fieldtype": "Data",
#             "width": 100
#         },
#         {
#             "label": "Production Actual Date",
#             "fieldname": "production_actual_date",
#             "fieldtype": "Data",
#             "width": 100
#         },
#         {
#             "label": "Production Qty",
#             "fieldname": "production_qty",
#             "fieldtype": "Data",
#             "width": 100
#         },
#         {
#             "label": "Raw Material Required",
#             "fieldname": "raw_material_required",
#             "fieldtype": "Data",
#             "width": 100
#         },
#         {
#             "label": "Raw Material Available",
#             "fieldname": "raw_material_available",
#             "fieldtype": "Data",
#             "width": 100
#         },
#         {
#             "label": "RM to be Procurred",
#             "fieldname": "rm_to_be_procurred",
#             "fieldtype": "Data",
#             "width": 100
#         },
#         {
#             "label": "RM Arrival Expected Date",
#             "fieldname": "rm_arrival_expected_date",
#             "fieldtype": "Data",
#             "width": 100
#         },
#         {
#             "label": "RM Arrival Date",
#             "fieldname": "rm_arrival_date",
#             "fieldtype": "Data",
#             "width": 100
#         },
#         {
#             "label": "Press Date",
#             "fieldname": "press_date",
#             "fieldtype": "Data",
#             "width": 100
#         },
#         {
#             "label": "Polish Date",
#             "fieldname": "polish_date",
#             "fieldtype": "Data",
#             "width": 100
#         },
#         {
#             "label": "QC Date",
#             "fieldname": "qc_date",
#             "fieldtype": "Data",
#             "width": 100
#         },
#         {
#             "label": "FG Qty after QC",
#             "fieldname": "fg_qty_after_qc",
#             "fieldtype": "Data",
#             "width": 100
#         }
#     ]

#     data = []
    
#     data.append({
#         "sales_order": "8716723418394", 
#         "item_code": "abc",
#         "item_name": "",
#         "warehouse": "",
#         "order_qty": "",
#         "planned_delivery_date": "",
#         "available_stock": "",
#         "reserve_stock_against_order": "",
#         "packing_list_date": "",
#         "pending_to_be_produce": "",
#         "bom": "",
#         "production_planning_date": "",
#         "production_actual_date": "",
#         "production_qty": "",
#         "raw_material_required": "",
#         "raw_material_available": "",
#         "rm_to_be_procurred": "",
# 		"rm_arrival_expected_date": "",
# 		"rm_arrival_date": "",
# 		"press_date": "",
# 		"polish_date": "",
# 		"qc_date": "",
# 		"fg_qty_after_qc": ""
#     })

#     return columns, data

    
 
    
 