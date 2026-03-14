# Copyright (c) 2025, Sacco SMS Manager and contributors
# License: MIT. See LICENSE

import frappe
from frappe.model.document import Document


class Member(Document):
	def validate(self):
		self.set_full_name()
		# Sync member_id with document name (MEM-00001 format)
		if self.name and self.name.startswith("MEM-"):
			self.member_id = self.name

	def set_full_name(self):
		"""Build full name from first, middle, and last name."""
		parts = [self.first_name, self.middle_name or "", self.last_name]
		self.full_name = " ".join(p for p in parts if p).strip()

	def on_update(self):
		if self.name and self.name.startswith("MEM-"):
			self.db_set("member_id", self.name, update_modified=False)
