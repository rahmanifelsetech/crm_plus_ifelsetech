"""
Create dummy projects for a CRM Deal
Usage: bench --site <site_name> execute crm_plus_ifelsetech.create_dummy_projects.create_dummy_projects --args "['CRM-DEAL-2026-00006']"
"""
import frappe
from frappe.utils import today, add_days

def create_dummy_projects(deal_name):
    """Create dummy projects for the given deal"""

    # Check if the deal exists
    if not frappe.db.exists("CRM Deal", deal_name):
        frappe.throw(f"Deal {deal_name} not found!")

    deal = frappe.get_doc("CRM Deal", deal_name)
    print(f"✓ Deal found: {deal.name}")
    print(f"  Organization: {deal.organization or 'Not set'}")

    # Check for existing projects
    existing_projects = frappe.get_all(
        "CRM Project",
        filters={"crm_deal": deal_name},
        fields=["name", "project_name"]
    )

    if existing_projects:
        print(f"\n⚠ Found {len(existing_projects)} existing projects:")
        for proj in existing_projects:
            print(f"  - {proj.name}: {proj.project_name}")
        print("\nDeleting existing projects...")
        for proj in existing_projects:
            frappe.delete_doc("CRM Project", proj.name, force=1)
        frappe.db.commit()
        print("✓ Existing projects deleted")

    # Dummy projects to create
    dummy_projects = [
        {
            "project_name": "Website Redesign Project",
            "status": "In Progress",
            "priority": "High",
            "start_date": add_days(today(), -30),
            "end_date": add_days(today(), 30),
            "percent_complete": 45,
            "description": "<p>Complete redesign of the company website with modern UI/UX and responsive design.</p>"
        },
        {
            "project_name": "Mobile App Development",
            "status": "Open",
            "priority": "Medium",
            "start_date": today(),
            "end_date": add_days(today(), 90),
            "percent_complete": 10,
            "description": "<p>Develop a cross-platform mobile application for iOS and Android.</p>"
        },
        {
            "project_name": "CRM System Integration",
            "status": "On Hold",
            "priority": "Low",
            "start_date": add_days(today(), -15),
            "end_date": add_days(today(), 45),
            "percent_complete": 25,
            "description": "<p>Integrate the existing CRM system with third-party marketing automation tools.</p>"
        },
        {
            "project_name": "Security Audit & Compliance",
            "status": "Completed",
            "priority": "Urgent",
            "start_date": add_days(today(), -60),
            "end_date": add_days(today(), -10),
            "percent_complete": 100,
            "description": "<p>Comprehensive security audit and compliance assessment for ISO 27001 certification.</p>"
        },
        {
            "project_name": "Data Migration Project",
            "status": "In Progress",
            "priority": "High",
            "start_date": add_days(today(), -20),
            "end_date": add_days(today(), 20),
            "percent_complete": 65,
            "description": "<p>Migrate legacy data from old systems to the new cloud-based infrastructure.</p>"
        }
    ]

    print(f"\n📋 Creating {len(dummy_projects)} dummy projects...")
    created_projects = []

    for proj_data in dummy_projects:
        try:
            project = frappe.new_doc("CRM Project")
            project.project_name = proj_data["project_name"]
            project.crm_deal = deal_name
            project.customer = deal.organization
            project.status = proj_data["status"]
            project.priority = proj_data["priority"]
            project.start_date = proj_data["start_date"]
            project.end_date = proj_data["end_date"]
            project.percent_complete = proj_data["percent_complete"]
            project.description = proj_data["description"]

            project.insert(ignore_permissions=True)
            created_projects.append(project)
            print(f"✓ Created: {project.name} - {project.project_name}")
        except Exception as e:
            print(f"✗ Error creating project '{proj_data['project_name']}': {str(e)}")
            frappe.db.rollback()
            raise

    # Commit the changes
    frappe.db.commit()
    print(f"\n✅ Successfully created {len(created_projects)} projects for {deal_name}")

    # Display summary
    print("\n" + "="*60)
    print("PROJECT SUMMARY")
    print("="*60)
    for project in created_projects:
        print(f"\n📦 {project.name}")
        print(f"   Name: {project.project_name}")
        print(f"   Status: {project.status}")
        print(f"   Priority: {project.priority}")
        print(f"   Progress: {project.percent_complete}%")
        print(f"   Duration: {project.start_date} to {project.end_date}")

    return {
        "success": True,
        "created": len(created_projects),
        "projects": [{"name": p.name, "project_name": p.project_name} for p in created_projects]
    }
