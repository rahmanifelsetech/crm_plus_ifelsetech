"""
Create dummy ERPNext projects for a CRM Deal
Usage: bench --site <site_name> execute crm_plus_ifelsetech.create_erpnext_projects.create_erpnext_projects --args "['CRM-DEAL-2026-00006']"
"""
import frappe
from frappe.utils import today, add_days

def create_erpnext_projects(deal_name):
    """Create dummy ERPNext projects for the given deal"""

    # Check if the deal exists
    if not frappe.db.exists("CRM Deal", deal_name):
        frappe.throw(f"Deal {deal_name} not found!")

    deal = frappe.get_doc("CRM Deal", deal_name)
    print(f"✓ Deal found: {deal.name}")
    print(f"  Organization: {deal.organization or 'Not set'}")

    # Delete existing CRM Projects
    existing_crm_projects = frappe.get_all(
        "CRM Project",
        filters={"crm_deal": deal_name},
        fields=["name", "project_name"]
    )

    if existing_crm_projects:
        print(f"\n⚠ Found {len(existing_crm_projects)} existing CRM Projects:")
        for proj in existing_crm_projects:
            print(f"  - {proj.name}: {proj.project_name}")
        print("\nDeleting existing CRM Projects...")
        for proj in existing_crm_projects:
            frappe.delete_doc("CRM Project", proj.name, force=1)
        frappe.db.commit()
        print("✓ Existing CRM Projects deleted")

    # Check for existing ERPNext Projects
    existing_projects = frappe.get_all(
        "Project",
        filters={"crm_deal": deal_name},
        fields=["name", "project_name"]
    )

    if existing_projects:
        print(f"\n⚠ Found {len(existing_projects)} existing ERPNext Projects:")
        for proj in existing_projects:
            print(f"  - {proj.name}: {proj.project_name}")
        print("\nDeleting existing ERPNext Projects...")
        for proj in existing_projects:
            frappe.delete_doc("Project", proj.name, force=1)
        frappe.db.commit()
        print("✓ Existing ERPNext Projects deleted")

    # Get company (required for ERPNext projects)
    company = frappe.get_all("Company", fields=["name"], limit=1)
    if not company:
        frappe.throw("No company found in ERPNext. Please create a company first.")
    company = company[0].name
    print(f"✓ Using company: {company}")

    # Get or create customer
    customer = None
    if deal.organization:
        customer = frappe.db.get_value("Customer", {"customer_name": deal.organization})
        if not customer:
            print(f"\n⚠ Customer '{deal.organization}' not found, creating...")
            try:
                # Get first customer group and territory
                customer_group = frappe.get_all("Customer Group", fields=["name"], limit=1)
                territory = frappe.get_all("Territory", fields=["name"], limit=1)

                if customer_group and territory:
                    customer_doc = frappe.new_doc("Customer")
                    customer_doc.customer_name = deal.organization
                    customer_doc.customer_type = "Company"
                    customer_doc.customer_group = customer_group[0].name
                    customer_doc.territory = territory[0].name
                    customer_doc.insert(ignore_permissions=True)
                    customer = customer_doc.name
                    print(f"✓ Customer created: {customer}")
                else:
                    print(f"✗ Could not create customer: Customer Group or Territory not found")
            except Exception as e:
                print(f"✗ Could not create customer: {str(e)}")

    # Dummy projects to create
    dummy_projects = [
        {
            "project_name": "Website Redesign Project",
            "status": "Open",
            "priority": "High",
            "expected_start_date": add_days(today(), -30),
            "expected_end_date": add_days(today(), 30),
            "percent_complete_method": "Manual",
            "notes": "<p>Complete redesign of the company website with modern UI/UX and responsive design.</p>"
        },
        {
            "project_name": "Mobile App Development",
            "status": "Open",
            "priority": "Medium",
            "expected_start_date": today(),
            "expected_end_date": add_days(today(), 90),
            "percent_complete_method": "Manual",
            "notes": "<p>Develop a cross-platform mobile application for iOS and Android.</p>"
        },
        {
            "project_name": "CRM System Integration",
            "status": "Open",
            "priority": "Low",
            "expected_start_date": add_days(today(), -15),
            "expected_end_date": add_days(today(), 45),
            "percent_complete_method": "Manual",
            "notes": "<p>Integrate the existing CRM system with third-party marketing automation tools.</p>"
        },
        {
            "project_name": "Security Audit & Compliance",
            "status": "Completed",
            "priority": "High",
            "expected_start_date": add_days(today(), -60),
            "expected_end_date": add_days(today(), -10),
            "percent_complete_method": "Manual",
            "notes": "<p>Comprehensive security audit and compliance assessment for ISO 27001 certification.</p>"
        },
        {
            "project_name": "Data Migration Project",
            "status": "Open",
            "priority": "High",
            "expected_start_date": add_days(today(), -20),
            "expected_end_date": add_days(today(), 20),
            "percent_complete_method": "Manual",
            "notes": "<p>Migrate legacy data from old systems to the new cloud-based infrastructure.</p>"
        }
    ]

    print(f"\n📋 Creating {len(dummy_projects)} dummy ERPNext projects...")
    created_projects = []

    for proj_data in dummy_projects:
        try:
            project = frappe.new_doc("Project")
            project.project_name = proj_data["project_name"]
            project.company = company
            project.crm_deal = deal_name
            if customer:
                project.customer = customer
            project.status = proj_data["status"]
            project.priority = proj_data["priority"]
            project.is_active = "Yes"
            project.expected_start_date = proj_data["expected_start_date"]
            project.expected_end_date = proj_data["expected_end_date"]
            project.percent_complete_method = proj_data["percent_complete_method"]
            project.notes = proj_data["notes"]

            project.insert(ignore_permissions=True)
            created_projects.append(project)
            print(f"✓ Created: {project.name} - {project.project_name}")
        except Exception as e:
            print(f"✗ Error creating project '{proj_data['project_name']}': {str(e)}")
            frappe.db.rollback()
            raise

    # Commit the changes
    frappe.db.commit()
    print(f"\n✅ Successfully created {len(created_projects)} ERPNext projects for {deal_name}")

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
        print(f"   Duration: {project.expected_start_date} to {project.expected_end_date}")

    return {
        "success": True,
        "created": len(created_projects),
        "projects": [{"name": p.name, "project_name": p.project_name} for p in created_projects]
    }
