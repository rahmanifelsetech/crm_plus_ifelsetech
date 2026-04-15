import frappe
from frappe import _

@frappe.whitelist()
def get_events_for_deal(deal_name):
    """Get all events linked to a specific CRM Deal"""
    if not frappe.has_permission("CRM Deal", "read", deal_name):
        frappe.throw(_("You don't have permission to access this deal"))

    events = frappe.get_all(
        "Event",
        filters={"crm_deal": deal_name},
        fields=[
            "name",
            "subject",
            "event_category",
            "event_type",
            "starts_on",
            "ends_on",
            "status",
            "description",
            "color",
            "all_day",
            "modified"
        ],
        order_by="starts_on desc"
    )

    return events

@frappe.whitelist()
def create_event_for_deal(deal_name, subject, event_category="Event", event_type="Public", starts_on=None, ends_on=None, description=None, all_day=0):
    """Create a new event linked to a CRM Deal"""
    if not frappe.has_permission("CRM Deal", "read", deal_name):
        frappe.throw(_("You don't have permission to access this deal"))

    if not frappe.has_permission("Event", "create"):
        frappe.throw(_("You don't have permission to create events"))

    event = frappe.new_doc("Event")
    event.subject = subject
    event.event_category = event_category
    event.event_type = event_type
    event.starts_on = starts_on
    event.ends_on = ends_on
    event.description = description
    event.all_day = all_day
    event.crm_deal = deal_name

    event.insert()

    return event.as_dict()

@frappe.whitelist()
def get_event_categories():
    """Get available event categories"""
    return ["Event", "Meeting", "Call", "Sent/Received Email", "Other"]
