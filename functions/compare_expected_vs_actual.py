import os
import pandas as pd
from functions.logger import get_logger


logger = get_logger(__name__)

def compare_expected_vs_actual_output():
    input_folder = "input"
    output_folder = "output"
    
    if not os.path.exists(output_folder):
        logger.warning("Output folder does not exist")
        return False
    
    # Get all input CSV files
    input_files = [f for f in os.listdir(input_folder) if f.endswith(".csv")]
    
    if len(input_files) == 0:
        logger.warning("No input files found")
        return False
    
    all_passed = True
    
    for input_file in input_files:
        processed_file = f"processed_{input_file}"
        input_path = os.path.join(input_folder, input_file)
        output_path = os.path.join(output_folder, processed_file)
        
        # Check if output file exists
        if not os.path.exists(output_path):
            logger.error("Missing output file: %s", processed_file)
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
                logger.error("%s: Missing columns in output: %s", input_file, missing_cols)
                all_passed = False
                continue
            
            # Report row count changes
            if output_rows < input_rows:
                logger.info(
                    "%s: %s -> %s rows (data cleaning applied)",
                    input_file,
                    input_rows,
                    output_rows,
                )
            elif output_rows == input_rows:
                logger.info("%s: %s rows preserved", input_file, output_rows)
            
            # Check for processing metadata
            if 'processed_at' in output_df.columns and 'record_id' in output_df.columns:
                logger.info("%s: Processing metadata added", input_file)
            
        except Exception as e:
            logger.exception("Error comparing %s: %s", input_file, e)
            all_passed = False
    
    if all_passed:
        logger.info("All comparisons passed")
    else:
        logger.warning("Some comparisons failed")
    
    return all_passed