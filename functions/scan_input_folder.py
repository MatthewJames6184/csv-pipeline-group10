import os


def scan_input_folder_for_new_csv(input_folder="input"):
	if not os.path.isdir(input_folder):
		return []
	csv_files = [f for f in os.listdir(input_folder) if f.endswith(".csv")]
	print(f"Found: {csv_files}")
	return csv_files
