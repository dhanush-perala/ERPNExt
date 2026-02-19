app_name = "ursc_cms_app"
app_title = "ISRO CMS"
app_publisher = "neemus"
app_description = "ERPnext based app"
app_email = "goutham.krishna@neemus.com"
app_license = "mit"

app_logo_url = "/assets/ursc_cms_app/images/logo1.png"
app_favicon = "/assets/ursc_cms_app/images/logo1.png"

# Background image for login page
# Configured in: apps/frappe/frappe/public/scss/login.bundle.scss
login_background_image = "/assets/ursc_cms_app/images/image.png"

# Include CSS
app_include_css = "/assets/ursc_cms_app/css/custom.css"

# Modules
MODULES = ["ISRO CMS", "URSC CMS App"]

# Core Doctypes
CORE_DTYPES = [
    # ERPNext core doctypes
    "Item", "Item Group", "Supplier", "Warehouse",
    "Quality Inspection", "Quality Inspection Template",
    # SRV Doctypes
]

# frappe-bench/apps/your_custom_app/your_custom_app/hooks.py
 
# Fixtures to export and import standard configuration changes
fixtures = [
    "Custom Field",
    "Property Setter",
    "Client Script",
    "Server Script",
    "Print Format",
    "Report",
    "Workflow",
    "Workflow State",
    "Workflow Action Master",
    "Dashboard",
    "Dashboard Chart",
    "Workspace",
]

doctype_js = {
    "Purchase Order": "public/js/purchase_order_custom.js",
    "Stock Entry": "public/js/stock_entry_custom.js",
        "BOM": "public/js/bom_custom.js",
}
'''    "Purchase Order": {
        "validate": "ursc_cms_app.api.validate_supplier_items"
    },'''
# --- Document Events ---
doc_events = {
    # Purchase Order validation: enforce supplier → item relationship
   
    "DPA Request": {
        "on_update": "ursc_cms_app.api.handle_dpa_workflow"    },
    # Stock Entry validation: populate base + MDB part numbers
    "Stock Entry": {
        "validate": "ursc_cms_app.api.populate_mdb_part_no",
         "on_submit": "ursc_cms_app.cardex.stock_entry.on_submit",
        "on_cancel": "ursc_cms_app.cardex.stock_entry.on_cancel",
    },
        "Warehouse Location Master": {
        "validate": "ursc_cms_app.cardex.validations.validate_location_master"
    },
        "Alternate Part Disable": {
        "on_submit": "ursc_cms_app.events.alternate_part_disable_on_submit"}

    #    "GENERATE REQUEST - KITTED COMPONENTS": {
    #    "after_cancel": "ursc_cms_app.isro_cms.doctype.generate_request___kitted_components.generate_request___kitted_components.cancel_linked_sales_order_after_cancel"
    #}
}
 
# --- Patches / Fixes ---
after_migrate = ["ursc_cms_app.api.fix_item_title_field"]


 
# Note: You can add more complex fixtures with filters
# to export specific data records, for example:
#
# fixtures = [
#     ...,
#     {"doctype": "Role", "filters": [["name", "in", ["Sales Manager", "HR Manager"]]]}
# ]
 

# Optional commented hooks (cleaned)
# before_install = "ursc_cms_app.install.before_install"
# after_install = "ursc_cms_app.install.after_install"
# before_uninstall = "ursc_cms_app.uninstall.before_uninstall"
# after_uninstall = "ursc_cms_app.uninstall.after_uninstall"
# doc_events = {}
# scheduler_events = {}
# auth_hooks = []
# override_doctype_class = {}
# override_whitelisted_methods = {}
# override_doctype_dashboards = {}
# user_data_fields = []

# End of hooks.py

# Apps
 
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
 
# add_to_apps_screen = [
 
#   {
 
#       "name": "ursc_cms_app",
 
#       "logo": "/assets/ursc_cms_app/logo.png",
 
#       "title": "ISRO CMS",
 
#       "route": "/ursc_cms_app",
 
#       "has_permission": "ursc_cms_app.api.permission.has_app_permission"
 
#   }
 
# ]

# Includes in <head>
 
# ------------------

# include js, css files in header of desk.html
 
# app_include_css = "/assets/ursc_cms_app/css/ursc_cms_app.css"
 
# app_include_js = "/assets/ursc_cms_app/js/ursc_cms_app.js"

# include js, css files in header of web template
 
# web_include_css = "/assets/ursc_cms_app/css/ursc_cms_app.css"
 
# web_include_js = "/assets/ursc_cms_app/js/ursc_cms_app.js"

# include custom scss in every website theme (without file extension ".scss")
 
# website_theme_scss = "ursc_cms_app/public/scss/website"

# include js, css files in header of web form
 
# webform_include_js = {"doctype": "public/js/doctype.js"}
 
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
 
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
 
# doctype_js = {"doctype" : "public/js/doctype.js"}
 
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
 
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
 
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
 
# ------------------
 
# include app icons in desk
 
# app_include_icons = "ursc_cms_app/public/icons.svg"

# Home Pages
 
# ----------

# application home page (will override Website Settings)
 
# home_page = "login"

# website user home page (by Role)
 
# role_home_page = {
 
#   "Role": "home_page"
 
# }

# Generators
 
# ----------

# automatically create page for each record of this doctype
 
# website_generators = ["Web Page"]

# Jinja
 
# ----------

# add methods and filters to jinja environment
 
# jinja = {
 
#   "methods": "ursc_cms_app.utils.jinja_methods",
 
#   "filters": "ursc_cms_app.utils.jinja_filters"
 
# }

# Installation
 
# ------------

# before_install = "ursc_cms_app.install.before_install"
 
# after_install = "ursc_cms_app.install.after_install"

# Uninstallation
 
# ------------

# before_uninstall = "ursc_cms_app.uninstall.before_uninstall"
 
# after_uninstall = "ursc_cms_app.uninstall.after_uninstall"

# Integration Setup
 
# ------------------
 
# To set up dependencies/integrations with other apps
 
# Name of the app being installed is passed as an argument

# before_app_install = "ursc_cms_app.utils.before_app_install"
 
# after_app_install = "ursc_cms_app.utils.after_app_install"

# Integration Cleanup
 
# -------------------
 
# To clean up dependencies/integrations with other apps
 
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "ursc_cms_app.utils.before_app_uninstall"
 
# after_app_uninstall = "ursc_cms_app.utils.after_app_uninstall"

# Desk Notifications
 
# ------------------
 
# See frappe.core.notifications.get_notification_config

# notification_config = "ursc_cms_app.notifications.get_notification_config"

# Permissions
 
# -----------
 
# Permissions evaluated in scripted ways

# permission_query_conditions = {
 
#   "Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
 
# }
 
#
 
# has_permission = {
 
#   "Event": "frappe.desk.doctype.event.event.has_permission",
 
# }

# DocType Class
 
# ---------------
 
# Override standard doctype classes

# override_doctype_class = {
 
#   "ToDo": "custom_app.overrides.CustomToDo"
 
# }

# Document Events
 
# ---------------
 
# Hook on document methods and events

# doc_events = {
 
#   "*": {
 
#       "on_update": "method",
 
#       "on_cancel": "method",
 
#       "on_trash": "method"
 
#   }
 
# }

# Scheduled Tasks
 
# ---------------

scheduler_events = {
	"daily": [
		"ursc_cms_app.isro_cms.doctype.siv.siv.inactivate_old_siv_records"
	],
}

# Testing
 
# -------

# before_tests = "ursc_cms_app.install.before_tests"

# Overriding Methods
 
# ------------------------------
 
#
 
# override_whitelisted_methods = {
 
#   "frappe.desk.doctype.event.event.get_events": "ursc_cms_app.event.get_events"
 
# }
 
#
 
# each overriding function accepts a `data` argument;
 
# generated from the base implementation of the doctype dashboard,
 
# along with any modifications made in other Frappe apps
 
# override_doctype_dashboards = {
 
#   "Task": "ursc_cms_app.task.get_dashboard_data"
 
# }

# exempt linked doctypes from being automatically cancelled
 
#
 
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
 
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
 
# ----------------
 
# before_request = ["ursc_cms_app.utils.before_request"]
 
# after_request = ["ursc_cms_app.utils.after_request"]

# Job Events
 
# ----------
 
# before_job = ["ursc_cms_app.utils.before_job"]
 
# after_job = ["ursc_cms_app.utils.after_job"]

# User Data Protection
 
# --------------------

# user_data_fields = [
 
#   {
 
#       "doctype": "{doctype_1}",
 
#       "filter_by": "{filter_by}",
 
#       "redact_fields": ["{field_1}", "{field_2}"],
 
#       "partial": 1,
 
#   },
 
#   {
 
#       "doctype": "{doctype_2}",
 
#       "filter_by": "{filter_by}",
 
#       "partial": 1,
 
#   },
 
#   {
 
#       "doctype": "{doctype_3}",
 
#       "strict": False,
 
#   },
 
#   {
 
#       "doctype": "{doctype_4}"
 
#   }
 
# ]

# Authentication and authorization
 
# --------------------------------

# auth_hooks = [
 
#   "ursc_cms_app.auth.validate"
 
# ]

# Automatically update python controller files with type annotations for this app.
 
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
 
#   "Logging DocType Name": 30  # days to retain logs
 
# }


 
