import frappe
from datetime import datetime
import calendar

@frappe.whitelist()
def get_attendance(month, year):
    
    months = month
    
    days_30 = ["04", "06", "09", "11"]
    days_31 = ["01", "03", "05", "07", "08", "10", "12"]
    other = ["02"]
    # date_format = '%d-%m-%Y'
    days = 0
    
    if months in days_30:
        days = 30
        from_date = f'{year}-{months}-01'
        to_date = f'{year}-{months}-30'
        
    elif months in days_31:
        days = 31
        from_date = f'{year}-{months}-01'
        to_date = f'{year}-{months}-31'
        
    elif months in other:
        from_date = f'{year}-{months}-01'
        is_leap_year = calendar.isleap(int(year))
        to_date = f'{year}-{months}-29' if is_leap_year else f'{year}-{months}-28'
        if is_leap_year:
            days = 29
        else:
            days = 28
      
    else:
        return None


    employees = frappe.get_all("Employee", filters={}, fields=["employee_name"])


    employee_logs = {}
    for employee in employees:
        employee_name = employee.get("employee_name")
        records = {}

        for i in range(1, days + 1):
            date = f'{year}-{int(months):02d}-{i:02d}'

            first_in_record = frappe.db.sql("""
                SELECT employee_name, log_type, MIN(time) AS Mintime
                FROM `tabEmployee Checkin`
                WHERE time BETWEEN %s AND %s
                    AND employee_name = %s
                    AND log_type = 'IN'
            """, (f'{date} 00:00:00', f'{date} 23:59:59', employee_name), as_dict=True)

            last_out_record = frappe.db.sql("""
                SELECT employee_name, log_type, MAX(time) AS Maxtime
                FROM `tabEmployee Checkin`
                WHERE time BETWEEN %s AND %s
                    AND employee_name = %s
                    AND log_type = 'OUT'
            """, (f'{date} 00:00:00', f'{date} 23:59:59', employee_name), as_dict=True)

            records[date] = {'employee_name': employee_name}

            if first_in_record and first_in_record[0]['Mintime'] is not None:
                records[date].update({'IN': {'Mintime': first_in_record[0]['Mintime'].strftime('%H:%M:%S')}})

            if last_out_record and last_out_record[0]['Maxtime'] is not None:
                records[date].update({'OUT': {'Maxtime': last_out_record[0]['Maxtime'].strftime('%H:%M:%S')}})

        employee_logs[employee_name] = records

    # print(employee_logs, days)
    return employee_logs

    
    
    