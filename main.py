from functions.scan_input_folder import scan_input_folder_for_new_csv
from functions.auto_process_all_csv import auto_process_all_csv_files
from functions.version_output_files import version_output_files
from functions.compare_expected_vs_actual import compare_expected_vs_actual_output
from functions.commit_results import commit_results_to_repository

if __name__ == "__main__":
    print("🔍 Scanning input folder...")
    csv_files = scan_input_folder_for_new_csv()

    print("⚙️ Processing CSV files...")
    auto_process_all_csv_files()

    print("🗂️ Versioning output files...")
    version_output_files(csv_files)

    print("✅ Comparing expected vs actual...")
    compare_expected_vs_actual_output()

    print("📤 Committing results...")
    commit_results_to_repository()

    print("🎉 Pipeline complete!")