# Copyright (c) 2025, Sacco SMS Manager and contributors
# License: MIT. See LICENSE

"""REST API endpoints for SACCO SMS Manager."""

import frappe
from frappe import _


@frappe.whitelist()
def send_sms_to_member(member: str, message: str):
	"""Send SMS to a single member by member ID/name."""
	frappe.only_for(["SACCO Admin", "SACCO Officer"])
	member_doc = frappe.get_doc("Member", member)
	if not member_doc.phone:
		frappe.throw(_("Member has no phone number."))
	from sacco_sms_manager.sms_service import send_sms

	result = send_sms(member_doc.phone, message, member=member)
	return result


@frappe.whitelist()
def send_bulk_sms(members: list[str] | str, message: str):
	"""Send SMS to multiple members. members can be JSON list or comma-separated."""
	frappe.only_for(["SACCO Admin", "SACCO Officer"])
	if isinstance(members, str):
		import json

		try:
			members = json.loads(members)
		except json.JSONDecodeError:
			members = [m.strip() for m in members.split(",")]
	phones = []
	for m in members:
		phone = frappe.db.get_value("Member", m, "phone")
		if phone:
			phones.append(phone)
	if not phones:
		frappe.throw(_("No valid phone numbers found."))
	from sacco_sms_manager.sms_service import send_bulk_sms

	return send_bulk_sms(phones, message)


@frappe.whitelist()
def send_campaign_now(campaign_name: str):
	"""Trigger SMS campaign send by name."""
	frappe.only_for(["SACCO Admin", "SACCO Officer"])
	campaign = frappe.get_doc("SMS Campaign", campaign_name)
	return campaign.send_now()


@frappe.whitelist()
def get_dashboard_stats():
	"""Get dashboard statistics (no auth required if user has read on Member)."""
	from sacco_sms_manager.dashboard import get_dashboard_data

	return get_dashboard_data()


@frappe.whitelist()
def send_membership_fee_reminder(payment_name: str):
	"""Manually trigger membership fee reminder for a payment."""
	frappe.only_for(["SACCO Admin", "SACCO Officer", "Accountant"])
	from sacco_sms_manager.sms_service import send_sms

	payment = frappe.get_doc("Membership Fee Payment", payment_name)
	if payment.payment_status == "Paid":
		frappe.throw(_("Payment is already marked as paid."))
	member_doc = frappe.get_cached_doc("Member", payment.member)
	if not member_doc.phone:
		frappe.throw(_("Member has no phone number."))
	message = (
		f"Dear {member_doc.full_name or member_doc.first_name}, "
		f"your SACCO membership fee of {payment.amount} is due on {payment.due_date}. "
		"Please make payment on time."
	)
	send_sms(member_doc.phone, message, member=payment.member)
	return {"success": True}


@frappe.whitelist()
def send_loan_saving_payment_reminder(payment_name: str):
	"""Manually trigger loan/saving payment reminder for a payment."""
	frappe.only_for(["SACCO Admin", "SACCO Officer", "Accountant"])
	from sacco_sms_manager.sms_service import send_sms

	payment = frappe.get_doc("Loan Saving Payment", payment_name)
	if payment.payment_status == "Paid":
		frappe.throw(_("Payment is already marked as paid."))
	member_doc = frappe.get_cached_doc("Member", payment.member)
	if not member_doc.phone:
		frappe.throw(_("Member has no phone number."))
	message = (
		f"Dear {member_doc.full_name or member_doc.first_name}, "
		f"your SACCO {payment.payment_type} payment of {payment.amount} is due on {payment.due_date}. "
		"Please make payment on time."
	)
	send_sms(member_doc.phone, message, member=payment.member)
	return {"success": True}
