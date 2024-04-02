# # Copyright (c) 2023, pooja@sanskartechnolab.com and contributors
# # For license information, please see license.txt

import frappe
import math
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def execute(filters=None):
    columns = [
		{
            "label": "UAN", 
            "fieldname": "uan", 
            "fieldtype": "Data", 
            "width": 100
        },
        {
            "label": "Member Name",
            "fieldname": "member_name",
            "fieldtype": "Data",
            "width": 220
        },
        {
            "label": "Gross Wages",
            "fieldname": "gross_wages",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": "EPF Wages", 
            "fieldname": "epf_wages", 
            "fieldtype": "Data", 
            "width": 100
        },
		{
            "label": "EPS Wages",
            "fieldname": "eps_wages",
            "fieldtype": "Data",
            "width": 100
        },
		{
            "label": "EDLI Wages",
            "fieldname": "edli_wages",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": "EPF Contribution remitted",
            "fieldname": "epf_contribution_remitted",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": "EPS Contribution remitted",
            "fieldname": "eps_contribution_remitted",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": "EPF and EPS Diff remitted",
            "fieldname": "epf_and_eps_diff_remitted",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": "NCP Days",
            "fieldname": "ncp_days",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": "Refund of Advances",
            "fieldname": "refund_of_advances",
            "fieldtype": "Data",
            "width": 100
        }
    ]

    data = []
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    salary_slips = frappe.get_all("Salary Slip", filters={
        "start_date": ["<=", from_date],
        "end_date": [">=", to_date],
        "docstatus": 1
    }, fields=['name', 'uan', 'employee_name', 'gross_pay', 'leave_without_pay', 'absent_days'])
    
    for slip in salary_slips:
        # Extracting required data from the salary slip
        gross_pay = slip.get('gross_pay')
        uan = slip.get('uan')
        employee_name = slip.get('employee_name')
        
        # Calculating EPF Wages as per the given formula
        salary_detail_data = frappe.get_all('Salary Detail', filters={'parent': slip['name'],'salary_component': ['in', ['House Rent Allowance']]}, fields=['amount'])
        house_rent_allowance = sum(detail['amount'] for detail in salary_detail_data)
        epf_wages = gross_pay - house_rent_allowance
        
        # Appending data to the list
        data.append({
            "uan": uan,
            "member_name": employee_name,
            "gross_wages": gross_pay,
            "epf_wages": epf_wages,
            # Fill other fields as needed
        })

    return columns, data

    # for slip in salary_slips:
    #     name = slip.get('name')
        
    #     salary_detail_data = frappe.get_all('Salary Detail', filters={'parent': name,'salary_component': ['in', ['Basic', 'House Rent Allowance', 'Provident Fund']]}, fields=['salary_component', 'amount'])
        
    #     ncp_days = slip.get('leave_without_pay', 0) + slip.get('absent_days', 0)
        
    #     epf_wages = ""
    #     epf_contribution_remitted = ""
        
    #     for detail in salary_detail_data:
    #         component = detail.get('salary_component')
    #         amount = detail.get('amount')
            
    #         # if component == 'Basic':
    #         #     epf_wages = amount
    #         #     eps_contribution_remitted = epf_wages * (8.33 / 100)
    #         if component == 'Provident Fund':
    #             epf_contribution_remitted = amount
    #             eps_contribution_remitted = amount * (8.33 / 100)
    #             epf_and_eps_diff_remitted = amount * (3.67/ 100)
    #         elif component == 'House Rent Allowance':
    #             epf_wages = slip.get('gross_pay') - amount
        
    #     # epf_and_eps_diff_remitted = epf_contribution_remitted - eps_contribution_remitted
        
    #     data.append({
    #         "uan": slip.get('uan'), 
    #         "member_name": slip.get('employee_name'),
    #         "gross_wages": slip.get('gross_pay'),
    #         "epf_wages": math.ceil(epf_wages),  
    #         "eps_wages": math.ceil(epf_wages),  
    #         "edli_wages": math.ceil(epf_wages), 
    #         "epf_contribution_remitted": math.ceil(epf_contribution_remitted),  
    #         "eps_contribution_remitted": math.ceil(eps_contribution_remitted),  
    #         "epf_and_eps_diff_remitted": math.ceil(epf_and_eps_diff_remitted),  
    #         "ncp_days": math.ceil(ncp_days),  
    #         "refund_of_advances": "0"
    #     })

    # return columns, data

    
 