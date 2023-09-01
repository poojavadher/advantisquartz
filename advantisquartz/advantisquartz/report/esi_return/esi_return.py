# Copyright (c) 2023, pooja@sanskartechnolab.com and contributors
# For license information, please see license.txt

import frappe
import math
from datetime import datetime, timedelta
def execute(filters=None):
    columns = [
		{
            "label": "IP Number ", 
            "fieldname": "ip_number", 
            "fieldtype": "Data", 
            "width": 185
        },
        {
            "label": "IP Name",
            "fieldname": "ip_name",
            "fieldtype": "Data",
            "width": 350
        },
        {
            "label": "No of Days for which wages paid/payable during the month",
            "fieldname": "paid_days",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": "Total Monthly Wages", 
            "fieldname": "monthly_wages", 
            "fieldtype": "Data", 
            "width": 200
        },
		{
            "label": " Reason Code for Zero workings days",
            "fieldname": "reason_code",
            "fieldtype": "Int",
            "width": 150
        },
		{
            "label": " Last Working Day",
            "fieldname": "last_working_day",
            "fieldtype": "Data",
            "width": 180
        }
    ]

    data = []
    
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    
    salary_slips = frappe.get_all("Salary Slip", filters={
        "start_date": ["<=", from_date],
        "end_date": [">=", to_date],
        "docstatus": 1
    }, fields=['name', 'esi_number', 'employee_name', 'gross_pay', 'payment_days', 'reason_code', 'relieving_date'])
    
    # print("\n\n", salary_slips, "\n\n")
    
    # without_reason = '0'
    # on_leave = '1'
    # left_service = '2'
    # retired = '3'
    # out_of_coverage = '4'
    # expired = '5'
    # non_implemented_area = '6'
    # compliance_by_immediate_employer = '7'
    # suspension_of_work = '8'
    # strike_lockout = '9'
    # retrenchment = '10'
    # no_work = '11'
    # doesnt_belong_to_this_employer = '12'
    # duplicate_ip = '13'
       
    for slip in salary_slips:
        esi_number = slip.get('esi_number')
        employee_name = slip.get('employee_name')
        payment_days = slip.get('payment_days')
        gross_pay = slip.get('gross_pay')
        reason_code = slip.get('reason_code')
        relieving_date = slip.get('relieving_date')
        if relieving_date:
            relieving_date = datetime.strptime(relieving_date, '%Y-%m-%d').strftime('%d/%m/%Y')
        
        data.append({
            "ip_number": esi_number, 
            "ip_name": employee_name,
            "paid_days": math.ceil(payment_days),
            "monthly_wages": math.ceil(gross_pay),  
            "reason_code": reason_code,  
            "last_working_day": relieving_date,
        })

    return columns, data

    
 