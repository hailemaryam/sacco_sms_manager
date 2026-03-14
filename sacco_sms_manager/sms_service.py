# Copyright (c) 2025, Sacco SMS Manager and contributors
# License: MIT. See LICENSE

"""SMS Service - Reusable module for sending SMS via configured gateway."""

from datetime import datetime

import requests

import frappe


def get_sms_settings():
	"""Get active SMS Settings. Returns None if not configured."""
	try:
		settings = frappe.get_single("SMS Settings")
		if settings.is_active and settings.api_url:
			return settings
	except Exception:
		pass
	return None


def send_sms(
	phone: str,
	message: str,
	member: str | None = None,
	sms_campaign: str | None = None,
) -> dict:
	"""
	Send a single SMS to the given phone number.
	Uses SMS Settings for gateway configuration.
	Creates SACCO SMS Log entry.

	Returns: {"success": bool, "provider_response": str, "log_name": str}
	"""
	settings = get_sms_settings()
	if not settings:
		frappe.throw("SMS Settings not configured or inactive. Please configure SMS Settings.")

	# Normalize phone number
	phone = _normalize_phone(phone)
	if not phone:
		frappe.throw("Invalid phone number.")

	log_doc = frappe.get_doc(
		{
			"doctype": "SACCO SMS Log",
			"member": member,
			"phone": phone,
			"message": message,
			"send_status": "Pending",
			"timestamp": datetime.now(),
			"sms_campaign": sms_campaign,
		}
	)
	log_doc.insert(ignore_permissions=True)

	try:
		response = _call_sms_gateway(settings, phone, message)
		log_doc.send_status = "Sent"
		log_doc.provider_response = str(response) if response else "Success"
		log_doc.save(ignore_permissions=True)
		return {"success": True, "provider_response": str(response), "log_name": log_doc.name}
	except Exception as e:
		log_doc.send_status = "Failed"
		log_doc.provider_response = str(e)
		log_doc.save(ignore_permissions=True)
		raise


def send_bulk_sms(phones: list[str], message: str) -> dict:
	"""
	Send SMS to multiple phone numbers.
	Returns: {"success_count": int, "failed_count": int, "results": list}
	"""
	results = []
	success_count = 0
	failed_count = 0

	for phone in phones:
		try:
			send_sms(phone, message)
			success_count += 1
			results.append({"phone": phone, "success": True})
		except Exception as e:
			failed_count += 1
			results.append({"phone": phone, "success": False, "error": str(e)})

	return {
		"success_count": success_count,
		"failed_count": failed_count,
		"results": results,
	}


def _normalize_phone(phone: str) -> str:
	"""Normalize phone number - remove spaces, ensure format."""
	if not phone:
		return ""
	return "".join(c for c in str(phone).strip() if c.isdigit() or c == "+")


def _call_sms_gateway(settings, phone: str, message: str) -> str | None:
	"""
	Call the SMS gateway API.
	Supports generic REST APIs - customize for your provider (e.g., Africa's Talking, Twilio).
	"""
	api_url = settings.api_url.strip()
	api_key = settings.get_password("api_key") or ""
	sender_id = settings.sender_id or ""

	# Generic HTTP POST - adapt headers/body to your provider
	headers = {
		"Content-Type": "application/json",
		"Authorization": f"Bearer {api_key}",
	}
	payload = {
		"phone": phone,
		"message": message,
		"sender": sender_id,
	}

	response = requests.post(api_url, json=payload, headers=headers, timeout=30)
	response.raise_for_status()
	return response.text
