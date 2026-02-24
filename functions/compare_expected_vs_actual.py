import os
import pandas as pd

def compare_expected_vs_actual_output():
    input_folder = "input"
    output_folder = "output"
    
    if not os.path.exists(output_folder):
        print("⚠️ Output folder does not exist.")
        return False
    
    # Get all input CSV files
    input_files = [f for f in os.listdir(input_folder) if f.endswith(".csv")]
    
    if len(input_files) == 0:
        print("⚠️ No input files found.")
        return False
    
    all_passed = True
    
    for input_file in input_files:
        processed_file = f"processed_{input_file}"
        input_path = os.path.join(input_folder, input_file)
        output_path = os.path.join(output_folder, processed_file)
        
        # Check if output file exists
        if not os.path.exists(output_path):
            print(f"❌ Missing output file: {processed_file}")
            all_passed = False
            continue
        
        try:
            # Read both files
            input_df = pd.read_csv(input_path)
            output_df = pd.read_csv(output_path)
            
            # Validation checks
            input_rows = len(input_df)
            output_rows = len(output_df)
            
            # Check that output has expected columns (original + processing metadata)
            expected_cols = set(input_df.columns)
            output_cols = set(output_df.columns)
            
            # Output should have at least the original columns
            missing_cols = expected_cols - output_cols
            if missing_cols:
                print(f"❌ {input_file}: Missing columns in output: {missing_cols}")
                all_passed = False
                continue
            
            # Report row count changes
            if output_rows < input_rows:
                print(f"ℹ️ {input_file}: {input_rows} → {output_rows} rows (data cleaning applied)")
            elif output_rows == input_rows:
                print(f"✅ {input_file}: {output_rows} rows preserved")
            
            # Check for processing metadata
            if 'processed_at' in output_df.columns and 'record_id' in output_df.columns:
                print(f"✅ {input_file}: Processing metadata added")
            
        except Exception as e:
            print(f"❌ Error comparing {input_file}: {e}")
            all_passed = False
    
    if all_passed:
        print("✅ All comparisons passed")
    else:
        print("⚠️ Some comparisons failed")
    
    return all_passed