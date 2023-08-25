# Copyright (c) 2023, pooja@sanskartechnolab.com and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns(filters)
    items = get_item(filters)
    purchases = get_purchase(filters)
    ledgers = get_stock_issue(filters)
    deliver = get_delivery_issue(filters)
    before_purchases = get_before_month_purchase(filters)
    before_issues = get_before_month_issue(filters)
    before_deliver = get_before_month_delivery_issue(filters)
    
    data = []
    
    # Create a dictionary for each item to accumulate relevant data
    item_data_dict = {}
    
    # Iterate over purchases and populate the dictionary
    for purchase_item in purchases:
        item_code = purchase_item.itemCode
        if item_code not in item_data_dict:
            item_data_dict[item_code] = {
                "purchase_qty": 0,
                "item_issue_qty": 0,
                "before_issue_qty": 0,
                "before_purchase_qty": 0,
                "before_delivery_issue_qty":0
            }
        item_data_dict[item_code]["purchase_qty"] += purchase_item.purchase_qty
    
    # Iterate over ledgers and delivers to accumulate item issue quantity
    for ledger in ledgers:
        item_code = ledger.itemCode
        if item_code in item_data_dict:
            item_data_dict[item_code]["item_issue_qty"] += ledger.issue_qty
    for deliver_item in deliver:
        item_code = deliver_item.itemCode
        if item_code in item_data_dict:
            item_data_dict[item_code]["item_issue_qty"] += deliver_item.deliver_qty
    for before_purchase in before_purchases:
        item_code = before_purchase.itemCode
        if item_code in item_data_dict:
            item_data_dict[item_code]["before_purchase_qty"] += before_purchase.bmp_qty
    for before_issuess in before_issues:
        item_code = before_issuess.itemCode
        if item_code in item_data_dict:
            item_data_dict[item_code]["before_issue_qty"] += before_issuess.issue_qty
    for before_delivery in before_deliver:
        item_code = before_delivery.itemCode
        if item_code in item_data_dict:
            item_data_dict[item_code]["before_delivery_issue_qty"] += before_delivery.issue_qty
            
    # Continue similar accumulation for other sets of data

    # Iterate over items to generate the final report data
    for item in items:
        item_code = item.item_code
        if item_code in item_data_dict:
            item_issue_qty = item_data_dict[item_code]["item_issue_qty"]
            before_issue_qty = item_data_dict[item_code]["before_issue_qty"]
            before_purchase_qty = item_data_dict[item_code]["before_purchase_qty"]  
            before_delivery_issue_qty = item_data_dict[item_code]["before_delivery_issue_qty"]
            before_delivery_issue_qty_sum = before_delivery_issue_qty + before_issue_qty
            opening_qty = before_purchase_qty - before_delivery_issue_qty_sum
            closing_qty_pre = opening_qty + item_data_dict[item_code]["purchase_qty"]
            closing_qty = closing_qty_pre - item_issue_qty
            
            data.append({
                "item_code": item_code,
                "item_name": item.item_name,
                "stock_uom": item.stock_uom,
                "purchase_qty": item_data_dict[item_code]["purchase_qty"],
                "issue_qty": item_issue_qty,
                "opening_qty": opening_qty,
                "closing_qty": closing_qty
            })
    
    return columns, data
    


def get_columns(filters):
    columns = [

		{"label": _("Item Code"), "fieldname": "item_code", "fieldtype": "Link", "options":"Item"},
		{"label": _("Item Name"), "fieldname": "item_name", "fieldtype": "Data"},
        {"label": _("Unit"), "fieldname": "stock_uom", "fieldtype": "Link", "options":"UOM"},
        {"label": _("Opening Qty"), "fieldname": "opening_qty", "fieldtype": "Float"},
        {"label": _("Purchase Qty"), "fieldname": "purchase_qty", "fieldtype": "Float"},
        {"label": _("Issue Qty"), "fieldname": "issue_qty", "fieldtype": "Float"},
        {"label": _("Closing  Qty"), "fieldname": "closing_qty", "fieldtype": "Float"},
	]
    return columns



def get_item(filters):
    item = frappe.qb.DocType("Item")
    query = (
        frappe.qb.from_(item)
        .select(
			item.item_code,
			item.item_name,
            item.stock_uom
   
		)
        )
    return query.run(as_dict= True)

def get_purchase(filters):
    query = (
        f"""
        SELECT 
            its.item_code AS 'itemCode',
            its.item_name AS 'itemName',
            SUM(its.qty) AS 'purchase_qty'
        FROM
            `tabPurchase Receipt` it
        JOIN
            `tabPurchase Receipt Item` its ON it.name = its.parent
        WHERE
            it.status != "Draft"
            AND YEAR(it.posting_date) = {filters.get("year")}
            AND MONTH(it.posting_date) = {filters.get("month")}
        GROUP BY
            its.item_code
        """
    )
    main_query = frappe.db.sql(query, as_dict=True)
    return main_query

def get_issue(filters):
    query = (
        f"""
        SELECT 
            it.item_code AS 'itemCode',
            ABS(SUM(CASE WHEN it.dependant_sle_voucher_detail_no IS NULL THEN it.actual_qty ELSE 0 END)) AS 'issue_qty'
        FROM
            `tabStock Ledger Entry` it
       
        WHERE
            it.actual_qty < 0
            AND YEAR(it.posting_date) = {filters.get("year")}
            AND MONTH(it.posting_date) = {filters.get("month")}
        GROUP BY
            it.item_code
        """
    )
    main_query = frappe.db.sql(query, as_dict=True)
    return main_query


def get_stock_issue(filters):
    query = (
        f"""
        SELECT 
            sed.item_code AS 'itemCode',
            SUM((CASE WHEN  sed.t_warehouse IS NULL THEN sed.qty ELSE 0 END)) AS 'issue_qty'
            FROM
            `tabStock Entry` se JOIN `tabStock Entry Detail` sed on se.name = sed.parent 
            WHERE
            se.docstatus != "Draft"
            and
            se.docstatus != "Cancelled"
            AND YEAR(se.posting_date) = {filters.get("year")}
            AND MONTH(se.posting_date) = {filters.get("month")}
            GROUP BY
            sed.item_code
        """
    )
    main_query = frappe.db.sql(query, as_dict=True)
    return main_query

def get_delivery_issue(filters):
    query = (
        f"""
        SELECT 
            sed.item_code AS 'itemCode',
            SUM(sed.qty) AS 'deliver_qty'
            FROM
            `tabDelivery Note` se JOIN `tabDelivery Note Item` sed on se.name = sed.parent 
            WHERE
            se.docstatus != "Draft"
            and
            se.docstatus != "Cancelled"
            AND YEAR(se.posting_date) = {filters.get("year")}
            AND MONTH(se.posting_date) = {filters.get("month")}
             GROUP BY
            sed.item_code
        """
    )
    main_query = frappe.db.sql(query, as_dict=True)
    return main_query
def get_before_month_purchase(filters):
    query = (
        f"""
        SELECT 
            its.item_code AS 'itemCode',
            its.item_name AS 'itemName',
            SUM(CASE WHEN MONTH(it.posting_date) < {filters.get("month")} THEN its.qty ELSE 0 END) AS 'bmp_qty'
        FROM
            `tabPurchase Receipt` it
        JOIN
            `tabPurchase Receipt Item` its ON it.name = its.parent
        WHERE
            it.status != "Draft"
            AND 
            it.status != "Cancelled"
            AND YEAR(it.posting_date) = {filters.get("year")}
        GROUP BY
            its.item_code
        """
    )
    main_query = frappe.db.sql(query, as_dict=True)
    return main_query

def get_before_month_issue(filters):
    query = (
       f"""
        SELECT 
            sed.item_code AS 'itemCode',
            SUM((CASE WHEN MONTH(se.posting_date) < {filters.get("month")} AND  sed.t_warehouse IS NULL THEN sed.qty ELSE 0 END)) AS 'issue_qty'
            FROM
            `tabStock Entry` se JOIN `tabStock Entry Detail` sed on se.name = sed.parent 
            WHERE
            se.docstatus != "Draft"
            and
            se.docstatus != "Cancelled"
            AND YEAR(se.posting_date) = {filters.get("year")}
            
            GROUP BY
            sed.item_code
        """
    )
    main_query = frappe.db.sql(query, as_dict=True)
    return main_query

def get_before_month_delivery_issue(filters):
    query = (
       f"""
        SELECT 
            sed.item_code AS 'itemCode',
            SUM((CASE WHEN MONTH(se.posting_date) < {filters.get("month")} IS NULL THEN sed.qty ELSE 0 END)) AS 'issue_qty'
            FROM
            `tabDelivery Note` se JOIN `tabDelivery Note Item` sed on se.name = sed.parent 
            WHERE
            se.docstatus != "Draft"
            and
            se.docstatus != "Cancelled"
            AND YEAR(se.posting_date) = {filters.get("year")}
            
            GROUP BY
            sed.item_code
        """
    )
    main_query = frappe.db.sql(query, as_dict=True)
    return main_query