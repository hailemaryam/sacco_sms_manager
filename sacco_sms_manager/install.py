# Copyright (c) 2025, Sacco SMS Manager and contributors
# License: MIT. See LICENSE

import frappe


def after_install():
	"""Run after app installation: create roles, default settings, workspace."""
	create_roles()
	create_default_sms_settings()
	create_sacco_workspace()


def after_migrate():
	"""Run after migrate: ensure SACCO workspace and menu exist."""
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
	"""Create SACCO SMS Settings single doc if not exists."""
	if not frappe.db.exists("SACCO SMS Settings", "SACCO SMS Settings"):
		frappe.get_doc(
			{
				"doctype": "SACCO SMS Settings",
				"provider_name": "Default",
				"api_url": "https://api.example.com/sms/send",
				"api_key": "",
				"sender_id": "SACCO",
				"is_active": 0,
			}
		).insert(ignore_permissions=True)
		frappe.db.commit()


def create_sacco_workspace():
	"""Create SACCO workspace with dashboard, links, shortcuts, and sidebar menu."""
	# Create number cards for dashboard (recreate if missing)
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

	content = (
		'[{"id":"card1","type":"number_card","data":{"number_card_name":"Total Members","col":4}},'
		'{"id":"card2","type":"number_card","data":{"number_card_name":"Active Members","col":4}},'
		'{"id":"card3","type":"number_card","data":{"number_card_name":"Pending Membership Payments","col":4}},'
		'{"id":"card4","type":"number_card","data":{"number_card_name":"Pending Loan Payments","col":4}},'
		'{"id":"card5","type":"number_card","data":{"number_card_name":"SMS Sent Today","col":4}}]'
	)

	link_items = [
		{"label": "Members", "link_to": "Member", "link_type": "DocType", "type": "Link"},
		{"label": "SMS Campaigns", "link_to": "SMS Campaign", "link_type": "DocType", "type": "Link"},
		{"label": "Membership Fees", "link_to": "Membership Fee Payment", "link_type": "DocType", "type": "Link"},
		{"label": "Loan/Saving Payments", "link_to": "Loan Saving Payment", "link_type": "DocType", "type": "Link"},
		{"label": "SMS Logs", "link_to": "SACCO SMS Log", "link_type": "DocType", "type": "Link"},
		{"label": "SACCO SMS Settings", "link_to": "SACCO SMS Settings", "link_type": "DocType", "type": "Link"},
	]

	shortcut_items = [
		{"label": "Members", "link_to": "Member", "type": "DocType", "icon": "users"},
		{"label": "SMS Campaigns", "link_to": "SMS Campaign", "type": "DocType", "icon": "mail"},
		{"label": "Membership Fees", "link_to": "Membership Fee Payment", "type": "DocType", "icon": "credit-card"},
		{"label": "Loan/Saving Payments", "link_to": "Loan Saving Payment", "type": "DocType", "icon": "file-text"},
		{"label": "SMS Logs", "link_to": "SACCO SMS Log", "type": "DocType", "icon": "list"},
		{"label": "SACCO SMS Settings", "link_to": "SACCO SMS Settings", "type": "DocType", "icon": "settings"},
	]

	if frappe.db.exists("Workspace", "SACCO"):
		workspace = frappe.get_doc("Workspace", "SACCO")
		workspace.content = content
		workspace.standard = 1
		workspace.links = []
		workspace.shortcuts = []
		workspace.number_cards = []
		for item in link_items:
			workspace.append("links", item)
		for item in shortcut_items:
			workspace.append("shortcuts", item)
		for card in cards:
			workspace.append("number_cards", {
				"number_card_name": card["name"],
				"label": card["label"]
			})
		workspace.save(ignore_permissions=True)
	else:
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
				"standard": 1,
			}
		)
		for item in link_items:
			workspace.append("links", item)
		for item in shortcut_items:
			workspace.append("shortcuts", item)
		for card in cards:
			workspace.append("number_cards", {
				"number_card_name": card["name"],
				"label": card["label"]
			})
		workspace.insert(ignore_permissions=True)

	# Create or update Workspace Sidebar for menu
	create_sacco_workspace_sidebar()
	frappe.db.commit()


def create_sacco_workspace_sidebar():
	"""Create Workspace Sidebar for SACCO menu."""
	from frappe.desk.doctype.workspace_sidebar.workspace_sidebar import create_workspace_sidebar_for_workspaces

	# Creates sidebar for any workspace that doesn't have one
	create_workspace_sidebar_for_workspaces()

	# Ensure SACCO sidebar has our menu items
	if frappe.db.exists("Workspace Sidebar", "SACCO"):
		sidebar = frappe.get_doc("Workspace Sidebar", "SACCO")
		sidebar.module = "Sacco Sms Manager"
		sidebar.app = "sacco_sms_manager"
		sidebar.header_icon = "users"
		sidebar.standard = 1
		# Rebuild items from workspace shortcuts
		workspace = frappe.get_doc("Workspace", "SACCO")
		items = [
			frappe._dict({"label": "Home", "link_to": "SACCO", "link_type": "Workspace", "type": "Link", "idx": -1, "icon": "home"})
		]
		for idx, s in enumerate(workspace.shortcuts or [], start=1):
			items.append(
				frappe._dict({
					"label": s.label,
					"link_to": s.link_to,
					"link_type": s.type,
					"type": "Link",
					"idx": idx,
					"icon": s.icon,
				})
			)
		sidebar.set("items", [])
		for item in items:
			sidebar.append("items", {
				"label": item.label,
				"link_to": item.link_to,
				"link_type": item.link_type,
				"type": "Link",
				"idx": item.idx,
				"icon": item.icon,
			})
		sidebar.save(ignore_permissions=True)
