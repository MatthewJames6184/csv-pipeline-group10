import os
from functions.logger import get_logger


logger = get_logger(__name__)


def scan_input_folder_for_new_csv(input_folder="input"):
	if not os.path.isdir(input_folder):
		logger.warning("Input folder does not exist: %s", input_folder)
		return []
	csv_files = [f for f in os.listdir(input_folder) if f.endswith(".csv")]
	logger.info("Found CSV files in input folder: %s", csv_files)
	return csv_files
