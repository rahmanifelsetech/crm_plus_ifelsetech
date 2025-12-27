# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CRMQuotation(Document):
	def validate(self):
		"""Validate CRM Quotation"""
		self.validate_dates()

	def validate_dates(self):
		"""Validate transaction date and valid till date"""
		if self.valid_till and self.transaction_date:
			if self.valid_till < self.transaction_date:
				frappe.throw("Valid Till date cannot be before Transaction Date")

	def before_save(self):
		"""Set party name from deal or organization if not set"""
		if not self.party_name:
			if self.crm_deal:
				deal = frappe.get_doc("CRM Deal", self.crm_deal)
				if deal.organization:
					self.party_name = deal.organization
					self.organization = deal.organization
			elif self.organization:
				self.party_name = self.organization
