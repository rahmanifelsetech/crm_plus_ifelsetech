# custom_crm Setup and Maintenance Guide

## Overview

The `custom_crm` app contains all customizations for the Frappe CRM app. All custom code is isolated in this app, ensuring the base CRM app remains clean and updatable.

## Architecture

### How Customizations Work

1. **Source of Truth**: All custom code is in the `custom_crm` app
   - Backend: `custom_crm/api/` and `custom_crm/fcrm/doctype/`
   - Frontend: `custom_crm/public/frontend_overrides/components/`

2. **Frontend Overrides**: Custom Vue components are automatically copied to the CRM app during installation
   - Script: `custom_crm/apply_frontend_overrides.py`
   - Destination: `apps/crm/frontend/src/`

3. **Backend Overrides**: Custom API endpoints override CRM endpoints
   - `custom_crm.api.activities.get_activities` replaces `crm.api.activities.get_activities`
   - `custom_crm.api.upload.upload_file_with_metadata` extends file upload functionality

## Installation

```bash
# Install the app on your site
bench --site [site-name] install-app custom_crm

# Build CRM frontend
bench build --app crm

# Clear cache
bench clear-cache
```

The post-install hook automatically:
1. Imports custom field fixtures
2. Applies frontend overrides
3. Creates necessary doctypes

## Git Management

### CRM App (apps/crm)

The CRM app will have modified files after custom_crm installation, but these are managed to not show in git:

**Modified files** (functional, but hidden from git):
- `frontend/src/components/Activities/Activities.vue`
- `frontend/src/components/Activities/AttachmentArea.vue`
- `frontend/src/components/FilesUploader/FilesUploader.vue`
- `frontend/src/components/FilesUploader/FilesUploaderArea.vue`
- `frontend/src/components/FilesUploader/filesUploaderHandler.ts`
- `frontend/src/pages/Deal.vue`

**How they're hidden**:
```bash
git update-index --assume-unchanged [file-path]
```

**Ignored files** (via .gitignore):
- `*.original` - Backup files created by apply script
- `package-lock.json` - NPM lock file

### custom_crm App (apps/custom_crm)

All customizations should be committed to this app:
- Backend API files
- Frontend override files
- Custom doctypes
- Fixtures

## Updating Customizations

### Modifying Frontend Components

1. Edit files in `custom_crm/public/frontend_overrides/components/`
2. Apply changes:
   ```bash
   python3 /path/to/custom_crm/custom_crm/apply_frontend_overrides.py
   bench build --app crm
   ```
3. Commit changes to custom_crm app

### Modifying Backend APIs

1. Edit files in `custom_crm/api/` or `custom_crm/fcrm/`
2. Clear cache:
   ```bash
   bench clear-cache
   ```
3. Commit changes to custom_crm app

## Features Implemented

### 1. Enhanced File Upload
- Add descriptions to files
- Categorize files with tags
- Predefined categories: General, Contract, Invoice, Proposal, Presentation, Report, Image, Video, Audio, Document, Spreadsheet, Other

### 2. Smart Attachments View
- Search by name or description
- Multi-select category filter
- Display descriptions and category tags
- Visual organization

### 3. Quotation Management
- Create and manage quotations for deals
- Link quotations to CRM Deals
- Display quotations in dedicated tab
- Status tracking

## API Endpoints

### File Upload
```
POST /api/method/custom_crm.api.upload.upload_file_with_metadata
Parameters: file, file_description, file_category
```

### Get Activities (with custom fields)
```
GET /api/method/custom_crm.api.activities.get_activities
Parameters: name (deal/lead name)
```

### Quotation APIs
```
GET /api/method/custom_crm.fcrm.doctype.crm_quotation.api.get_quotations_for_deal
POST /api/method/custom_crm.fcrm.doctype.crm_quotation.api.create_quotation_from_deal
```

## Troubleshooting

### Frontend changes not showing
1. Reapply overrides:
   ```bash
   python3 custom_crm/apply_frontend_overrides.py
   bench build --app crm
   ```
2. Hard refresh browser (Ctrl+Shift+R)

### Backend changes not working
```bash
bench clear-cache
```

### After CRM app update
When the CRM app is updated, reapply customizations:
```bash
python3 custom_crm/apply_frontend_overrides.py
bench build --app crm
bench clear-cache
```

## File Structure

```
custom_crm/
├── api/
│   ├── activities.py          # Custom activities API
│   └── upload.py              # File upload with metadata
├── fcrm/
│   └── doctype/
│       └── crm_quotation/     # Quotation doctype
├── fixtures/
│   └── custom_field.json      # Custom fields for File doctype
├── public/
│   └── frontend_overrides/
│       └── components/        # Custom Vue components
├── apply_frontend_overrides.py
├── install.py
└── hooks.py
```

## Notes

- Original CRM files are backed up with `.original` extension
- All customizations are version-controlled in custom_crm app
- Frontend overrides can be reapplied without data loss
- The CRM app remains clean for updates
