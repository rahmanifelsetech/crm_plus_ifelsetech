"""
Setup basic ERPNext records (Company, Customer Group, Territory)
Usage: bench --site <site_name> execute crm_plus_ifelsetech.setup_erpnext_basics.setup_erpnext_basics
"""
import frappe

def setup_erpnext_basics():
    """Setup basic ERPNext records if they don't exist"""

    print("🔧 Setting up basic ERPNext records...")

    # Create Company if none exists
    companies = frappe.get_all("Company", fields=["name"])
    if not companies:
        print("\n📋 Creating default Company...")
        try:
            company = frappe.new_doc("Company")
            company.company_name = "Test Company"
            company.abbr = "TC"
            company.default_currency = "USD"
            company.country = "United States"
            company.insert(ignore_permissions=True)
            print(f"✓ Company created: {company.name}")
        except Exception as e:
            print(f"✗ Error creating company: {str(e)}")
            frappe.db.rollback()
            return
    else:
        print(f"✓ Company exists: {companies[0].name}")

    # Create Customer Group if none exists
    customer_groups = frappe.get_all("Customer Group", fields=["name"])
    if not customer_groups:
        print("\n📋 Creating default Customer Group...")
        try:
            cg = frappe.new_doc("Customer Group")
            cg.customer_group_name = "All Customer Groups"
            cg.is_group = 1
            cg.parent_customer_group = ""
            cg.insert(ignore_permissions=True)
            print(f"✓ Customer Group created: {cg.name}")

            # Create a child group
            cg2 = frappe.new_doc("Customer Group")
            cg2.customer_group_name = "Commercial"
            cg2.parent_customer_group = "All Customer Groups"
            cg2.insert(ignore_permissions=True)
            print(f"✓ Customer Group created: {cg2.name}")
        except Exception as e:
            print(f"✗ Error creating customer group: {str(e)}")
    else:
        print(f"✓ Customer Group exists: {customer_groups[0].name}")

    # Create Territory if none exists
    territories = frappe.get_all("Territory", fields=["name"])
    if not territories:
        print("\n📋 Creating default Territory...")
        try:
            territory = frappe.new_doc("Territory")
            territory.territory_name = "All Territories"
            territory.is_group = 1
            territory.parent_territory = ""
            territory.insert(ignore_permissions=True)
            print(f"✓ Territory created: {territory.name}")
        except Exception as e:
            print(f"✗ Error creating territory: {str(e)}")
    else:
        print(f"✓ Territory exists: {territories[0].name}")

    frappe.db.commit()
    print("\n✅ ERPNext basic setup complete!")

    return {"success": True}
