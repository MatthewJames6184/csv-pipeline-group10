import os
import pandas as pd
from datetime import datetime

def auto_process_all_csv_files():
    input_folder = "input"
    output_folder = "output"
    
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    csv_files = [f for f in os.listdir(input_folder) if f.endswith(".csv")]
    
    for file in csv_files:
        try:
            # Read CSV file
            input_path = os.path.join(input_folder, file)
            df = pd.read_csv(input_path)
            
            # Data processing steps:
            # 1. Remove any duplicate rows
            original_rows = len(df)
            df = df.drop_duplicates()
            
            # 2. Strip whitespace from string columns
            for col in df.select_dtypes(include=['object']).columns:
                df[col] = df[col].str.strip()
            
            # 3. Add processing metadata
            df['processed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            df['record_id'] = range(1, len(df) + 1)
            
            # 4. Remove rows with any null values
            df = df.dropna()
            
            # Write processed file
            output_path = os.path.join(output_folder, f"processed_{file}")
            df.to_csv(output_path, index=False)
            
            rows_processed = len(df)
            rows_removed = original_rows - rows_processed
            print(f"Processed: {file} → processed_{file} ({rows_processed} rows, {rows_removed} removed)")
            
        except Exception as e:
            print(f"Error processing {file}: {e}")
    
    return csv_files