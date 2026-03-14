# Copyright (c) 2025, Sacco SMS Manager and contributors
# License: MIT. See LICENSE

import unittest

import frappe


class TestMember(unittest.TestCase):
	def setUp(self):
		pass

	def test_full_name(self):
		"""Test that full_name is set from first, middle, last name."""
		doc = frappe.new_doc("Member")
		doc.first_name = "John"
		doc.middle_name = "Robert"
		doc.last_name = "Doe"
		doc.phone = "+1234567890"
		doc.validate()
		assert doc.full_name == "John Robert Doe"

	def test_full_name_no_middle(self):
		"""Test full_name without middle name."""
		doc = frappe.new_doc("Member")
		doc.first_name = "Jane"
		doc.last_name = "Smith"
		doc.phone = "+1234567890"
		doc.validate()
		assert doc.full_name == "Jane Smith"


class TestMembershipFeePayment(unittest.TestCase):
	def test_status_paid_when_payment_date(self):
		"""Test that status becomes Paid when payment_date is set."""
		import frappe
		from frappe.utils import add_days, nowdate

		member = frappe.get_doc(
			{
				"doctype": "Member",
				"first_name": "Test",
				"last_name": "User",
				"phone": "+1234567890",
				"status": "Active",
			}
		).insert()

		payment = frappe.get_doc(
			{
				"doctype": "Membership Fee Payment",
				"member": member.name,
				"amount": 100,
				"due_date": add_days(nowdate(), 7),
			}
		)
		payment.validate()
		assert payment.payment_status == "Pending"

		payment.payment_date = nowdate()
		payment.validate()
		assert payment.payment_status == "Paid"

		# Cleanup
		payment.delete()
		member.delete()
