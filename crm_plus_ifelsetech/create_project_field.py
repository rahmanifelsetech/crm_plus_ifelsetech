"""
Script to create the Project custom field
Run: bench --site testcrm.loclahost execute crm_plus_ifelsetech.create_project_field.create_field
"""

import frappe

def create_field():
    """Create Project crm_deal custom field"""

    # Check if field already exists
    existing = frappe.db.exists("Custom Field", {
        "dt": "Project",
        "fieldname": "crm_deal"
    })

    if existing:
        print("✅ Project.crm_deal custom field already exists")
        return

    # Create the custom field
    custom_field = frappe.new_doc("Custom Field")
    custom_field.dt = "Project"
    custom_field.fieldname = "crm_deal"
    custom_field.fieldtype = "Link"
    custom_field.label = "CRM Deal"
    custom_field.options = "CRM Deal"
    custom_field.insert_after = "customer"
    custom_field.translatable = 0
    custom_field.allow_on_submit = 0
    custom_field.read_only = 0
    custom_field.hidden = 0
    custom_field.description = "Link this project to a CRM Deal"

    custom_field.insert(ignore_permissions=True)
    frappe.db.commit()

    print("✅ Created Project.crm_deal custom field successfully!")

if __name__ == "__main__":
    create_field()
