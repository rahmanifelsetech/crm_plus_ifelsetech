"""
Script to verify CRM Plus custom fields installation
Run: bench --site testcrm.loclahost execute crm_plus_ifelsetech.verify_installation.verify_all
"""

import frappe

def verify_all():
    """Verify all custom fields are installed"""
    print("\n" + "="*60)
    print("CRM Plus Installation Verification")
    print("="*60 + "\n")

    # Check User availability_status field
    check_custom_field("User", "availability_status")

    # Check Event crm_deal field
    check_custom_field("Event", "crm_deal")

    # Check Project crm_deal field
    check_custom_field("Project", "crm_deal")

    # Check File custom fields
    check_custom_field("File", "file_description")
    check_custom_field("File", "file_category")

    # Check frontend components
    print("="*60)
    print("Frontend Components Status")
    print("="*60 + "\n")
    check_frontend_components()

    # Check dummy data
    print("\n" + "="*60)
    print("Dummy Data Status")
    print("="*60 + "\n")
    check_events_data()

    print("\n" + "="*60)
    print("Verification Complete!")
    print("="*60 + "\n")

def check_custom_field(doctype, fieldname):
    """Check if a custom field exists"""
    custom_field = frappe.db.exists("Custom Field", {
        "dt": doctype,
        "fieldname": fieldname
    })

    if custom_field:
        field_doc = frappe.get_doc("Custom Field", custom_field)
        print(f"✅ {doctype}.{fieldname}")
        print(f"   Label: {field_doc.label}")
        print(f"   Type: {field_doc.fieldtype}")
        if field_doc.options:
            print(f"   Options: {field_doc.options}")
        print()
    else:
        print(f"❌ {doctype}.{fieldname} - NOT FOUND")
        print(f"   Please run: bench --site testcrm.loclahost migrate")
        print()

def check_frontend_components():
    """Check if frontend components are copied to CRM"""
    import os

    components = [
        "/home/caratred/frappev15/frappe-bench/apps/crm/frontend/src/components/Activities/EventArea.vue",
        "/home/caratred/frappev15/frappe-bench/apps/crm/frontend/src/components/Activities/ProjectArea.vue",
        "/home/caratred/frappev15/frappe-bench/apps/crm/frontend/src/components/CreateProjectModal.vue"
    ]

    all_found = True
    for component_path in components:
        component_name = os.path.basename(component_path)
        if os.path.exists(component_path):
            stat = os.stat(component_path)
            size = stat.st_size
            print(f"✅ {component_name} - {size} bytes")
        else:
            print(f"❌ {component_name} - NOT FOUND")
            all_found = False

    if all_found:
        print(f"\n⚠️  Build needed: cd /apps/crm && yarn build")
    else:
        print(f"\n❌ Some components missing - check IMPLEMENTATION_STATUS.md")

def check_events_data():
    """Check if dummy events exist"""
    try:
        events = frappe.get_all(
            "Event",
            filters={"crm_deal": ["is", "set"]},
            fields=["name", "subject", "crm_deal"]
        )
        if events:
            print(f"✅ Found {len(events)} events linked to deals:")
            for event in events[:3]:  # Show first 3
                print(f"   - {event.subject} → {event.crm_deal}")
            if len(events) > 3:
                print(f"   ... and {len(events) - 3} more")
        else:
            print(f"⚠️  No events linked to deals yet")
            print(f"   Run: bench --site testcrm.loclahost execute crm_plus_ifelsetech.add_dummy_data.add_dummy_data")
    except Exception as e:
        print(f"❌ Error checking events: {str(e)}")

def show_api_endpoints():
    """Show available API endpoints"""
    print("\n" + "="*60)
    print("Available API Endpoints")
    print("="*60 + "\n")

    endpoints = [
        {
            "name": "Get Events for Deal",
            "endpoint": "crm_plus_ifelsetech.api.events.get_events_for_deal",
            "params": "deal_name"
        },
        {
            "name": "Create Event for Deal",
            "endpoint": "crm_plus_ifelsetech.api.events.create_event_for_deal",
            "params": "deal_name, subject, ..."
        },
        {
            "name": "Get Projects for Deal",
            "endpoint": "crm_plus_ifelsetech.api.project.get_projects_for_deal",
            "params": "deal_name"
        },
        {
            "name": "Create Project from Deal",
            "endpoint": "crm_plus_ifelsetech.api.project.create_project_from_deal",
            "params": "deal_name, project_template, project_name"
        },
        {
            "name": "Get Project Templates",
            "endpoint": "crm_plus_ifelsetech.api.project.get_project_templates",
            "params": "None"
        },
        {
            "name": "Update User Status",
            "endpoint": "crm_plus_ifelsetech.api.user_status.update_user_status",
            "params": "status"
        },
        {
            "name": "Get User Status",
            "endpoint": "crm_plus_ifelsetech.api.user_status.get_user_status",
            "params": "user (optional)"
        },
    ]

    for ep in endpoints:
        print(f"📌 {ep['name']}")
        print(f"   {ep['endpoint']}")
        print(f"   Params: {ep['params']}")
        print()

if __name__ == "__main__":
    verify_all()
    show_api_endpoints()
