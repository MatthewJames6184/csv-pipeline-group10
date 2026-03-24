from functions.scan_input_folder import scan_input_folder_for_new_csv
from functions.auto_process_all_csv import auto_process_all_csv_files
from functions.version_output_files import version_output_files
from functions.compare_expected_vs_actual import compare_expected_vs_actual_output
from functions.commit_results import commit_results_to_repository
from functions.logger import get_logger


logger = get_logger(__name__)

if __name__ == "__main__":
    logger.info("Scanning input folder")
    csv_files = scan_input_folder_for_new_csv()

    logger.info("Processing CSV files")
    auto_process_all_csv_files()

    logger.info("Versioning output files")
    version_output_files(csv_files)

    logger.info("Comparing expected vs actual")
    compare_expected_vs_actual_output()

    logger.info("Committing results")
    commit_results_to_repository()

    logger.info("Pipeline complete")