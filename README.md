# Custom CRM Extensions

Custom extensions and customizations for Frappe CRM.

## Overview

This app contains custom frontend and backend modifications for the Frappe CRM app, including:

### Backend Customizations

1. **CRM Quotation DocType**
   - New doctype for managing quotations linked to CRM Deals
   - API endpoints for creating and managing quotations

2. **Enhanced File Upload**
   - Custom file upload handler supporting metadata (description, categories)
   - Additional custom fields on File doctype:
     - `file_description`: Text description for files
     - `file_category`: Categorization for better organization

3. **Custom Fields**
   - Fixtures for File doctype custom fields

### Frontend Customizations

1. **Quotation Management**
   - New QuotationArea component for displaying quotations
   - Quotations tab in Deal page
   - View, edit, and delete quotation functionality

2. **Enhanced File Uploader**
   - Description field for uploaded files
   - Category tags with predefined options
   - Multi-select category support

3. **Enhanced Attachments**
   - Search functionality for attachments (by name or description)
   - Category-based filtering
   - Display of file descriptions and categories

## Installation

### Prerequisites

- Frappe CRM app must be installed
- Frappe framework v15+

### Steps

1. **Install the app:**
   ```bash
   cd frappe-bench
   bench get-app /path/to/custom_crm
   bench --site [your-site] install-app custom_crm
   ```

2. **Apply frontend overrides:**
   The frontend overrides are automatically applied during installation. If you need to reapply them manually:
   ```bash
   cd apps/custom_crm
   python3 -m custom_crm.apply_frontend_overrides
   ```

3. **Build assets:**
   ```bash
   bench build --app crm
   ```

4. **Restart bench:**
   ```bash
   bench restart
   ```

## Frontend Overrides

The following CRM frontend files are customized:

- `frontend/src/components/Activities/QuotationArea.vue` (new)
- `frontend/src/components/Activities/Activities.vue`
- `frontend/src/components/Activities/AttachmentArea.vue`
- `frontend/src/pages/Deal.vue`
- `frontend/src/components/FilesUploader/FilesUploaderArea.vue`
- `frontend/src/components/FilesUploader/filesUploaderHandler.ts`

**Note:** Original files are backed up with `.original` extension before being overwritten.

## Directory Structure

```
custom_crm/
├── custom_crm/
│   ├── api/
│   │   └── upload.py                    # Custom file upload handler
│   ├── fcrm/
│   │   └── doctype/
│   │       └── crm_quotation/           # CRM Quotation DocType
│   ├── fixtures/
│   │   └── custom_field.json            # Custom Field fixtures
│   ├── public/
│   │   └── frontend_overrides/
│   │       ├── components/              # Modified frontend components
│   │       └── patches/                 # Git diff patches
│   ├── apply_frontend_overrides.py      # Script to apply frontend changes
│   ├── install.py                       # Installation hooks
│   └── hooks.py                         # App hooks configuration
└── README.md
```

## Reapplying Frontend Overrides

If the CRM app is updated and frontend files are overwritten, reapply the customizations:

```bash
cd /path/to/frappe-bench
python3 -c "from custom_crm.apply_frontend_overrides import apply_frontend_overrides; apply_frontend_overrides()"
bench build --app crm
bench restart
```

## API Endpoints

### File Upload with Metadata
```
POST /api/method/custom_crm.api.upload.upload_file_with_metadata
```
Parameters:
- `file`: The file to upload
- `file_description`: (optional) Description of the file
- `file_category`: (optional) Category tags (comma-separated)

### Get Quotations for Deal
```
GET /api/method/custom_crm.fcrm.doctype.crm_quotation.api.get_quotations_for_deal
```
Parameters:
- `deal_name`: Name of the CRM Deal

## Development

### Modifying Frontend Files

1. Make changes to files in `custom_crm/public/frontend_overrides/components/`
2. Run the apply script:
   ```bash
   python3 -m custom_crm.apply_frontend_overrides
   ```
3. Rebuild:
   ```bash
   bench build --app crm
   ```

### Creating Patches

If you need to update the patches after modifying files in the CRM app:

```bash
cd apps/crm
git diff main...custom_changes -- frontend/src/components/Activities/Activities.vue > ../custom_crm/custom_crm/public/frontend_overrides/patches/activities.patch
# Repeat for other files
```

## Troubleshooting

### Frontend changes not appearing
1. Ensure frontend overrides are applied: `python3 -m custom_crm.apply_frontend_overrides`
2. Clear cache: `bench clear-cache`
3. Rebuild: `bench build --app crm`
4. Hard refresh browser (Ctrl+Shift+R)

### Custom fields not showing
1. Run: `bench --site [site-name] migrate`
2. Clear cache: `bench clear-cache`
3. Reload the doctype in Customize Form

## License

MIT