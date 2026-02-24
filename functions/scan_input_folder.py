import os


def scan_input_folder_for_new_csv():
	# STUB — replace with real logic when Data Processing Lead is ready
	input_folder = "input"
	csv_files = [f for f in os.listdir(input_folder) if f.endswith(".csv")]
	print(f"Found: {csv_files}")
	return csv_files
