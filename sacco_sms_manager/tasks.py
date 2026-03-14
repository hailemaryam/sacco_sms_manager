# Copyright (c) 2025, Sacco SMS Manager and contributors
# License: MIT. See LICENSE

"""Scheduled tasks for SACCO SMS Manager."""

import frappe
from frappe.utils import add_days, getdate, nowdate

from sacco_sms_manager.sms_service import send_sms


def daily():
	"""Run daily: membership fee reminders and loan/saving payment reminders."""
	send_membership_fee_reminders()
	send_loan_saving_reminders()


def send_membership_fee_reminders():
	"""Send SMS reminders for membership fee payments: 3 days before, on due date, 3 days after."""
	today = getdate(nowdate())

	for reminder_type, target_date in [
		("3_days_before", add_days(today, 3)),
		("due_date", today),
		("3_days_after", add_days(today, -3)),
	]:
		payments = frappe.get_all(
			"Membership Fee Payment",
			filters={
				"payment_status": ["in", ["Pending", "Overdue"]],
				"due_date": target_date,
			},
			fields=["name", "member", "amount", "due_date"],
		)
		for payment in payments:
			if _reminder_already_sent("Membership Fee Payment", payment["name"], reminder_type):
				continue
			_send_membership_fee_reminder(payment, reminder_type)


def _send_membership_fee_reminder(payment: dict, reminder_type: str):
	"""Send membership fee reminder SMS."""
	member_doc = frappe.get_cached_doc("Member", payment["member"])
	if not member_doc.phone:
		return
	message = (
		f"Dear {member_doc.full_name or member_doc.first_name}, "
		f"your SACCO membership fee of {payment['amount']} is due on {payment['due_date']}. "
		"Please make payment on time."
	)
	try:
		send_sms(member_doc.phone, message, member=payment["member"])
		_log_reminder_sent("Membership Fee Payment", payment["name"], reminder_type)
	except Exception as e:
		frappe.log_error(
			title=f"Membership Fee Reminder Failed: {payment['name']}",
			message=str(e),
		)


def send_loan_saving_reminders():
	"""Send daily reminders for due loan/saving payments."""
	today = getdate(nowdate())
	payments = frappe.get_all(
		"Loan Saving Payment",
		filters={
			"payment_status": ["in", ["Pending", "Overdue"]],
			"due_date": ["<=", today],
		},
		fields=["name", "member", "payment_type", "amount", "due_date"],
	)
	for payment in payments:
		if _reminder_already_sent("Loan Saving Payment", payment["name"], "due_date"):
			continue
		_send_loan_saving_reminder(payment)


def _send_loan_saving_reminder(payment: dict):
	"""Send loan/saving payment reminder SMS."""
	member_doc = frappe.get_cached_doc("Member", payment["member"])
	if not member_doc.phone:
		return
	message = (
		f"Reminder: Your {payment['payment_type']} payment of {payment['amount']} "
		f"is due on {payment['due_date']}. Please complete your payment."
	)
	try:
		send_sms(member_doc.phone, message, member=payment["member"])
		_log_reminder_sent("Loan Saving Payment", payment["name"], "due_date")
	except Exception as e:
		frappe.log_error(
			title=f"Loan/Saving Reminder Failed: {payment['name']}",
			message=str(e),
		)


def _reminder_already_sent(doctype: str, docname: str, reminder_type: str) -> bool:
	"""Check if we already sent this reminder type for this document."""
	return bool(
		frappe.db.exists(
			"Payment Reminder Log",
			{
				"reference_doctype": doctype,
				"reference_name": docname,
				"reminder_type": reminder_type,
			},
		)
	)


def _log_reminder_sent(doctype: str, docname: str, reminder_type: str):
	"""Log that a reminder was sent."""
	frappe.get_doc(
		{
			"doctype": "Payment Reminder Log",
			"reference_doctype": doctype,
			"reference_name": docname,
			"reminder_type": reminder_type,
		}
	).insert(ignore_permissions=True)


def process_scheduled_sms_campaigns():
	"""Process SMS Campaigns that are scheduled for now or past."""
	campaigns = frappe.get_all(
		"SMS Campaign",
		filters={
			"status": "Scheduled",
			"scheduled_time": ["<=", frappe.utils.now()],
		},
		pluck="name",
	)
	for name in campaigns:
		try:
			doc = frappe.get_doc("SMS Campaign", name)
			doc.send_now()
		except Exception as e:
			frappe.log_error(title=f"Scheduled SMS Campaign Failed: {name}", message=str(e))
