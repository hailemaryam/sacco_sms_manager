# Copyright (c) 2025, Sacco SMS Manager and contributors
# License: MIT. See LICENSE

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, nowdate


class LoanSavingPayment(Document):
	def validate(self):
		self.update_payment_status()

	def update_payment_status(self):
		"""Update status based on payment_date and due_date."""
		if self.payment_date:
			self.payment_status = "Paid"
		elif self.due_date and getdate(self.due_date) < getdate(nowdate()):
			self.payment_status = "Overdue"
		else:
			self.payment_status = "Pending"
