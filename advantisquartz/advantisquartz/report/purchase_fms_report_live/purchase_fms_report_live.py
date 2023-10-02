# Copyright (c) 2023, pooja@sanskartechnolab.com and contributors
# For license information, please see license.txt
import frappe
from frappe import _
from datetime import datetime
from datetime import datetime, timedelta
def execute(filters=None):
    columns = get_columns(filters)
    
    sl_entries = get_material_name_entries(filters)
    purchase_entries = get_purchase_name_entries(filters)
    receipt_entries = get_purchase_receipt_entries(filters)
    cmt_entries = get_modified_comment(filters)
    cmt_purchase_entries = get_purchase_modified_comment(filters)
    quotation_entries = get_quotation_entries(filters)

    data = []
    unique_entries = set()

    for slm in sl_entries:
        entry_key = (slm.name, slm.item_code)  # Create a unique key based on material request and item code
        unique_entries.add(entry_key)

        start_time = slm.creation
        time_difference = None  # Initialize time difference

        # Find matching entries for purchase, receipt, cmt, quotation, and cmt_purchase
        matching_purchase = None
        matching_receipt = None
        matching_cmt = None
        matching_quotation = None
        matching_cmt_purchase = None

        for sl in purchase_entries:
            if slm.name == sl.material_request:
                matching_purchase = sl
                break
        
        for gate in receipt_entries:
            if slm.name == gate.material_request:
                matching_receipt = gate
                break

        for cmt in cmt_entries:
            if slm.name == cmt.reference_name:
                matching_cmt = cmt
                break
        
        for quotation in quotation_entries:
            if slm.name == quotation.material_request:
                matching_quotation = quotation
                break
        
        for po_cmt_entries in cmt_purchase_entries:
            if matching_purchase and matching_purchase.name == po_cmt_entries.reference_name:
                matching_cmt_purchase = po_cmt_entries
                break
            
        if matching_purchase and matching_cmt:
            end_time = matching_cmt.modified
            time_difference = end_time - start_time
        if matching_quotation:
            quotation_starttime = matching_quotation.creation
            quotation_endtime = matching_quotation.modified
            current_date = datetime.now()
            two_days_after_creation = quotation_starttime + timedelta(days=2)
            if quotation_endtime:
                if quotation_endtime > two_days_after_creation:
                    quotation_delay = (quotation_endtime - two_days_after_creation).days
                else:
                    quotation_delay = 0
            elif current_date:
                if current_date > two_days_after_creation:
                    quotation_delay = (current_date -two_days_after_creation)
                                
        # ... Similar logic for other time calculations ...
        if matching_purchase and matching_cmt_purchase:
            purchase_starttime = matching_purchase.creation
            purchase_endtime = matching_cmt_purchase.modified
            current_date = datetime.now()
            one_days_after_creation = purchase_starttime + timedelta(days=1)
    
            if purchase_endtime:
                if purchase_endtime > one_days_after_creation:
                    purchase_delay = (purchase_endtime - one_days_after_creation).days
                else:
                    purchase_delay = 0
            elif current_date:
                if current_date > one_days_after_creation:
                    purchase_delay = (current_date - one_days_after_creation)
                else:
                    purchase_delay = None
        else:
    # Handle the case when either matching_purchase or matching_cmt_purchase is None
            purchase_starttime = None
            purchase_endtime = None
            purchase_delay = None

        
        if matching_receipt:                                
            receipt_starttime = matching_receipt.creation_by
            receipt_endtime = matching_receipt.modification
            current_date = datetime.now()
            two_days_after_creation_by = receipt_starttime + timedelta(days=2)
            if receipt_endtime:
                if receipt_endtime > two_days_after_creation_by:
                    receipt_delay = (receipt_endtime - two_days_after_creation_by).days
                else:
                    receipt_delay = 0
            elif current_date:
                if current_date > two_days_after_creation_by:
                    receipt_delay = (current_date -two_days_after_creation_by)

            quality_starttime= matching_receipt.quality_creation
            quality_endtime = matching_receipt.quality_modified
            current_date = datetime.now()
            if(quality_starttime):
                two_days_after_creation_date = quality_starttime + timedelta(days=2)    
                if quality_endtime:
                    if quality_starttime > two_days_after_creation_date:
                        quality_delays = (quality_endtime - two_days_after_creation_date).days
                    else:
                        quality_delays = 0
            
                elif quality_starttime:
                    if current_date > two_days_after_creation_date:
                        quality_delays =  (current_date -two_days_after_creation_date)
                    else:
                        quality_delays = 0
            else:
                quality_delays = 0
        data.append({
            "material_request": slm.name,
            "purchase_order": matching_purchase.name if matching_purchase else None,
            "gate_entry": matching_receipt.gate_entry if matching_receipt else None,
            "grn_entry": matching_receipt.name if matching_receipt else None,
            "timestamp": slm.transaction_date,
            "indent_require_by": slm.schedule_date,
            "indent_item": slm.item_code,
            "requisition_no": slm.name,
            "available_stock": slm.actual_qty,
            "material_planned": slm.creation,
            "material_actual": matching_cmt.modified if matching_cmt else None, 
            "approval_no": matching_cmt.reference_name if matching_cmt else None,
            "remarks": slm.remarks,
            "time_delay": time_difference,
            "quotation_planned":matching_quotation.creation if matching_quotation else None,
            "quotation_actual":matching_quotation.modified if matching_quotation else None,
            "quotation_link":matching_quotation.name if matching_quotation else None,
            "quotation_status":matching_quotation.status if matching_quotation else None,
            "supplier_quotation_delay":quotation_delay if matching_quotation else None,
            "purchase_planned":matching_purchase.creation if matching_purchase else None,
            "purchase_actual":purchase_endtime,
            "purchase_order_no":matching_purchase.name if matching_purchase else None,
            "gate_planned":matching_receipt.creation if matching_receipt else None,
            "gate_actual":matching_receipt.modified if matching_receipt else None,
            "gate_entry_no":matching_receipt.gate_entry if matching_receipt else None,
            "receipt_planned":matching_receipt.creation_by if matching_receipt else None, 
            "receipt_actual":matching_receipt.modification if matching_receipt else None,
            "purchase_receipt_no":matching_receipt.name if matching_receipt else None,
            "submitted_by":matching_receipt.full_name if matching_receipt else None,
            "purchase_order_time_delay":purchase_delay if purchase_delay else None,
            "receipt_time_delay":receipt_delay if matching_receipt else None, 
            "quality_planned":matching_receipt.quality_creation if matching_receipt else None,
            "quality_actual":matching_receipt.quality_modified if matching_receipt else None,             
            "quality_remarks":matching_receipt.remarks if matching_receipt else None,
            "quality_submitted_by":matching_receipt.inspected_by if matching_receipt else None,
            "quality_delay":quality_delays if matching_receipt else None
           
            # ... Other fields ...
            # ... Other fields ...
        })

    return columns, data


def get_columns(filters):
	columns = [
		{"label": _("Indent No"), "fieldname": "material_request", "fieldtype": "Link", "options":"Material Request"},
        {"label": _("Purchase Order"), "fieldname": "purchase_order", "fieldtype": "Link", "options":"Purchase Order"},
        {"label": _("Gate No"), "fieldname": "gate_entry", "fieldtype": "Link", "options":"Gate Entry"},
        {"label": _("GRN No"), "fieldname": "grn_entry", "fieldtype": "Link", "options":"Purchase Receipt"},
        {"label": _("TimeStamp"), "fieldname": "timestamp", "fieldtype": "Date"},
        {"label": _("Indent Require By"), "fieldname": "indent_require_by", "fieldtype": "Date"},
        {"label": _("Indent Requisition Attachment"), "fieldname": "indent_item", "fieldtype": "Link","options":"Item"},
        {"label": _("Requisition No"), "fieldname": "requisition_no", "fieldtype": "Link","options":"Material Request"},
        {"label": _("Available Stock"), "fieldname": "available_stock", "fieldtype": "Float"},
        {"label": _("Material Planned"), "fieldname": "material_planned", "fieldtype": "Datetime"},
        {"label": _("Material Actual"), "fieldname": "material_actual", "fieldtype": "Datetime"},
        {"label":_("Requisition No For Approval"),"fieldname":"approval_no","fieldtype":"Link","options":"Material Request"},
        {"label":_("Remarks"),"fieldname":"remarks","fieldtype":"Data"},
        {"label": _("Time Delay"), "fieldname": "time_delay", "fieldtype": "Time"},
        {"label": _("Quotation Planned"), "fieldname": "quotation_planned", "fieldtype": "Datetime"},
        {"label": _("Quotation Actual"), "fieldname": "quotation_actual", "fieldtype": "Datetime"},
        {"label": _("Quotation Link"), "fieldname": "quotation_link", "fieldtype": "Link","options":"Supplier Quotation"},
        {"label": _("Quotation Status"), "fieldname": "quotation_status", "fieldtype": "Data"},
		{"label": _("Supplier Quotation Time Delay"), "fieldname": "supplier_quotation_delay", "fieldtype": "Data"},
		{"label": _("Purchase Planned"), "fieldname": "purchase_planned", "fieldtype": "Datetime"},
        {"label": _("Purchase Actual"), "fieldname": "purchase_actual", "fieldtype": "Datetime"},
        {"label": _("Purchase Order No"), "fieldname": "purchase_order_no", "fieldtype": "Link","options":"Purchase Order"},
        {"label": _("Purchase Order Time Delay"), "fieldname": "purchase_order_time_delay", "fieldtype": "Data"},
        {"label": _("Gate Planned"), "fieldname": "gate_planned", "fieldtype": "Datetime"},
        {"label": _("Gate Actual"), "fieldname": "gate_actual", "fieldtype": "Datetime"},
        {"label": _("Gate Entry No"), "fieldname": "gate_entry_no", "fieldtype": "Link", "options":"Gate Entry"},
        {"label":_("Receipt Planned"),"fieldname":"receipt_planned","fieldtype":"Datetime"},
        {"label":_("Receipt Actual"),"fieldname":"receipt_actual","fieldtype":"Datetime"},
        {"label": _("Purchase Receipt No"), "fieldname": "purchase_receipt_no", "fieldtype": "Link", "options":"Purchase Receipt"},
        {"label": _("Submitted By"), "fieldname": "submitted_by", "fieldtype": "Data"},
        {"label": _("Receipt Time Delay"), "fieldname": "receipt_time_delay", "fieldtype": "Data"},
        {"label":_("Quality Planned"),"fieldname":"quality_planned","fieldtype":"Datetime"},
        {"label":_("Quality actual"),"fieldname":"quality_actual","fieldtype":"Datetime"},
        {"label": _("Remarks"), "fieldname": "quality_remarks", "fieldtype": "Data"},
        {"label": _("Quality Submitted By"), "fieldname": "quality_submitted_by", "fieldtype": "Data"},
        {"label": _("Quality Delay"), "fieldname": "quality_delay", "fieldtype": "Data"},
        {"label": _("Payment Planned"), "fieldname": "payment_planned", "fieldtype": "Datetime"},
        {"label": _("Payment Actual"), "fieldname": "payment_actual", "fieldtype": "Datetime"},

        
	]

	

	columns.extend(
		[

			
			
		]
	)

	return columns

def get_material_name_entries(filters):
	sle = frappe.qb.DocType("Material Request")
	sed = frappe.qb.DocType("Material Request Item")
	query = (
		frappe.qb.from_(sle)
		.join(sed).on(sle.name == sed.parent)
		.select(
			sle.name,
			sle.transaction_date,
			sle.schedule_date,
			sed.item_code,
			sed.actual_qty,
			sle.creation,
            sle.remarks
   
		).where(sle.status != "Cancelled")
	)
	
	
	

	return query.run(as_dict=True)




def get_purchase_name_entries(filters):
	sle = frappe.qb.DocType("Material Request")
	sed = frappe.qb.DocType("Purchase Order")
	sedt = frappe.qb.DocType("Purchase Order Item")
	query = (
		frappe.qb.from_(sed)
        .join(sedt)
        .on(sed.name == sedt.parent)
        .join(sle).on(sedt.material_request == sle.name)
        .select(
            sed.name,
            sedt.material_request,
            sed.creation
		).where((sed.status != "Cancelled") & (sle.name == sedt.material_request) )
	)
	
	
	

	return query.run(as_dict=True)


def get_purchase_receipt_entries(filters):
    
    sle = frappe.qb.DocType("Material Request")
    sed = frappe.qb.DocType("Purchase Receipt")
    sedt = frappe.qb.DocType("Purchase Receipt Item")
    gate = frappe.qb.DocType("Gate Entry")
    cmt = frappe.qb.DocType("Comment")
    act = frappe.qb.DocType("Activity Log")
    qc = frappe.qb.DocType("Quality Inspection")
    query = (
		frappe.qb.from_(sed)
        .join(sedt)
        .on(sed.name == sedt.parent)
        .join(sle).on(sedt.material_request == sle.name)
        .left_outer_join(gate).on(sed.gate_entry == gate.name)
        .left_outer_join(cmt).on(sed.name == cmt.reference_name)
        .left_outer_join(act).on(sed.name == act.reference_name)
        .left_outer_join(qc).on(sedt.quality_inspection == qc.name)
        .select(
            sed.name,
            sedt.material_request,
            sed.gate_entry,
            gate.creation,
            gate.modified,
            sed.creation.as_("creation_by"),
            cmt.modified.as_("modification"),
            act.full_name,
            qc.creation.as_("quality_creation"),
            qc.modified.as_("quality_modified"),
            qc.remarks,
            qc.inspected_by 
            
		).where((sed.status != "Cancelled") & (sle.name == sedt.material_request))
	)
    return query.run(as_dict=True)

def get_modified_comment(filters):
    sle = frappe.qb.DocType("Material Request")
    cmt = frappe.qb.DocType("Comment")
    query = (
        frappe.qb.from_(cmt).join(sle).on(cmt.reference_name==sle.name)
        .select(
            cmt.modified,
            cmt.reference_name,
            sle.creation
        ).where((cmt.reference_doctype =="Material Request")&(cmt.content =="Pending"))
    )
    return query.run(as_dict=True)


def get_quotation_entries(filters):
	sle = frappe.qb.DocType("Material Request")
	sed = frappe.qb.DocType("Supplier Quotation")
	sedt = frappe.qb.DocType("Supplier Quotation Item")
	query = (
		frappe.qb.from_(sed)
        .join(sedt)
        .on(sed.name == sedt.parent)
        .join(sle).on(sedt.material_request == sle.name)
        .select(
            sed.name,
            sedt.material_request,
            sed.creation,
            sed.modified,
            sed.name,
            sed.status
		).where((sed.status != "Cancelled") & (sle.name == sedt.material_request))
	)
	return query.run(as_dict=True)

def get_purchase_modified_comment(filters):
    
    cmt = frappe.qb.DocType("Comment")
    po = frappe.qb.DocType("Purchase Order")
    query = (
        frappe.qb.from_(cmt).join(po).on(cmt.reference_name==po.name)
        .select(
            cmt.modified,
            cmt.reference_name,
            po.creation
        ).where((cmt.reference_doctype =="Purchase Order")&(cmt.content =="To Receive and Bill"))
    )
    return query.run(as_dict=True)


def get_purchase_invoice(filters):
    pui = frappe.qb.DocType("Purchase Invoice")
    pii = frappe.qb.DocType("Purchase Invoice Item")
    
    query =(
        frappe.qb.from_(pui).join(pii).on(pui.name == pii.parent)
        .select(
            
        )
    )