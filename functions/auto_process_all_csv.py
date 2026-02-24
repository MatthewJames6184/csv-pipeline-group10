import os
import shutil

def auto_process_all_csv_files():
    # STUB — replace with real logic when Data Processing Lead is ready
    input_folder = "input"
    output_folder = "output"

    csv_files = [f for f in os.listdir(input_folder) if f.endswith(".csv")]

    for file in csv_files:
        src = os.path.join(input_folder, file)
        dst = os.path.join(output_folder, f"processed_{file}")
        shutil.copy(src, dst)
        print(f"Processed: {file} → processed_{file}")

    return csv_files