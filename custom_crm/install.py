import frappe
from frappe import _


def after_install():
	"""
	Called after custom_crm app is installed.
	Apply custom field fixtures and frontend overrides.
	"""
	print("\n" + "="*60)
	print("Installing Custom CRM Extensions")
	print("="*60 + "\n")

	# Import custom fields
	try:
		import_custom_fields()
	except Exception as e:
		frappe.log_error(f"Error importing custom fields: {str(e)}")
		print(f"⚠️  Warning: Could not import custom fields: {str(e)}")

	# Apply frontend overrides
	try:
		apply_frontend_overrides()
	except Exception as e:
		frappe.log_error(f"Error applying frontend overrides: {str(e)}")
		print(f"⚠️  Warning: Could not apply frontend overrides: {str(e)}")

	print("\n" + "="*60)
	print("✅ Custom CRM Extensions installed successfully!")
	print("="*60 + "\n")
	print("ℹ️  Note: You need to run 'bench build' to compile frontend changes")
	print("\n")


def import_custom_fields():
	"""Import custom fields from fixtures"""
	from frappe.core.doctype.data_import.data_import import import_file

	fixtures_path = frappe.get_app_path("custom_crm", "fixtures")
	custom_field_file = fixtures_path + "/custom_field.json"

	if frappe.os.path.exists(custom_field_file):
		print("📦 Importing custom fields...")
		with open(custom_field_file, "r") as f:
			import json
			data = json.load(f)

			for field in data:
				if not frappe.db.exists("Custom Field", field.get("name")):
					doc = frappe.get_doc(field)
					doc.insert(ignore_permissions=True)
					print(f"   ✓ Created custom field: {field.get('name')}")
				else:
					print(f"   ℹ️  Custom field already exists: {field.get('name')}")

		frappe.db.commit()
	else:
		print(f"⚠️  Custom field fixture not found at {custom_field_file}")


def apply_frontend_overrides():
	"""Apply frontend file overrides to CRM app"""
	from custom_crm.apply_frontend_overrides import apply_frontend_overrides as apply_overrides

	print("\n🔧 Applying frontend overrides...")
	success = apply_overrides()

	if success:
		print("✅ Frontend overrides applied")
	else:
		print("⚠️  Could not apply frontend overrides")
