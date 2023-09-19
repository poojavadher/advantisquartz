import frappe
import datetime
import math
from frappe.utils.file_manager import save_file_on_filesystem

# @frappe.whitelist(allow_guest=True)
# def get_gratuity(employee):
#     salary_slips = frappe.get_all("Salary Slip", filters={ "employee": employee, "docstatus": 1 }, fields=['name', 'employee', 'start_date', 'end_date'])
#     return salary_slips

@frappe.whitelist(allow_guest=True)
def get_gratuity(employee):
    today = datetime.date.today()
    salary_slips = frappe.get_all("Salary Slip", filters={"employee": employee, "docstatus": 1}, fields=['name', 'employee', 'start_date', 'end_date'])
    
    if salary_slips:
        salary_slips.sort(key=lambda slip: abs((slip['end_date'] - today).days))
        get_basic_salary = frappe.get_all('Salary Detail', filters={
            'parent': ['in', [ss['name'] for ss in salary_slips]],
            'salary_component': 'Basic'  
        }, fields=['amount'])
        return get_basic_salary[0]
        # return salary_slips[0], get_basic_salary[0]
    else:
        return None


@frappe.whitelist(allow_guest=True)
def get_employee_bonus(employee, from_date, to_date):
    if not (employee and from_date and to_date):
        return None  

    from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d')
    to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d')

    salary_slips = frappe.get_all("Salary Slip", filters={
        "docstatus": 1,
        "employee": employee,
        "start_date": (">=", from_date),
        "end_date": ("<=", to_date)
    }, fields=['name', 'start_date', 'end_date'])

    if not salary_slips:
        return None  

    get_salary_data = frappe.get_all('Salary Detail', filters={
        'parent': ['in', [ss['name'] for ss in salary_slips]],
        'salary_component': 'Basic'  
    }, fields=['amount'])
    
    return salary_slips, get_salary_data


@frappe.whitelist(allow_guest=True)
def generate_txt(selected_date):
    salary_slips = frappe.get_all("Salary Slip", filters={
        "start_date": ["<=", selected_date],
        "end_date": [">=", selected_date],
        "docstatus": 1
    }, fields=['name', 'employee', 'uan', 'gross_pay', 'leave_without_pay', 'absent_days'])
    # return salary_slips
    output_data = []
    # stored_basic_amount = None
    
    if salary_slips:
        for salary_slip in salary_slips:
            leave_without_pay = salary_slip.leave_without_pay
            absent_days = salary_slip.absent_days
            ncp_days = leave_without_pay + absent_days
            if ncp_days == 0.0:
                ncp_days = 0
            uan = salary_slip.uan
            gross_pay = salary_slip.gross_pay
            employee_name = frappe.get_value("Employee", salary_slip.employee, "employee_name")
            salary_detail_data = frappe.get_all('Salary Detail', filters={
                'parent': salary_slip.name,
                'salary_component': ['in', ['Basic', 'Provident Fund']]
            }, fields=['salary_component', 'amount'])

            basic_amount = None
            pf_amount = None

            for detail in salary_detail_data:
                if detail['salary_component'] == 'Basic':
                    basic_amount = format_amount(detail['amount'])
                    eps = basic_amount * (8.33 / 100)
                    # print("EPS:", eps)
                    # stored_basic_amount = basic_amount
                elif detail['salary_component'] == 'Provident Fund':
                    pf_amount = format_amount(detail['amount'])
                    # print("pf:", pf_amount)

            diff = pf_amount - eps
            # print("diff:", diff)
            gross_pay_formatted = format_amount(gross_pay)
            ncp_days_formatted = format_amount(ncp_days)

            employee_output = f"{uan}#~#{employee_name}#~#{math.ceil(gross_pay_formatted)}#~#{math.ceil(basic_amount)}#~#{math.ceil(basic_amount)}#~#{math.ceil(basic_amount)}#~#{math.ceil(pf_amount)}#~#{math.ceil(eps)}#~#{math.ceil(diff)}#~#{math.ceil(ncp_days_formatted)}#~#0"

            output_data.append(employee_output)

        final_output = "\n".join(output_data)
        print(final_output)
        txt_file_path = "PF_ECR.txt"
        save_file_on_filesystem(txt_file_path, content=final_output, is_private=0)
        return txt_file_path
            
    else: 
        frappe.msgprint("Salary slip does not exist for given dates.")

def format_amount(amount):
    if amount == int(amount):
        return float(amount)
    else:
        return float(amount)


@frappe.whitelist(allow_guest=True)
def generate_leave_allocation():
    return "Hello"
    current_date = datetime.datetime.now().date().strftime('%Y-%m-%d')
    
    l_type = frappe.db.get_list('Leave Type', fields="name", filters={"is_privilege_leave":1})
    # return l_type 

    for leaves in l_type:
        leave_type = leaves.name
    
        all_emp = frappe.db.get_list('Leave Allocation', filters={'leave_type': leave_type}, fields=['employee_name'])
        
        for emp in all_emp:
            employee_name = emp.employee_name
            last_doc = frappe.get_last_doc("Leave Allocation", filters={"employee_name": employee_name, "docstatus": 1})
            
            if last_doc:
                to_date = last_doc.to_date
                next_date = to_date + datetime.timedelta(days=1)
                specific_fields = {
                    "emp": last_doc.employee,
                    "emp_name": last_doc.employee_name,
                    "leave_type": last_doc.leave_type,
                    "to_date": last_doc.to_date,
                    "next_date": next_date
                }
            else:
                specific_fields = None
                to_date = None 
            
            if to_date and to_date.strftime('%Y-%m-%d') == current_date:  
                new_leave_allocation = next_date + datetime.timedelta(days=19)
                leave_period = frappe.get_all("Leave Period", filters={"from_date": ("<=", next_date), "to_date": (">=", next_date)}, fields=["name", "from_date", "to_date"])
                
                if leave_period:
                    leave_period = leave_period[0]
                    
                    from_date_leave_period = leave_period.get("from_date")
                    to_date_leave_period = leave_period.get("to_date")
                    
                    count_leave_allocations = frappe.get_all("Leave Allocation", filters={"employee": specific_fields["emp"], "from_date": (">=", from_date_leave_period), "to_date": ("<=", to_date_leave_period)})
                    count = len(count_leave_allocations)
                    
                    if count < 15 :
                        existing_allocation = frappe.get_all("Leave Allocation", filters={"employee": specific_fields["emp"], "from_date": next_date, "to_date": new_leave_allocation})
                        
                        if not existing_allocation:
                            if new_leave_allocation <= to_date_leave_period:
                                new_allocation = frappe.new_doc("Leave Allocation")
                                new_allocation.employee = specific_fields["emp"]
                                new_allocation.leave_type = specific_fields["leave_type"]
                                new_allocation.from_date = next_date
                                new_allocation.to_date = new_leave_allocation
                                new_allocation.new_leaves_allocated = "1"
                                new_allocation.carry_forward = 1
                                new_allocation.insert(ignore_permissions=True)
                                frappe.db.commit()
                            else:
                                new_allocation = frappe.new_doc("Leave Allocation")
                                new_allocation.employee = specific_fields["emp"]
                                new_allocation.leave_type = specific_fields["leave_type"]
                                new_allocation.from_date = next_date
                                new_allocation.to_date = to_date_leave_period
                                new_allocation.new_leaves_allocated = "1"
                                new_allocation.carry_forward = 1
                                new_allocation.insert(ignore_permissions=True)
                                frappe.db.commit()
                        else:
                            None
                            # frappe.msgprint("Leave allocation already exists for the given period")
                    else: 
                        None
                        # frappe.msgprint("Can't allocate leaves more than 15")
                else:
                    None
                    # frappe.msgprint("Create Leave Period for the current month")
            else:
                return "NO"

    #     return "yesssssssssss"  
    # return "yes" 


