import frappe
import datetime

@frappe.whitelist(allow_guest=True)
def generate_leave_allocation():
    current_date = datetime.datetime.now().date().strftime('%Y-%m-%d')
    
    last_doc = frappe.get_last_doc("Leave Allocation", filters={"employee_name": "Pooja", "docstatus": 1})
    
    if last_doc:
        to_date = last_doc.to_date
        next_date = to_date + datetime.timedelta(days=1) 
        specific_fields = {
            "emp": last_doc.employee,
            "emp_name": last_doc.employee_name,
            "leave_type": last_doc.leave_type,
            "to_date": last_doc.to_date,
            "next_date": next_date.strftime('%Y-%m-%d')
        }
    else:
        specific_fields = None
        
    # if to_date == current_date:
        # return "yes"
    new_leave_allocation = next_date + datetime.timedelta(days=19)
    leave_period = frappe.get_all("Leave Period", filters={"from_date": ("<=", next_date), "to_date": (">=", next_date)}, fields=["name", "from_date", "to_date"])
    
    if leave_period:
        leave_period = leave_period[0]
        
        from_date = leave_period.get("from_date")
        to_date = leave_period.get("to_date")
        
        existing_allocation = frappe.get_all("Leave Allocation", filters={"employee": specific_fields["emp"], "from_date": next_date, "to_date": new_leave_allocation})
        
        if not existing_allocation:
        
            if new_leave_allocation <= to_date:
                print("\n\n\n\n\n", "yes", "\n\n\n\n\n")
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
                print("\n\n\n\n\n", "no", "\n\n\n\n\n")
                new_allocation = frappe.new_doc("Leave Allocation")
                new_allocation.employee = specific_fields["emp"]
                new_allocation.leave_type = specific_fields["leave_type"]
                new_allocation.from_date = next_date
                new_allocation.to_date = to_date
                new_allocation.new_leaves_allocated = "1"
                new_allocation.carry_forward = 1
                new_allocation.insert(ignore_permissions=True)
                frappe.db.commit()
                
        else:
            frappe.msgprint("Leave allocation already exists for the given period")

    else:
        frappe.msgprint("Create Leave Period for current month")

    # else:
    #     return None
        
    # new_leave_allocation = next_date + datetime.timedelta(days=20)
    # leave_period = frappe.get_all("Leave Period", filters={"from_date": ("<=", current_date), "to_date": (">=", current_date)}, fields=["name", "from_date", "to_date"])
    
    
    # leave_period = get_leave_period_for_date(current_date)
    # new_leave_allocation = next_date + datetime.timedelta(days=20)
    
    # if specific_fields and leave_period:
    #     from_date = leave_period.get("from_date")
    #     to_date = leave_period.get("to_date")
        
    #     if from_date <= next_date <= to_date:
    #         print("\n\n\n\n\n", next_date, "\n\n\n\n\n")
    #         # return "yes"
    #         new_allocation = frappe.new_doc("Leave Allocation")
    #         new_allocation.employee = specific_fields["emp"]
    #         new_allocation.leave_type = specific_fields["leave_type"]
    #         new_allocation.from_date = specific_fields["next_date"]
    #         new_allocation.to_date = new_leave_allocation
    #         new_allocation.new_leaves_allocated = "1"
    #         new_allocation.carry_forward = 1
    #         new_allocation.insert(ignore_permissions=True)
    #         frappe.db.commit()
            
    #     else:
    #         print("\n\n\n\n\n", "no", "\n\n\n\n\n")
    #         new_allocation = frappe.new_doc("Leave Allocation")
    #         new_allocation.employee = specific_fields["emp"]
    #         new_allocation.leave_type = specific_fields["leave_type"]
    #         new_allocation.from_date = specific_fields["next_date"]
    #         new_allocation.to_date = to_date
    #         new_allocation.new_leaves_allocated = "1"
    #         new_allocation.carry_forward = 1
    #         new_allocation.insert(ignore_permissions=True)
    #         frappe.db.commit()
        
    # return "no"

# def get_leave_period_for_date(current_date):
#     leave_period = frappe.get_all("Leave Period",
#                                    filters={"from_date": ("<=", current_date), "to_date": (">=", current_date)},
#                                    fields=["name", "from_date", "to_date"])
    
#     if leave_period:
#         return leave_period[0]
#     else:
#         return None








# import frappe
# import datetime

# @frappe.whitelist(allow_guest=True)
# def generate_leave_allocation():
#     current_date = datetime.datetime.now().date().strftime('%Y-%m-%d')
    
#     last_doc = frappe.get_last_doc("Leave Allocation", filters={"employee_name":"Pooja"})
#     # return last_doc
#     if last_doc:
#         to_date = last_doc.to_date
#         next_date = (to_date + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
#         specific_fields = {
#             "emp": last_doc.employee,
#             "emp_name": last_doc.employee_name,
#             "leave_type" : last_doc.leave_type,
#             "to_date": last_doc.to_date,
#             "next_date": next_date
#         }
#         # return specific_fields, current_date
#     else:
#         None
        
#     leave_period = frappe.get_all("Leave Period", filters={"from_date": ("<=", current_date), "to_date": (">=", current_date)}, fields=["name", "from_date", "to_date"])
#     # return leave_period[0]
    
#     # if to_date == current_date:
#     #     return "yes"
#     # else:
#     #     return "no" 
        
#     # new_allocation = frappe.new_doc("Leave Allocation")
#     # new_allocation.employee = specific_fields["emp"]
#     # new_allocation.leave_type = specific_fields["leave_type"]
#     # new_allocation.from_date = specific_fields["next_date"]
#     # new_allocation.to_date = "2023-10-10"
#     # new_allocation.new_leaves_allocated = "1"
#     # new_allocation.carry_forward = 1
#     # new_allocation.insert(ignore_permissions=True)
#     # frappe.db.commit()
    
#     # return "ok"
