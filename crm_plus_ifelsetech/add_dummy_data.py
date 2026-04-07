"""
Script to add dummy data for testing CRM Plus extensions
Run: bench --site testcrm.loclahost execute crm_plus_ifelsetech.add_dummy_data.add_test_data
"""

import frappe
from frappe.utils import now_datetime, add_days, today, nowtime

def add_test_data():
    """Add dummy events and projects for testing"""

    # Get first CRM Deal
    deals = frappe.get_all("CRM Deal", limit=5, order_by="creation desc")

    if not deals:
        print("No CRM Deals found. Please create a deal first.")
        return

    for deal in deals[:3]:  # Add data to first 3 deals
        deal_name = deal.name
        print(f"\nAdding data to Deal: {deal_name}")

        # Create Events
        create_dummy_events(deal_name)

        # Skip Projects if ERPNext is not installed
        if frappe.db.exists("DocType", "Project"):
            create_dummy_projects(deal_name)
        else:
            print("  ⚠ Skipping Projects (ERPNext not installed)")

    frappe.db.commit()
    print("\n✅ Dummy data added successfully!")

def create_dummy_events(deal_name):
    """Create dummy events for a deal"""
    events_data = [
        {
            "subject": "Initial Meeting",
            "event_category": "Meeting",
            "event_type": "Public",
            "starts_on": f"{today()} 10:00:00",
            "ends_on": f"{today()} 11:00:00",
            "description": "First meeting with the client to discuss requirements",
            "status": "Open",
        },
        {
            "subject": "Follow-up Call",
            "event_category": "Call",
            "event_type": "Public",
            "starts_on": f"{add_days(today(), 2)} 14:00:00",
            "ends_on": f"{add_days(today(), 2)} 14:30:00",
            "description": "Follow-up call to discuss proposal",
            "status": "Open",
        },
        {
            "subject": "Demo Session",
            "event_category": "Event",
            "event_type": "Public",
            "starts_on": f"{add_days(today(), 5)} 15:00:00",
            "ends_on": f"{add_days(today(), 5)} 16:30:00",
            "description": "Product demonstration for the client team",
            "status": "Open",
        },
    ]

    for event_data in events_data:
        # Check if event already exists
        existing = frappe.db.exists("Event", {
            "subject": event_data["subject"],
            "crm_deal": deal_name
        })

        if not existing:
            event = frappe.new_doc("Event")
            event.update(event_data)
            event.crm_deal = deal_name
            event.insert(ignore_permissions=True)
            print(f"  ✓ Created Event: {event_data['subject']}")
        else:
            print(f"  - Event already exists: {event_data['subject']}")

def create_dummy_projects(deal_name):
    """Create dummy projects for a deal"""

    # Get deal details
    deal = frappe.get_doc("CRM Deal", deal_name)
    org_name = deal.organization or "Client"

    projects_data = [
        {
            "project_name": f"{org_name} - Website Redesign",
            "status": "Open",
            "priority": "High",
            "expected_start_date": today(),
            "expected_end_date": add_days(today(), 30),
            "percent_complete": 15,
        },
        {
            "project_name": f"{org_name} - CRM Implementation",
            "status": "Open",
            "priority": "Medium",
            "expected_start_date": add_days(today(), 7),
            "expected_end_date": add_days(today(), 60),
            "percent_complete": 5,
        },
    ]

    for project_data in projects_data:
        # Check if project already exists
        existing = frappe.db.exists("Project", {
            "project_name": project_data["project_name"],
            "crm_deal": deal_name
        })

        if not existing:
            project = frappe.new_doc("Project")
            project.update(project_data)
            project.crm_deal = deal_name

            # Set customer if organization exists
            if deal.organization:
                project.customer = deal.organization

            project.insert(ignore_permissions=True)
            print(f"  ✓ Created Project: {project_data['project_name']}")
        else:
            print(f"  - Project already exists: {project_data['project_name']}")

def update_user_status():
    """Update availability status for current user"""
    user = frappe.session.user
    if user != "Guest":
        frappe.db.set_value("User", user, "availability_status", "Available")
        frappe.db.commit()
        print(f"✅ Updated user {user} status to Available")

if __name__ == "__main__":
    add_test_data()
    update_user_status()
