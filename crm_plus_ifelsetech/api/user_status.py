import frappe
from frappe import _

@frappe.whitelist()
def update_user_status(status):
    """Update the availability status for the current user"""
    if status not in ["Available", "Busy", "Free", "Do Not Disturb"]:
        frappe.throw(_("Invalid status value"))

    user = frappe.session.user

    # Update using User document to ensure proper save
    user_doc = frappe.get_doc("User", user)
    user_doc.availability_status = status
    user_doc.save(ignore_permissions=True)
    frappe.db.commit()

    # Verify the update
    updated_status = frappe.db.get_value("User", user, "availability_status")

    return {
        "status": updated_status,
        "message": _("Status updated successfully"),
        "user": user,
        "verified": updated_status == status
    }

@frappe.whitelist()
def get_user_status(user=None):
    """Get the availability status for a specific user or current user"""
    if not user:
        user = frappe.session.user

    status = frappe.db.get_value("User", user, "availability_status")

    if not status:
        status = "Available"

    return {"user": user, "status": status}

@frappe.whitelist()
def get_all_users_status():
    """Get availability status for all active users"""
    users = frappe.get_all(
        "User",
        filters={"enabled": 1, "user_type": "System User"},
        fields=["name", "full_name", "user_image", "availability_status"]
    )

    for user in users:
        if not user.get("availability_status"):
            user["availability_status"] = "Available"

    return users
