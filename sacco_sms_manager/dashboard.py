# Copyright (c) 2025, Sacco SMS Manager and contributors
# License: MIT. See LICENSE

"""Dashboard data for SACCO SMS Manager."""

import frappe
from frappe.utils import nowdate


@frappe.whitelist()
def get_sms_sent_today():
	"""Return count of SMS sent today for number card."""
	today = nowdate()
	count = frappe.db.count(
		"SACCO SMS Log",
		filters={"send_status": "Sent", "creation": [">=", today]},
	)
	return {"value": count, "fieldtype": "Int"}


@frappe.whitelist()
def get_dashboard_data():
	"""Return dashboard stats for API."""
	today = nowdate()
	return {
		"total_members": frappe.db.count("Member"),
		"active_members": frappe.db.count("Member", {"status": "Active"}),
		"pending_membership_payments": frappe.db.count(
			"Membership Fee Payment",
			{"payment_status": ["in", ["Pending", "Overdue"]]},
		),
		"pending_loan_payments": frappe.db.count(
			"Loan Saving Payment",
			{"payment_status": ["in", ["Pending", "Overdue"]]},
		),
		"sms_sent_today": frappe.db.count(
			"SACCO SMS Log",
			{"send_status": "Sent", "creation": [">=", today]},
		),
	}
