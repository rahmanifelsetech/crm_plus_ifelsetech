#!/usr/bin/env python3
"""
Create custom field in Project DocType to link to CRM Deal
"""

import frappe

def create_project_custom_field():
    """Add CRM Deal custom field to Project DocType"""

    # Check if custom field already exists
    if frappe.db.exists("Custom Field", {"dt": "Project", "fieldname": "crm_deal"}):
        print("✅ Custom field 'crm_deal' already exists in Project DocType")
        return

    try:
        custom_field = frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "Project",
            "label": "CRM Deal",
            "fieldname": "crm_deal",
            "fieldtype": "Link",
            "options": "CRM Deal",
            "insert_after": "customer",
            "allow_on_submit": 0,
            "bold": 0,
            "collapsible": 0,
            "default": None,
            "depends_on": None,
            "description": "Link this project to a CRM Deal",
            "fetch_from": None,
            "fetch_if_empty": 0,
            "hidden": 0,
            "hide_border": 0,
            "hide_days": 0,
            "hide_seconds": 0,
            "ignore_user_permissions": 0,
            "ignore_xss_filter": 0,
            "in_global_search": 0,
            "in_list_view": 0,
            "in_preview": 0,
            "in_standard_filter": 1,
            "is_system_generated": 0,
            "is_virtual": 0,
            "mandatory_depends_on": None,
            "no_copy": 0,
            "non_negative": 0,
            "permlevel": 0,
            "precision": "",
            "print_hide": 0,
            "print_hide_if_no_value": 0,
            "read_only": 0,
            "read_only_depends_on": None,
            "report_hide": 0,
            "reqd": 0,
            "search_index": 0,
            "translatable": 0,
            "unique": 0
        })

        custom_field.insert()
        frappe.db.commit()
        print("✅ Custom field 'crm_deal' created successfully in Project DocType!")

    except Exception as e:
        print(f"❌ Error creating custom field: {e}")
        frappe.db.rollback()

if __name__ == "__main__":
    create_project_custom_field()
