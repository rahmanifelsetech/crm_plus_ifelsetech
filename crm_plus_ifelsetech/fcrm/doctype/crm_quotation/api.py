# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _


@frappe.whitelist()
def get_quotations_for_deal(deal_name):
	"""Get all quotations linked to a specific CRM Deal"""
	quotations = frappe.get_all(
		"CRM Quotation",
		filters={"crm_deal": deal_name},
		fields=[
			"name",
			"party_name",
			"transaction_date",
			"valid_till",
			"status",
			"grand_total",
			"currency",
			"order_type",
			"quotation_to",
			"modified",
			"owner"
		],
		order_by="transaction_date desc"
	)

	return quotations


@frappe.whitelist()
def create_quotation_from_deal(deal_name):
	"""Create a new quotation from a CRM Deal"""
	deal = frappe.get_doc("CRM Deal", deal_name)

	quotation = frappe.new_doc("CRM Quotation")
	quotation.crm_deal = deal_name
	quotation.organization = deal.organization
	quotation.party_name = deal.organization

	# Set default values
	quotation.quotation_to = "Lead"
	quotation.status = "Draft"
	quotation.currency = "USD"

	# Get deal contacts if any
	if deal.contacts:
		first_contact = deal.contacts[0]
		quotation.contact_person = first_contact.contact

	return quotation.as_dict()
