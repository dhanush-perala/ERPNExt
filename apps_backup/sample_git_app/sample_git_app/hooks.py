
app_title = "Sample Git App"

app_publisher = "gk"

app_description = "Sample Git App Description"

app_email = "gouthamkrishna010111@gmail.com"

app_license = "MIT"
 
# Fixtures (Exported custom Doctypes, Fields, Reports, etc.)
# Fixtures (Exported custom Doctypes, Fields, Reports, etc.)
fixtures = [
    # Core metadata
    "Custom Field",
    "Property Setter",
    "Custom Script",
    "Client Script",
    "Server Script",
    "Web Page",
    "Web Form",
    "Website Theme",
    "Print Format",
    "Workflow",
    "Workflow State",
    "Workflow Action Master",
    "Report",
    "Dashboard Chart",
    "Notification",
    "Letter Head",
    "Role",
    "Custom DocPerm",
    "Role Profile",
    "Module Profile",
    "Translation",

    # ✅ Export all fully custom DocTypes (custom=1)
    {
        "dt": "DocType",
        "filters": [["custom", "=", 1]]
    }
]




# Includes in <head>

# ------------------

# app_include_css = "/assets/sample_git_app/css/sample_git_app.css"

# app_include_js = "/assets/sample_git_app/js/sample_git_app.js"

# web_include_css = "/assets/sample_git_app/css/sample_git_app.css"

# web_include_js = "/assets/sample_git_app/js/sample_git_app.js"
 
# Home Pages

# ----------

# home_page = "login"

# role_home_page = {

#     "Role": "home_page"

# }
 
# Generators

# ----------

# website_generators = ["Web Page"]
 
# Jinja

# -----

# jinja = {

#     "methods": "sample_git_app.utils.jinja_methods",

#     "filters": "sample_git_app.utils.jinja_filters"

# }
 
# Installation

# ------------

# before_install = "sample_git_app.install.before_install"

# after_install = "sample_git_app.install.after_install"
 
# Uninstallation

# --------------

# before_uninstall = "sample_git_app.uninstall.before_uninstall"

# after_uninstall = "sample_git_app.uninstall.after_uninstall"
 
# Desk Notifications

# ------------------

# notification_config = "sample_git_app.notifications.get_notification_config"
 
# Permissions

# -----------

# permission_query_conditions = {}

# has_permission = {}
 
# Document Events

# ---------------

# doc_events = {

#     "*": {

#         "on_update": "method",

#         "on_cancel": "method",

#         "on_trash": "method"

#     }

# }
 
# Scheduled Tasks

# ---------------

# scheduler_events = {

#     "all": ["sample_git_app.tasks.all"],

#     "daily": ["sample_git_app.tasks.daily"],

#     "hourly": ["sample_git_app.tasks.hourly"],

#     "weekly": ["sample_git_app.tasks.weekly"],

#     "monthly": ["sample_git_app.tasks.monthly"],

# }
 
# Testing

# -------

# before_tests = "sample_git_app.install.before_tests"
 
# Overriding Methods

# ------------------

# override_whitelisted_methods = {}
 
# override_doctype_dashboards = {}
 
# Request Events

# --------------

# before_request = ["sample_git_app.utils.before_request"]

# after_request = ["sample_git_app.utils.after_request"]
 
# Job Events

# ----------

# before_job = ["sample_git_app.utils.before_job"]

# after_job = ["sample_git_app.utils.after_job"]
 
# User Data Protection

# --------------------

# user_data_fields = []
 
# Authentication and authorization

# --------------------------------

# auth_hooks = ["sample_git_app.auth.validate"]

 
