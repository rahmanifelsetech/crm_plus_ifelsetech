#!/usr/bin/env python3
"""
Script to apply custom CRM frontend overrides.
This script copies the customized frontend files to the CRM app.
"""

import os
import shutil
from pathlib import Path


def apply_frontend_overrides():
	"""Copy custom frontend files to CRM app"""

	# Get paths
	custom_crm_path = Path(__file__).parent
	bench_path = custom_crm_path.parent.parent.parent
	crm_frontend_path = bench_path / "apps" / "crm" / "frontend" / "src"
	overrides_path = custom_crm_path / "public" / "frontend_overrides" / "components"

	if not crm_frontend_path.exists():
		print(f"❌ CRM frontend path not found: {crm_frontend_path}")
		return False

	if not overrides_path.exists():
		print(f"❌ Overrides path not found: {overrides_path}")
		return False

	# File mappings: source -> destination
	file_mappings = {
		"QuotationArea.vue": "components/Activities/QuotationArea.vue",
		"Activities.vue": "components/Activities/Activities.vue",
		"AttachmentArea.vue": "components/Activities/AttachmentArea.vue",
		"Deal.vue": "pages/Deal.vue",
		"FilesUploader.vue": "components/FilesUploader/FilesUploader.vue",
		"FilesUploaderArea.vue": "components/FilesUploader/FilesUploaderArea.vue",
		"filesUploaderHandler.ts": "components/FilesUploader/filesUploaderHandler.ts",
	}

	print("\n🔧 Applying custom CRM frontend overrides...\n")

	for source_file, dest_path in file_mappings.items():
		source = overrides_path / source_file
		destination = crm_frontend_path / dest_path

		if not source.exists():
			print(f"⚠️  Source file not found: {source_file}")
			continue

		# Create destination directory if it doesn't exist
		destination.parent.mkdir(parents=True, exist_ok=True)

		# Backup original file if it exists
		if destination.exists():
			backup = destination.with_suffix(destination.suffix + ".original")
			if not backup.exists():
				shutil.copy2(destination, backup)
				print(f"📦 Backed up: {dest_path}")

		# Copy the custom file
		shutil.copy2(source, destination)
		print(f"✅ Copied: {dest_path}")

	print("\n✨ Frontend overrides applied successfully!\n")
	return True


if __name__ == "__main__":
	apply_frontend_overrides()
