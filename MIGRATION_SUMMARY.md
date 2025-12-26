# Migration Summary: CRM Custom Changes to custom_crm App

**Date:** December 26, 2025
**Source Branch:** `custom_changes` (CRM app)
**Destination App:** `custom_crm`

## Overview

All custom frontend and backend changes from the CRM app's `custom_changes` branch have been successfully migrated to the standalone `custom_crm` app. This allows for better separation of concerns and easier maintenance of customizations.

## Files Migrated

### Backend Files

1. **CRM Quotation DocType**
   - Location: `custom_crm/fcrm/doctype/crm_quotation/`
   - Files:
     - `crm_quotation.json` - DocType definition
     - `crm_quotation.py` - Python controller
     - `api.py` - API endpoints for quotation management
     - `__init__.py`

2. **Custom Upload API**
   - Location: `custom_crm/api/upload.py`
   - Purpose: Handle file uploads with custom metadata (description, category)

3. **Custom Activities API**
   - Location: `custom_crm/api/activities.py`
   - Purpose: Override CRM activities API to include custom fields in attachments
   - Modification: Adds `file_description` and `file_category` to File query

4. **Custom Field Fixtures**
   - Location: `custom_crm/fixtures/custom_field.json`
   - Custom fields added to File doctype:
     - `file_description` (Text)
     - `file_category` (Small Text)

### Frontend Files

All frontend customizations are stored in `custom_crm/public/frontend_overrides/`

1. **Components Directory** (`components/`)
   - `QuotationArea.vue` - NEW component for displaying quotations
   - `Activities.vue` - Modified to support quotations tab and use custom_crm.api.activities
   - `AttachmentArea.vue` - Added search and multi-select category filtering
   - `Deal.vue` - Added quotations tab
   - `FilesUploader.vue` - Modified to pass description and category to upload handler
   - `FilesUploaderArea.vue` - Enhanced with description and category fields
   - `filesUploaderHandler.ts` - Modified to support custom upload endpoint (custom_crm.api.upload)

2. **Patches Directory** (`patches/`)
   - Git diff patches for each modified file
   - Can be used for reference or manual patching

## Infrastructure Files Created

1. **apply_frontend_overrides.py**
   - Automated script to copy frontend customizations to CRM app
   - Creates backups of original files (`.original` extension)
   - Used during installation and can be run manually

2. **install.py**
   - Post-installation hook
   - Imports custom field fixtures
   - Applies frontend overrides automatically

3. **hooks.py** (updated)
   - Added `required_apps = ["crm"]`
   - Added fixtures configuration
   - Added `after_install` hook

4. **README.md**
   - Comprehensive documentation
   - Installation instructions
   - Usage guidelines
   - Troubleshooting tips

## Custom Features Implemented

### 1. Quotation Management
- Create and manage quotations linked to CRM Deals
- Display quotations in a dedicated tab on Deal page
- View, edit, and delete functionality
- Status badges (Draft, Sent, Accepted, Rejected, etc.)
- Display transaction dates, validity period, and amounts

### 2. Enhanced File Upload
- Add descriptions to uploaded files
- Categorize files with tags
- Predefined categories: General, Contract, Invoice, Proposal, Presentation, Report, Image, Video, Audio, Document, Spreadsheet, Other
- Multi-select category support
- Custom categories via text input

### 3. Enhanced Attachments View
- Search attachments by name or description
- Filter by category
- Display file descriptions inline
- Show category tags
- Improved visual organization

## API Endpoints Added

1. **File Upload with Metadata**
   ```
   POST /api/method/custom_crm.api.upload.upload_file_with_metadata
   ```
   Parameters: file, file_description, file_category

2. **Get Quotations for Deal**
   ```
   GET /api/method/custom_crm.fcrm.doctype.crm_quotation.api.get_quotations_for_deal
   ```
   Parameters: deal_name

3. **Create Quotation from Deal**
   ```
   POST /api/method/custom_crm.fcrm.doctype.crm_quotation.api.create_quotation_from_deal
   ```
   Parameters: deal_name

## Installation Process

The custom_crm app can be installed using:

```bash
bench --site [site-name] install-app custom_crm
```

This will:
1. Import custom field fixtures
2. Apply frontend overrides to CRM app
3. Create necessary doctypes
4. Set up API endpoints

After installation:
```bash
bench build --app crm
bench restart
```

## Maintenance

### Reapplying Frontend Overrides

If CRM app is updated:
```bash
python3 -c "from custom_crm.apply_frontend_overrides import apply_frontend_overrides; apply_frontend_overrides()"
bench build --app crm
```

### Updating Customizations

1. Modify files in `custom_crm/public/frontend_overrides/components/`
2. Run apply script
3. Rebuild CRM app

## Testing Checklist

After installation, verify:

- [ ] CRM Quotation doctype is available
- [ ] Quotations tab appears on Deal page
- [ ] File upload includes description and category fields
- [ ] Attachments can be filtered by category
- [ ] Search works for attachments
- [ ] Custom fields visible on File doctype
- [ ] API endpoints respond correctly

## Notes

- Original CRM files are backed up with `.original` extension
- Custom changes are isolated in the `custom_crm` app
- Frontend overrides can be reapplied without data loss
- All customizations are version-controlled in the custom_crm app

## Next Steps

1. Install the app on your site
2. Run migrations
3. Build assets
4. Test all features
5. Update fixtures if needed (using `bench export-fixtures`)

## Rollback Procedure

If needed, frontend changes can be rolled back:

```bash
cd apps/crm/frontend/src
find . -name "*.original" -exec bash -c 'mv "$1" "${1%.original}"' _ {} \;
bench build --app crm
```

## Support

For issues or questions:
- Check README.md for troubleshooting
- Review MIGRATION_SUMMARY.md for details
- Check apply_frontend_overrides.py for file mappings
