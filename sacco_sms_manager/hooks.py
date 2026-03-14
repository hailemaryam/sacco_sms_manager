app_name = "sacco_sms_manager"
app_title = "Sacco Sms Manager"
app_publisher = "membership fee reminders"
app_description = "The system manages SACCO members and sends SMS notifications for:"
app_email = "hailemaryammecca@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "sacco_sms_manager",
# 		"logo": "/assets/sacco_sms_manager/logo.png",
# 		"title": "Sacco Sms Manager",
# 		"route": "/sacco_sms_manager",
# 		"has_permission": "sacco_sms_manager.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/sacco_sms_manager/css/sacco_sms_manager.css"
# app_include_js = "/assets/sacco_sms_manager/js/sacco_sms_manager.js"

# include js, css files in header of web template
# web_include_css = "/assets/sacco_sms_manager/css/sacco_sms_manager.css"
# web_include_js = "/assets/sacco_sms_manager/js/sacco_sms_manager.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "sacco_sms_manager/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Member": "public/js/member.js",
	"SMS Campaign": "public/js/sms_campaign.js",
	"Membership Fee Payment": "public/js/membership_fee_payment.js",
}
doctype_list_js = {
	"Member": "public/js/member_list.js",
}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "sacco_sms_manager/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "sacco_sms_manager.utils.jinja_methods",
# 	"filters": "sacco_sms_manager.utils.jinja_filters"
# }

# Installation
# ------------

after_install = "sacco_sms_manager.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "sacco_sms_manager.uninstall.before_uninstall"
# after_uninstall = "sacco_sms_manager.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "sacco_sms_manager.utils.before_app_install"
# after_app_install = "sacco_sms_manager.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "sacco_sms_manager.utils.before_app_uninstall"
# after_app_uninstall = "sacco_sms_manager.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "sacco_sms_manager.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
	"daily": [
		"sacco_sms_manager.tasks.daily",
	],
	"hourly": [
		"sacco_sms_manager.tasks.process_scheduled_sms_campaigns",
	],
}

# Testing
# -------

# before_tests = "sacco_sms_manager.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "sacco_sms_manager.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "sacco_sms_manager.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
override_doctype_dashboards = {}

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["sacco_sms_manager.utils.before_request"]
# after_request = ["sacco_sms_manager.utils.after_request"]

# Job Events
# ----------
# before_job = ["sacco_sms_manager.utils.before_job"]
# after_job = ["sacco_sms_manager.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"sacco_sms_manager.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

