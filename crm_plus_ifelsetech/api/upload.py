# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.handler import upload_file as frappe_upload_file


@frappe.whitelist()
def upload_file_with_metadata():
	"""
	Custom upload handler that supports custom fields like file_description and file_category.
	This extends Frappe's standard upload_file to handle metadata fields.
	"""
	try:
		# Use Frappe's standard upload_file to handle the file upload
		file_doc = frappe_upload_file()

		if not file_doc:
			frappe.throw(_("File upload failed"))

		# Get the File document
		if isinstance(file_doc, dict):
			file_name = file_doc.get("name")
		else:
			file_name = file_doc.name if hasattr(file_doc, "name") else file_doc

		if not file_name:
			frappe.throw(_("Could not get file name"))

		# Load the File document
		file_document = frappe.get_doc("File", file_name)

		# Update custom fields if provided using db.set_value to bypass validation
		file_description = frappe.form_dict.get("file_description")
		file_category = frappe.form_dict.get("file_category")

		updates = {}

		if file_description:
			updates["file_description"] = file_description

		if file_category:
			updates["file_category"] = file_category

		# Update using db.set_value to bypass field validation
		if updates:
			frappe.db.set_value("File", file_name, updates, update_modified=True)
			frappe.db.commit()
			# Reload the document to get updated values
			file_document.reload()

		# Return the file document data
		return file_document.as_dict()

	except Exception as e:
		frappe.log_error(f"Error in custom file upload: {str(e)}")
		frappe.throw(_("File upload failed: {0}").format(str(e)))
