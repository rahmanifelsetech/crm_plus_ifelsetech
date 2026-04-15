import frappe
from frappe import _
from frappe.utils import today, getdate

@frappe.whitelist()
def get_projects_for_deal(deal_name):
    """Get all projects linked to a specific CRM Deal"""
    if not frappe.has_permission("CRM Deal", "read", deal_name):
        frappe.throw(_("You don't have permission to access this deal"))

    projects = frappe.get_all(
        "Project",
        filters={"crm_deal": deal_name},
        fields=[
            "name",
            "project_name",
            "status",
            "priority",
            "expected_start_date",
            "expected_end_date",
            "percent_complete",
            "customer",
            "modified"
        ],
        order_by="creation desc"
    )

    # Map field names to match frontend expectations
    for project in projects:
        project['start_date'] = project.get('expected_start_date')
        project['end_date'] = project.get('expected_end_date')

    return projects

@frappe.whitelist()
def create_project_from_deal(deal_name, project_template=None, project_name=None):
    """Create a new project from a CRM Deal"""
    if not frappe.has_permission("CRM Deal", "read", deal_name):
        frappe.throw(_("You don't have permission to access this deal"))

    if not frappe.has_permission("Project", "create"):
        frappe.throw(_("You don't have permission to create projects"))

    # Get deal details
    deal = frappe.get_doc("CRM Deal", deal_name)

    # Get company (required for ERPNext projects)
    company = frappe.get_all("Company", fields=["name"], limit=1)
    if not company:
        frappe.throw(_("No company found in ERPNext. Please create a company first."))
    company = company[0].name

    # Create project
    project = frappe.new_doc("Project")

    # Set project name
    if project_name:
        project.project_name = project_name
    else:
        org_name = deal.organization or "Unknown"
        project.project_name = f"{org_name} - {deal.name}"

    # Set company (required)
    project.company = company

    # Link to deal
    project.crm_deal = deal_name

    # Set customer if organization exists
    if deal.organization:
        # Try to find matching Customer
        customer = frappe.db.get_value("Customer", {"customer_name": deal.organization})
        if customer:
            project.customer = customer

    # Set dates
    project.expected_start_date = today()
    if deal.get("close_date"):
        project.expected_end_date = deal.close_date

    # Set other fields
    project.priority = "Medium"
    project.status = "Open"
    project.is_active = "Yes"

    # Set project template if provided (validate it exists first)
    if project_template:
        # Check if template exists before assigning
        if frappe.db.exists("Project Template", project_template):
            project.project_template = project_template
        else:
            frappe.msgprint(_("Project Template '{0}' not found. Project will be created without template.").format(project_template))

    project.insert()

    return project.as_dict()

@frappe.whitelist()
def get_project_templates():
    """Get list of available project templates"""
    templates = frappe.get_all(
        "Project Template",
        fields=["name", "project_type"],
        order_by="name"
    )

    return templates

@frappe.whitelist()
def get_project_template_details(template_name):
    """Get details of a specific project template including tasks"""
    if not template_name:
        return None

    template = frappe.get_doc("Project Template", template_name)

    return {
        "name": template.name,
        "project_type": template.project_type,
        "tasks": [
            {
                "subject": task.subject,
                "start": task.start,
                "duration": task.duration,
                "description": task.description
            }
            for task in template.tasks
        ] if hasattr(template, 'tasks') else []
    }
