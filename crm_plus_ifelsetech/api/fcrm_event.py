import frappe
from frappe import _


@frappe.whitelist()
def get_events(reference_doctype, reference_docname):
	"""
	Get all FCRM Events linked to a specific document

	Args:
		reference_doctype: The doctype of the reference document (e.g., 'CRM Deal')
		reference_docname: The name of the reference document

	Returns:
		List of FCRM Events
	"""
	events = frappe.get_all(
		"FCRM Event",
		filters={
			"reference_doctype": reference_doctype,
			"reference_docname": reference_docname
		},
		fields=[
			"name",
			"subject",
			"event_category",
			"event_type",
			"status",
			"color",
			"starts_on",
			"ends_on",
			"all_day",
			"description",
			"modified",
			"creation"
		],
		order_by="starts_on desc"
	)

	return events


@frappe.whitelist()
def create_event(subject, starts_on, reference_doctype=None, reference_docname=None, **kwargs):
	"""
	Create a new FCRM Event

	Args:
		subject: Subject of the event
		starts_on: Start datetime
		reference_doctype: Optional reference doctype
		reference_docname: Optional reference docname
		**kwargs: Additional fields

	Returns:
		Created event document
	"""
	doc = frappe.get_doc({
		"doctype": "FCRM Event",
		"subject": subject,
		"starts_on": starts_on,
		"reference_doctype": reference_doctype or "CRM Deal",
		"reference_docname": reference_docname,
		**kwargs
	})
	doc.insert()
	frappe.db.commit()

	return doc


@frappe.whitelist()
def update_event(name, **kwargs):
	"""
	Update an existing FCRM Event

	Args:
		name: Name of the event to update
		**kwargs: Fields to update

	Returns:
		Updated event document
	"""
	doc = frappe.get_doc("FCRM Event", name)

	for key, value in kwargs.items():
		if hasattr(doc, key):
			setattr(doc, key, value)

	doc.save()
	frappe.db.commit()

	return doc


@frappe.whitelist()
def delete_event(name):
	"""
	Delete an FCRM Event

	Args:
		name: Name of the event to delete

	Returns:
		Success message
	"""
	frappe.delete_doc("FCRM Event", name)
	frappe.db.commit()

	return {"message": _("Event deleted successfully")}
