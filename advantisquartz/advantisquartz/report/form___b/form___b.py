import frappe

def execute(filters=None):
    columns = [
        {
            "label": "Name",
            "fieldname": "name",
            "fieldtype": "Data",
            "width": 220
        },
        {
            "label": "Number of Days Worked",
            "fieldname": "number_of_days_worked",
            "fieldtype": "Data",
            "width": 50
        },
        {
            "label": "Total Earnings",
            "fieldname": "total_earnings",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": "Total Deductions",
            "fieldname": "total_deductions",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": "Employee Share PF Welfare Found",
            "fieldname": "employee_share_pf_welfare_found",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": "Receipt by Employee/Bank Transaction ID",
            "fieldname": "receipt_by_employee_bank_transaction_id",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": "Date of Payment",
            "fieldname": "date_of_payment",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": "Remarks",
            "fieldname": "remarks",
            "fieldtype": "Data",
            "width": 100
        },
    ]

    data = []
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")

    salary_slips = frappe.get_all("Salary Slip", filters={
        "start_date": ["<=", from_date],
        "end_date": [">=", to_date],
        "docstatus": 1
    }, fields=['name', 'employee_name', 'payment_days', 'gross_pay', 'total_deduction', 'posting_date'])

    for slip in salary_slips:
        name = slip.get('name')
        
        sal_doc = frappe.get_doc("Salary Slip", name)
        sal_earning = sal_doc.get("earnings")
        sal_deduction = sal_doc.get("deductions")
        
        employee_earnings = {}
        employee_deductions = {}
        
        for sal_ear in sal_earning:
            ans_com = sal_ear.salary_component
            ans_amt = sal_ear.amount
            
            column_exists = any(column['fieldname'] == ans_com for column in columns)
            if not column_exists:
                columns.append({
                    "label": ans_com,
                    "fieldname": ans_com,
                    "fieldtype": "Data",
                    "width": 100
                })

            employee_earnings[ans_com] = ans_amt

        for sal_ded in sal_deduction:
            ded_com = sal_ded.salary_component
            ded_amt = sal_ded.amount
            employee_data = {
                "name": slip.get('employee_name'),
                "number_of_days_worked": slip.get('payment_days'),
                "total_earnings": slip.get('gross_pay'),
                "total_deductions": slip.get('total_deduction'),
                "date_of_payment": frappe.utils.get_datetime(slip.get('posting_date')).strftime('%d-%m-%Y') 
            }
            column_exists = any(column['fieldname'] == ded_com for column in columns)
            if not column_exists:
                columns.append({
                    "label": ded_com,
                    "fieldname": ded_com,
                    "fieldtype": "Data",
                    "width": 100
                })

            employee_deductions[ded_com] = ded_amt

        
        
        employee_data.update(employee_earnings)
        employee_data.update(employee_deductions)

        data.append(employee_data)

    return columns, data

# import frappe

# def execute(filters=None):
#     columns = [
#         {
#             "label": "Name",
#             "fieldname": "name",
#             "fieldtype": "Data",
#             "width": 220
#         },
#         {
#             "label": "Number of Days Worked",
#             "fieldname": "number_of_days_worked",
#             "fieldtype": "Data",
#             "width": 50
#         },
#         {
#             "label": "Total Earnings",
#             "fieldname": "total_earnings",
#             "fieldtype": "Data",
#             "width": 100
#         },
#         {
#             "label": "Total Deductions",
#             "fieldname": "total_deductions",
#             "fieldtype": "Data",
#             "width": 100
#         },
#         {
#             "label": "Employee Share PF Welfare Found",
#             "fieldname": "employee_share_pf_welfare_found",
#             "fieldtype": "Data",
#             "width": 100
#         },
#         {
#             "label": "Receipt by Employee/Bank Transaction ID",
#             "fieldname": "receipt_by_employee_bank_transaction_id",
#             "fieldtype": "Data",
#             "width": 100
#         },
#         {
#             "label": "Date of Payment",
#             "fieldname": "date_of_payment",
#             "fieldtype": "Data",
#             "width": 100
#         },
#         {
#             "label": "Remarks",
#             "fieldname": "remarks",
#             "fieldtype": "Data",
#             "width": 100
#         },
#     ]

#     data = []
#     from_date = filters.get("from_date")
#     to_date = filters.get("to_date")

#     salary_slips = frappe.get_all("Salary Slip", filters={
#         "start_date": ["<=", from_date],
#         "end_date": [">=", to_date],
#         "docstatus": 1
#     }, fields=['name', 'employee_name', 'payment_days', 'gross_pay', 'total_deduction', 'posting_date'])

#     for slip in salary_slips:
#         name = slip.get('name')
        
#         sal_doc = frappe.get_doc("Salary Slip", name)
#         sal_earning = sal_doc.get("earnings")
#         sal_deduction = sal_doc.get("deductions")
        
#         employee_earnings = {}
#         employee_deductions = {}
        
#         for sal_ear in sal_earning:
#             ans_com = sal_ear.salary_component
#             ans_amt = sal_ear.amount
            
#             column_exists = any(column['fieldname'] == ans_com for column in columns)
#             if not column_exists:
#                 columns.append({
#                     "label": ans_com,
#                     "fieldname": ans_com,
#                     "fieldtype": "Data",
#                     "width": 100
#                 })

#             employee_earnings[ans_com] = ans_amt

#         for sal_ded in sal_deduction:
#             ded_com = sal_ded.salary_component
#             ded_amt = sal_ded.amount
            
#             column_exists = any(column['fieldname'] == ded_com for column in columns)
#             if not column_exists:
#                 columns.append({
#                     "label": ded_com,
#                     "fieldname": ded_com,
#                     "fieldtype": "Data",
#                     "width": 100
#                 })

#             employee_deductions[ded_com] = ded_amt

#         employee_data = {
#             "name": slip.get('employee_name'),
#             "number_of_days_worked": slip.get('payment_days'),
#             "total_earnings": slip.get('gross_pay'),
#             "total_deductions": slip.get('total_deduction'),
#             "date_of_payment": frappe.utils.get_datetime(slip.get('posting_date')).strftime('%d-%m-%Y') 
#         }
        
#         employee_data.update(employee_earnings)
#         employee_data.update(employee_deductions)

#         data.append(employee_data)

#     return columns, data






# import frappe

# def execute(filters=None):
#     columns = [
#         {
#             "label": "Name",
#             "fieldname": "name",
#             "fieldtype": "Data",
#             "width": 220
#         },
#         {
#             "label": "Number of Days Worked",
#             "fieldname": "number_of_days_worked",
#             "fieldtype": "Data",
#             "width": 50
#         },
#         {
#             "label": "Total Earnings",
#             "fieldname": "total_earnings",
#             "fieldtype": "Data",
#             "width": 100
#         }
#     ]

#     data = []
#     from_date = filters.get("from_date")
#     to_date = filters.get("to_date")

#     salary_slips = frappe.get_all("Salary Slip", filters={
#         "start_date": ["<=", from_date],
#         "end_date": [">=", to_date],
#         "docstatus": 1
#     }, fields=['name', 'employee_name', 'payment_days', 'gross_pay', 'total_deduction'])

#     for slip in salary_slips:
#         name = slip.get('name')
#         gross = slip.get('gross_pay')

#         # Fetch earnings components for the current salary slip
#         earnings_component = frappe.get_all('Salary Detail', filters={'parent': name, 'custom_type': 'Earning'},
#                                             fields=['salary_component', 'amount'])

#         # Create a dictionary to store earnings for the current employee
#         employee_earnings = {}

#         for salary_detail in earnings_component:
#             component = salary_detail.get('salary_component')
#             amount = salary_detail.get('amount')
#             employee_earnings[component.lower().replace(' ', '_')] = amount

#         # Append data for the current employee
#         employee_data = {
#             "name": slip.get('employee_name'),
#             "number_of_days_worked": slip.get('payment_days'),
#             "total_earnings": gross,
#         }

#         # Add earnings data to the employee_data dictionary
#         employee_data.update(employee_earnings)

#         # Append the employee_data to the data list
#         data.append(employee_data)

#         # Update columns dynamically based on earnings components
#         for component in employee_earnings.keys():
#             columns.append({
#                 "label": component,
#                 "fieldname": component,
#                 "fieldtype": "Data",
#                 "width": 100
#             })

#     return columns, data



# import frappe

# def execute(filters=None):
# 	columns = [
# 		{
#             "label": "Name",
#             "fieldname": "name",
#             "fieldtype": "Data",
#             "width": 220
#         },
#   		{
#             "label": "Number of Days Worked",
#             "fieldname": "number_of_days_worked",
#             "fieldtype": "Data",
#             "width": 50
#         },
#     	{
#             "label": "Total Earnings",
#             "fieldname": "total_earnings",
#             "fieldtype": "Data",
#             "width": 100
#         }
# 	]
 
 
# 	data = []
# 	from_date = filters.get("from_date")
# 	to_date = filters.get("to_date")
	
# 	salary_slips = frappe.get_all("Salary Slip", filters={
#         "start_date": ["<=", from_date],
#         "end_date": [">=", to_date],
#         "docstatus": 1
#     }, fields=['name', 'employee_name', 'payment_days', 'gross_pay', 'total_deduction'])
 
# 	for slip in salary_slips:
# 		name = slip.get('name')
# 		# employee_name = slip.get('employee_name')	
# 		# payment_days = slip.get('payment_days')
# 		gross = slip.get('gross_pay')
# 		# print("\n\n\n", gross, "\n\n\n")
# 		earnings_component = frappe.get_all('Salary Detail', filters={'parent': name, 'custom_type': 'Earning'}, fields=['salary_component', 'amount'])
# 		# print(earnings_component)
  
# 		earnings_component_dict = {}		
# 		for salary_detail in earnings_component:
# 			component = salary_detail.get('salary_component')
# 			amount = salary_detail.get('amount')
# 			earnings_component_dict[component] = amount
# 		# print(earnings_component_dict)
  
# 		for component, amount in earnings_component_dict.items():
# 			columns.append({
# 				"label": component,
# 				"fieldname": component.lower().replace(' ', '_'),
# 				"fieldtype": "Data",
# 				"width": 100
# 			})
  
  
# 		data.append({
#             "name": slip.get('employee_name'),
#             "number_of_days_worked": slip.get('payment_days'),
#             # **earnings_component_dict,
#             "total_earnings": slip.get('gross_pay')
#         })	
 	
 
# 	return columns, data
 