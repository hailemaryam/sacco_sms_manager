# Copyright (c) 2025, Sacco SMS Manager and contributors
# License: MIT. See LICENSE

import frappe
from frappe.model.document import Document

from sacco_sms_manager.sms_service import send_sms


class SMSCampaign(Document):
	def get_phone_list(self):
		"""Get list of (phone, member) tuples to send SMS to."""
		if self.send_to_all_members:
			result = frappe.get_all(
				"Member",
				filters={"status": "Active"},
				fields=["name", "phone"],
			)
			return [(r["phone"], r["name"]) for r in result if r.get("phone")]
		return [
			(frappe.db.get_value("Member", row.member, "phone"), row.member)
			for row in self.target_members
			if row.member
		]

	@frappe.whitelist()
	def send_now(self):
		"""Send SMS to all target members immediately."""
		if self.status == "Sent":
			frappe.throw("Campaign has already been sent.")

		recipients = self.get_phone_list()
		if not recipients:
			frappe.throw("No valid phone numbers to send SMS to.")

		success_count = 0
		for phone, member in recipients:
			if not phone:
				continue
			try:
				send_sms(phone, self.message_body, member=member, sms_campaign=self.name)
				success_count += 1
			except Exception as e:
				frappe.log_error(
					title=f"SMS Campaign Send Failed: {self.name}",
					message=str(e),
				)

		self.status = "Sent"
		self.save(ignore_permissions=True)
		return {"success": True, "sent_count": success_count, "total": len(recipients)}
