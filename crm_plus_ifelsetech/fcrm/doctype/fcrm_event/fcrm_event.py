# Copyright (c) 2024, pythona@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FCRMEvent(Document):
	def validate(self):
		if self.ends_on and self.starts_on:
			if self.ends_on < self.starts_on:
				frappe.throw("End time cannot be before start time")
