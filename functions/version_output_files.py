from typing import List
import os
import shutil
from datetime import datetime


def version_output_files(csv_files: List[str]) -> None:
	output_folder = "output"
	versions_folder = "versions"
	
	# Create versions directory if it doesn't exist
	os.makedirs(versions_folder, exist_ok=True)
	
	# Generate timestamp for this version
	timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
	
	for csv_file in csv_files:
		processed_file = f"processed_{csv_file}"
		source_path = os.path.join(output_folder, processed_file)
		
		if os.path.exists(source_path):
			# Create versioned filename with timestamp
			base_name = csv_file.replace('.csv', '')
			versioned_file = f"{base_name}_{timestamp}.csv"
			version_path = os.path.join(versions_folder, versioned_file)
			
			# Copy to versions folder
			shutil.copy2(source_path, version_path)
			print(f"Versioned: {processed_file} → {versioned_file}")
		else:
			print(f"Warning: {processed_file} not found for versioning")
	
	return None
