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
    before_stock = get_before_month_stock_reconciliation(filters)
    stock_rec = get_stock_reconciliation(filters)
    data = []
    
    # Create a dictionary for each item to accumulate relevant data
    item_data_dict = {}
    for item in items:
        item_code = item.item_code
        if item_code not in item_data_dict:
            item_data_dict[item_code] = {
                "purchase_qty": 0,
                "item_issue_qty": 0,
                "before_issue_qty": 0,
                "before_purchase_qty": 0,
                "before_delivery_issue_qty":0,
                "before_stock_re_qty":0,
                "stock_re_qty":0,
                "item_receipt_qty":0,
                "before_receipt_qty":0,
                "item_manufacture_qty":0,
                "before_manufacture_qty":0
            }
    # Iterate over purchases and populate the dictionary
    for purchase_item in purchases:
        item_code = purchase_item.itemCode
        item_data_dict[item_code]["purchase_qty"] += purchase_item.purchase_qty
    
    # Iterate over ledgers and delivers to accumulate item issue quantity
    for ledger in ledgers:
        item_code = ledger.itemCode
        if item_code in item_data_dict:
            item_data_dict[item_code]["item_issue_qty"] += ledger.issue_qty
            item_data_dict[item_code]["item_receipt_qty"] += ledger.receipt_qty
            item_data_dict[item_code]["item_manufacture_qty"] += ledger.manufacture_qty
        
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
            item_data_dict[item_code]["before_receipt_qty"] += before_issuess.receipt_qty
            item_data_dict[item_code]["before_manufacture_qty"] += before_issuess.manufacture_qty
            
    for before_delivery in before_deliver:
        item_code = before_delivery.itemCode
        if item_code in item_data_dict:
            item_data_dict[item_code]["before_delivery_issue_qty"] += before_delivery.issue_qty
            
    for before_stock_re in before_stock:
        item_code = before_stock_re.itemCode
        if item_code in item_data_dict:
            item_data_dict[item_code]["before_stock_re_qty"] += before_stock_re.stock_re
    
    for stock_rec_sum in stock_rec:
        item_code = stock_rec_sum.itemCode
        if item_code in item_data_dict:
            item_data_dict[item_code]["stock_re_qty"] += stock_rec_sum.stock_re
    # Continue similar accumulation for other sets of data

    # Iterate over items to generate the final report data
    for item in items:
        item_code = item.item_code
        if item_code in item_data_dict:
            item_issue_qty = item_data_dict[item_code]["item_issue_qty"] if item_data_dict[item_code] else 1
            before_issue_qty = item_data_dict[item_code]["before_issue_qty"]
            before_purchase_qty = item_data_dict[item_code]["before_purchase_qty"]  
            before_stock_rec = item_data_dict[item_code]["before_stock_re_qty"] + before_purchase_qty + item_data_dict[item_code]["stock_re_qty"] + item_data_dict[item_code]["before_receipt_qty"] + item_data_dict[item_code]["item_receipt_qty"] + item_data_dict[item_code]["item_manufacture_qty"] + item_data_dict[item_code]["before_manufacture_qty"]
            before_delivery_issue_qty = item_data_dict[item_code]["before_delivery_issue_qty"]
            before_delivery_issue_qty_sum = before_delivery_issue_qty + before_issue_qty
            opening_qty = before_stock_rec - before_delivery_issue_qty_sum 
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
            SUM(its.received_qty) AS 'purchase_qty'
        FROM
            `tabPurchase Receipt` it
        JOIN
            `tabPurchase Receipt Item` its ON it.name = its.parent
        WHERE
            it.status != "Draft"
            AND
            it.status != "Cancelled"
            AND YEAR(it.posting_date) = {filters.get("year")}
            AND MONTH(it.posting_date) = {filters.get("month")}
        GROUP BY
            its.item_code
        """
    )
    main_query = frappe.db.sql(query, as_dict=True)
    return main_query




def get_stock_issue(filters):
    query = (
        f"""
        SELECT 
            sed.item_code AS 'itemCode',
            SUM((CASE WHEN  sed.t_warehouse IS NULL THEN sed.qty ELSE 0 END)) AS 'issue_qty',
            SUM((CASE WHEN  se.stock_entry_type = "Material Receipt" THEN sed.qty ELSE 0 END)) AS 'receipt_qty',
            SUM((CASE WHEN  sed.is_finished_item = 1 THEN sed.qty ELSE 0 END)) AS 'manufacture_qty'
            FROM
            `tabStock Entry` se JOIN `tabStock Entry Detail` sed on se.name = sed.parent 
            WHERE
            se.docstatus != "Draft" 
            and
            se.docstatus != "Cancelled  "
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
            SUM(CASE WHEN MONTH(it.posting_date) < {filters.get("month")} THEN its.received_qty ELSE 0 END) AS 'bmp_qty'
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
            SUM((CASE WHEN MONTH(se.posting_date) < {filters.get("month")} AND  sed.t_warehouse IS NULL THEN sed.qty ELSE 0 END))
            AS 'issue_qty',
            SUM((CASE WHEN  se.stock_entry_type ="Material Receipt" AND MONTH(se.posting_date) < {filters.get("month")} THEN sed.qty ELSE 0 END)) AS 'receipt_qty',
            SUM((CASE WHEN sed.is_finished_item = 1 AND MONTH(se.posting_date)<{filters.get("month")} THEN sed.qty ELSE 0 END)) AS 'manufacture_qty'
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
            SUM((CASE WHEN MONTH(se.posting_date) < {filters.get("month")}  THEN sed.qty ELSE 0 END)) AS 'issue_qty'
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


def get_before_month_stock_reconciliation(filters):
    query = (
       f"""
        SELECT 
            sed.item_code AS 'itemCode',
            SUM((CASE WHEN MONTH(se.posting_date) < {filters.get("month")} THEN sed.qty ELSE 0 END)) AS 'stock_re'
            FROM
            `tabStock Reconciliation` se JOIN `tabStock Reconciliation Item` sed on se.name = sed.parent 
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


def get_stock_reconciliation(filters):
    query = (
       f"""
        SELECT 
            sed.item_code AS 'itemCode',
            SUM(sed.qty ) AS 'stock_re'
            FROM
            `tabStock Reconciliation` se JOIN `tabStock Reconciliation Item` sed on se.name = sed.parent 
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