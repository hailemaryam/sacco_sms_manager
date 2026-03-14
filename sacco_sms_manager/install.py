# Copyright (c) 2025, Sacco SMS Manager and contributors
# License: MIT. See LICENSE

import frappe


def after_install():
	"""Run after app installation: create roles, default settings, workspace."""
	create_roles()
	create_default_sms_settings()
	create_sacco_workspace()


def create_roles():
	"""Create SACCO roles if they don't exist."""
	roles = ["SACCO Admin", "SACCO Officer", "Accountant"]
	for role_name in roles:
		if not frappe.db.exists("Role", role_name):
			frappe.get_doc({"doctype": "Role", "role_name": role_name}).insert(
				ignore_permissions=True
			)
	frappe.db.commit()


def create_default_sms_settings():
	"""Create SMS Settings single doc if not exists."""
	if not frappe.db.exists("SMS Settings", "SMS Settings"):
		# Single doc - name is always the doctype name
		frappe.get_doc(
			{
				"doctype": "SMS Settings",
				"provider_name": "Default",
				"api_url": "https://api.example.com/sms/send",
				"api_key": "",
				"sender_id": "SACCO",
				"is_active": 0,
			}
		).insert(ignore_permissions=True)
		frappe.db.commit()


def create_sacco_workspace():
	"""Create SACCO workspace with dashboard and links."""
	if frappe.db.exists("Workspace", "SACCO"):
		return

	# Create number cards for dashboard
	cards = [
		{
			"doctype": "Number Card",
			"name": "Total Members",
			"label": "Total Members",
			"document_type": "Member",
			"function": "Count",
			"type": "Document Type",
			"is_standard": 1,
			"module": "Sacco Sms Manager",
		},
		{
			"doctype": "Number Card",
			"name": "Active Members",
			"label": "Active Members",
			"document_type": "Member",
			"function": "Count",
			"type": "Document Type",
			"filters_json": '[["Member","status","=","Active"]]',
			"is_standard": 1,
			"module": "Sacco Sms Manager",
		},
		{
			"doctype": "Number Card",
			"name": "Pending Membership Payments",
			"label": "Pending Membership Payments",
			"document_type": "Membership Fee Payment",
			"function": "Count",
			"type": "Document Type",
			"filters_json": '[["Membership Fee Payment","payment_status","in",["Pending","Overdue"]]]',
			"is_standard": 1,
			"module": "Sacco Sms Manager",
		},
		{
			"doctype": "Number Card",
			"name": "Pending Loan Payments",
			"label": "Pending Loan Payments",
			"document_type": "Loan Saving Payment",
			"function": "Count",
			"type": "Document Type",
			"filters_json": '[["Loan Saving Payment","payment_status","in",["Pending","Overdue"]]]',
			"is_standard": 1,
			"module": "Sacco Sms Manager",
		},
		{
			"doctype": "Number Card",
			"name": "SMS Sent Today",
			"label": "SMS Sent Today",
			"type": "Custom",
			"method": "sacco_sms_manager.dashboard.get_sms_sent_today",
			"is_standard": 1,
			"module": "Sacco Sms Manager",
		},
	]
	for card_data in cards:
		if not frappe.db.exists("Number Card", card_data["name"]):
			frappe.get_doc(card_data).insert(ignore_permissions=True)

	# Create workspace
	content = (
        '[{"id":"card1","type":"number_card","data":{"number_card_name":"Total Members","col":4}},'
        '{"id":"card2","type":"number_card","data":{"number_card_name":"Active Members","col":4}},'
        '{"id":"card3","type":"number_card","data":{"number_card_name":"Pending Membership Payments","col":4}},'
        '{"id":"card4","type":"number_card","data":{"number_card_name":"Pending Loan Payments","col":4}},'
        '{"id":"card5","type":"number_card","data":{"number_card_name":"SMS Sent Today","col":4}}]'
    )
	workspace = frappe.get_doc(
		{
			"doctype": "Workspace",
			"name": "SACCO",
			"title": "SACCO",
			"label": "SACCO",
			"icon": "users",
			"module": "Sacco Sms Manager",
			"app": "sacco_sms_manager",
			"content": content,
			"public": 1,
			"links": [
				{"label": "Members", "link_to": "Member", "link_type": "DocType", "type": "Link"},
				{"label": "SMS Campaigns", "link_to": "SMS Campaign", "link_type": "DocType", "type": "Link"},
				{"label": "Membership Fees", "link_to": "Membership Fee Payment", "link_type": "DocType", "type": "Link"},
				{"label": "Loan/Saving Payments", "link_to": "Loan Saving Payment", "link_type": "DocType", "type": "Link"},
				{"label": "SMS Logs", "link_to": "SACCO SMS Log", "link_type": "DocType", "type": "Link"},
				{"label": "SMS Settings", "link_to": "SMS Settings", "link_type": "DocType", "type": "Link"},
			],
		}
	)
	workspace.insert(ignore_permissions=True)
	frappe.db.commit()
