from . import __version__ as app_version

app_name = "advantisquartz"
app_title = "Advantisquartz"
app_publisher = "pooja@sanskartechnolab.com"
app_description = "Custom App"
app_email = "pooja@sanskartechnolab.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/advantisquartz/css/advantisquartz.css"
# app_include_js = "/assets/advantisquartz/js/advantisquartz.js"
app_include_js = "/assets/advantisquartz/js/image_view.js"

# include js, css files in header of web template
# web_include_css = "/assets/advantisquartz/css/advantisquartz.css"
# web_include_js = "/assets/advantisquartz/js/advantisquartz.js"
# web_include_js = "/assets/advantisquartz/js/image_view.js"


# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "advantisquartz/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}
# page_js = {"page" : "public/js/image_view.js"}


# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "advantisquartz.utils.jinja_methods",
#	"filters": "advantisquartz.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "advantisquartz.install.before_install"
# after_install = "advantisquartz.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "advantisquartz.uninstall.before_uninstall"
# after_uninstall = "advantisquartz.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "advantisquartz.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

override_doctype_class = {
	"Gratuity": "advantisquartz.overrides.Gratuity",
    "Employee Checkin": "advantisquartz.employee_checkin.EmployeeCheckin",
    "Salary Slip": "advantisquartz.salary_slip.SalarySlip"
    # "Stock Reconciliation": "advantisquartz.stock_reconciliation.StockReconciliation"
}

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------
scheduler_events = {
    "generate_leave_allocation": {
       "00 00 * * *": [
            "advantisquartz.advantisquartz.doctype.api.generate_leave_allocation"
        ]
    },
    "set_attendance_date":{
        "50 23 * * *": [
            "advantisquartz.advantisquartz.doctype.api.set_attendance_date"
        ]
    }
    
    # "daily": [
	# 	"advantisquartz.advantisquartz.doctype.api.generate_leave_allocation"
	# ]
}
# scheduler_events = {
#	"all": [
#		"advantisquartz.tasks.all"
#	],
#	"daily": [
#		"advantisquartz.tasks.daily"
#	],
#	"hourly": [
#		"advantisquartz.tasks.hourly"
#	],
#	"weekly": [
#		"advantisquartz.tasks.weekly"
#	],
#	"monthly": [
#		"advantisquartz.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "advantisquartz.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "advantisquartz.event.get_events"
# }
override_whitelisted_methods = {
	"hrms.hr.doctype.employee_checkin.employee_checkin.add_log_based_on_employee_field": "advantisquartz.employee_checkin.add_log_based_on_employee_field"
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "advantisquartz.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["advantisquartz.utils.before_request"]
# after_request = ["advantisquartz.utils.after_request"]

# Job Events
# ----------
# before_job = ["advantisquartz.utils.before_job"]
# after_job = ["advantisquartz.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"advantisquartz.auth.validate"
# ]
 
fixtures = [
    "Workflow",
    "Workflow State",
    "Role",
    "Workflow Action Master",
    {"dt":"Server Script","filters":[
        [
            "module","in",[
               "advantisquartz"
            ],
        ]
    ]},
    {"dt":"Custom Field","filters":[
        [
            "module","in",[
               "advantisquartz"
            ]
        ]
    ]},
    {"dt":"Client Script","filters":[
        [
            "module","in",[
               "advantisquartz"
            ],
        ]
    ]},
    {"dt":"Dashboard","filters":[
        [
            "name","in",[
                "Advantis Selling",
                "AQ Stock Dashboard",
                "AQ Buying Dashboard",
                "Employee Asset",
                "Gate Entry"
            ]
        ]
    ]},
    {"dt":"Print Format","filters":[
        [
        "module","in",[
                "advantisquartz"
            ]
        ]
    ]},
    {"dt":"Report","filters":[
        [
            "module","in",[
                "advantisquartz"
            ]
        ]
    ]},
    {"dt":"Notification","filters":[
        [
            "module","in",[
                "advantisquartz"
            ]
        ]
    ]},
    {"dt":"Workspace","filters":[
        [
            "name","in",[
                "Employee Request",
                "Employee Lifecycle",
                "Buying",
                "Stock",
                "Manufacturing",
                "Selling",
                "Quality",
                "HR",
                "Gate Pass"
            ]
        ]
    ]}
]