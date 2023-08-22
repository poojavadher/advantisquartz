import frappe
import datetime


# @frappe.whitelist(allow_guest=True)
# def total_leaves():
#     total_leave = frappe.db.get_value("Leave Type", fieldname="max_leaves_allowed", filters={"leave_type_name": "Privilege Leave (Employee)"})
#     return total_leave

@frappe.whitelist(allow_guest=True)
def generate_leave_allocation():
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


# ---------------------------------------------------------------------------------------------------------------

# import frappe
# import datetime

# @frappe.whitelist(allow_guest=True)
# def generate_leave_allocation():
#     current_date = datetime.datetime.now().date().strftime('%Y-%m-%d')
    
#     all_emp = frappe.db.get_list('Leave Allocation',filters={'leave_type': 'Privilege Leave (Employee)'},fields=['employee_name'])
#     # return all_emp
#     for emp in all_emp:
#         employee_name = emp.employee_name
#         last_doc =  frappe.get_last_doc("Leave Allocation", filters={"employee_name": employee_name, "docstatus": 1})
        
#         if last_doc:
#             to_date = last_doc.to_date
#             next_date = to_date + datetime.timedelta(days=1) 
#             specific_fields = {
#                 "emp": last_doc.employee,
#                 "emp_name": last_doc.employee_name,
#                 "leave_type": last_doc.leave_type,
#                 "to_date": last_doc.to_date,
#                 "next_date": next_date  # Removed the extra period here
#             }
#         else:
#             specific_fields = None
#             to_date = None 
        
#         if to_date and to_date.strftime('%Y-%m-%d') == current_date:  # Check if to_date is not None
#             new_leave_allocation = next_date + datetime.timedelta(days=19)
#             leave_period = frappe.get_all("Leave Period", filters={"from_date": ("<=", next_date), "to_date": (">=", next_date)}, fields=["name", "from_date", "to_date"])
            
#             if leave_period:
#                 leave_period = leave_period[0]
                
#                 from_date_leave_period = leave_period.get("from_date")
#                 to_date_leave_period = leave_period.get("to_date")
                
#                 count_leave_allocations = frappe.get_all("Leave Allocation", filters={"employee": specific_fields["emp"], "from_date": (">=", from_date_leave_period), "to_date": ("<=", to_date_leave_period)})
#                 count = len(count_leave_allocations)
                
#                 if count < 15 :
#                     existing_allocation = frappe.get_all("Leave Allocation", filters={"employee": specific_fields["emp"], "from_date": next_date, "to_date": new_leave_allocation})
                    
#                     if not existing_allocation:
#                         if new_leave_allocation <= to_date_leave_period:
#                             new_allocation = frappe.new_doc("Leave Allocation")
#                             new_allocation.employee = specific_fields["emp"]
#                             new_allocation.leave_type = specific_fields["leave_type"]
#                             new_allocation.from_date = next_date
#                             new_allocation.to_date = new_leave_allocation
#                             new_allocation.new_leaves_allocated = "1"
#                             new_allocation.carry_forward = 1
#                             new_allocation.insert(ignore_permissions=True)
#                             frappe.db.commit()
#                         else:
#                             new_allocation = frappe.new_doc("Leave Allocation")
#                             new_allocation.employee = specific_fields["emp"]
#                             new_allocation.leave_type = specific_fields["leave_type"]
#                             new_allocation.from_date = next_date
#                             new_allocation.to_date = to_date_leave_period
#                             new_allocation.new_leaves_allocated = "1"
#                             new_allocation.carry_forward = 1
#                             new_allocation.insert(ignore_permissions=True)
#                             frappe.db.commit()
#                     else:
#                         frappe.msgprint("Leave allocation already exists for the given period")
#                 else: 
#                     frappe.msgprint("Can't allocate leaves more than 15")
#             else:
#                 frappe.msgprint("Create Leave Period for the current month")
            
#             return "yes"
#         else:
#             return "NO"
        





# -----------------------------------------------------------------------------------------





# import frappe
# import datetime

# @frappe.whitelist(allow_guest=True)
# def generate_leave_allocation():
#     current_date = datetime.datetime.now().date().strftime('%Y-%m-%d')
    
#     last_doc = frappe.get_last_doc("Leave Allocation", filters={"employee_name": "Pooja", "docstatus": 1})
#     # return last_doc
#     if last_doc:
#         to_date = last_doc.to_date
#         # return to_date
#         next_date = to_date + datetime.timedelta(days=1) 
#         specific_fields = {
#             "emp": last_doc.employee,
#             "emp_name": last_doc.employee_name,
#             "leave_type": last_doc.leave_type,
#             "to_date": last_doc.to_date,
#             "next_date": next_date.strftime('%Y-%m-%d')
#         }
#     else:
#         specific_fields = None
    
#     # return to_date, current_date
#     if to_date == current_date:
#         # return "yes"
#         new_leave_allocation = next_date + datetime.timedelta(days=19)
#         leave_period = frappe.get_all("Leave Period", filters={"from_date": ("<=", next_date), "to_date": (">=", next_date)}, fields=["name", "from_date", "to_date"])
        
#         if leave_period:
#             leave_period = leave_period[0]
            
#             from_date_leave_period = leave_period.get("from_date")
#             to_date_leave_period = leave_period.get("to_date")
            
#             count_leave_allocations = frappe.get_all("Leave Allocation", filters={"employee": specific_fields["emp"], "from_date": (">=", from_date_leave_period), "to_date": ("<=", to_date_leave_period)})
#             count = len(count_leave_allocations)
#             # return count
            
#             if count < 15 :
            
#                 existing_allocation = frappe.get_all("Leave Allocation", filters={"employee": specific_fields["emp"], "from_date": next_date, "to_date": new_leave_allocation})
                
#                 if not existing_allocation:
                
#                     if new_leave_allocation <= to_date_leave_period:
#                         print("\n\n\n\n\n", "yes", "\n\n\n\n\n")
#                         new_allocation = frappe.new_doc("Leave Allocation")
#                         new_allocation.employee = specific_fields["emp"]
#                         new_allocation.leave_type = specific_fields["leave_type"]
#                         new_allocation.from_date = next_date
#                         new_allocation.to_date = new_leave_allocation
#                         new_allocation.new_leaves_allocated = "1"
#                         new_allocation.carry_forward = 1
#                         new_allocation.insert(ignore_permissions=True)
#                         frappe.db.commit()

#                     else:
#                         print("\n\n\n\n\n", "no", "\n\n\n\n\n")
#                         new_allocation = frappe.new_doc("Leave Allocation")
#                         new_allocation.employee = specific_fields["emp"]
#                         new_allocation.leave_type = specific_fields["leave_type"]
#                         new_allocation.from_date = next_date
#                         new_allocation.to_date = to_date_leave_period
#                         new_allocation.new_leaves_allocated = "1"
#                         new_allocation.carry_forward = 1
#                         new_allocation.insert(ignore_permissions=True)
#                         frappe.db.commit()
                        
#                 else:
#                     frappe.msgprint("Leave allocation already exists for the given period")
                    
#             else: 
#                 frappe.msgprint("Can't allocate leaves more than 15")

#         else:
#             frappe.msgprint("Create Leave Period for current month")
            
#         return "yes"

#     else:
#         return "NO"
        
        
        
        # -----------------------------------------------------------------------------------
        
        
        
        
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
