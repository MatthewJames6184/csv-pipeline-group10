# CSV Pipeline – Report Presentation Script

---

## Slide 1 – Introduction: What Does This Project Do?

> **Speaker notes:**
> "Our project is an automated CSV processing pipeline. When you drop a CSV file into the `input/` folder and run the program, it automatically cleans the data, saves the result, keeps a version history, validates the output, and commits everything to GitHub — without any manual steps."

**Pipeline overview (left to right):**

```
input/ CSV files
    → Scan
    → Process & Clean
    → Version
    → Validate
    → Commit to Git
```

---

## Slide 2 – Project Structure

> **Speaker notes:**
> "Here is how the project is laid out. All logic lives inside the `functions/` folder as separate modules. `main.py` is the entry point that calls them in order. The `tests/` folder holds our unit tests."

```
csv-pipeline-group10/
│
├── main.py                        ← Entry point, runs the full pipeline
│
├── functions/
│   ├── scan_input_folder.py       ← Step 1: Detect CSV files
│   ├── auto_process_all_csv.py    ← Step 2: Clean & transform data
│   ├── version_output_files.py    ← Step 3: Save timestamped copies
│   ├── compare_expected_vs_actual.py  ← Step 4: Validate output
│   └── commit_results.py          ← Step 5: Git add / commit / push
│
├── input/      ← Raw CSV files go here
├── output/     ← Processed files are written here
├── versions/   ← Timestamped backups are stored here
└── tests/      ← Unit tests
```

---

## Slide 3 – Entry Point: `main.py`

> **Speaker notes:**
> "`main.py` is the conductor. It calls each pipeline step in sequence and prints progress messages so the user knows what is happening. There are five steps, each handled by its own dedicated function."

```python
# main.py
csv_files = scan_input_folder_for_new_csv()   # Step 1
auto_process_all_csv_files()                  # Step 2
version_output_files(csv_files)               # Step 3
compare_expected_vs_actual_output()           # Step 4
commit_results_to_repository()                # Step 5
```

**Key design choice:** Each step is isolated in its own module, making the pipeline easy to test, extend, or replace one part at a time.

---

## Slide 4 – Step 1: Scanning the Input Folder

**File:** `functions/scan_input_folder.py`

> **Speaker notes:**
> "The first step simply looks inside the `input/` folder and returns a list of every `.csv` file it finds. If the folder does not exist it returns an empty list safely, so the pipeline never crashes on a missing directory."

```python
def scan_input_folder_for_new_csv(input_folder="input"):
    if not os.path.isdir(input_folder):
        return []                           # Safe fallback
    csv_files = [f for f in os.listdir(input_folder) if f.endswith(".csv")]
    print(f"Found: {csv_files}")
    return csv_files
```

**Output example:**
```
Found: ['day.csv', 'jonas.csv', 'sample.csv']
```

---

## Slide 5 – Step 2: Processing & Cleaning the CSV Files

**File:** `functions/auto_process_all_csv.py`

> **Speaker notes:**
> "This is the core data transformation step. For every CSV file found in the input folder, four cleaning operations are applied using the pandas library."

### 4 Cleaning Operations Applied to Each File

| # | Operation | What it does |
|---|-----------|--------------|
| 1 | `drop_duplicates()` | Removes identical duplicate rows |
| 2 | `str.strip()` | Trims leading/trailing whitespace from text columns |
| 3 | Add metadata columns | Appends `processed_at` (timestamp) and `record_id` |
| 4 | `dropna()` | Removes any rows that still contain null values |

**Output example:**
```
Processed: day.csv → processed_day.csv (35 rows, 2 removed)
```

The cleaned file is written to `output/processed_<filename>.csv`.

---

## Slide 6 – Step 3: Versioning the Output Files

**File:** `functions/version_output_files.py`

> **Speaker notes:**
> "After processing, each output file is copied into the `versions/` folder with a timestamp embedded in the filename. This gives us a full audit trail — we can always go back and see what the data looked like after any specific pipeline run."

```python
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
versioned_file = f"{base_name}_{timestamp}.csv"
shutil.copy2(source_path, version_path)
```

**Example versioned filenames:**
```
versions/
    day_20260304_020205.csv
    jonas_20260304_020205.csv
    sample_20260304_020205.csv
```

All three files share the same timestamp, so you can always identify which files were produced together in one run.

---

## Slide 7 – Step 4: Validation (Compare Expected vs Actual)

**File:** `functions/compare_expected_vs_actual.py`

> **Speaker notes:**
> "Before committing anything, the pipeline validates that the output files are correct. It performs three checks for every input/output pair."

### 3 Validation Checks

1. **Output file exists** — confirms the processing step did not silently fail.
2. **No original columns were lost** — the output must contain every column from the input.
3. **Metadata was added** — confirms `processed_at` and `record_id` columns are present.

**Console output example:**
```
✅ day.csv: 35 rows preserved
✅ day.csv: Processing metadata added
✅ All comparisons passed
```

If any check fails, a clear `❌` message is printed and the function returns `False`.

---

## Slide 8 – Step 5: Committing Results to Git

**File:** `functions/commit_results.py`

> **Speaker notes:**
> "The final step closes the loop by automatically pushing the results back to the GitHub repository. This means every pipeline run is fully reproducible — the processed data and version history are always in sync with the code."

```python
subprocess.run(["git", "add", "output/"])
subprocess.run(["git", "add", "versions/"])
subprocess.run(["git", "commit", "-m", "Auto: commit processed output files [skip ci]"])
subprocess.run(["git", "push"])
```

**Safety handling:**
- If not inside a git repo → skips gracefully with a message.
- If there is nothing new to commit → reports "Nothing new to commit." and exits.
- If `git` is not installed → catches `FileNotFoundError` and skips.

---

## Slide 9 – Testing

**File:** `tests/test_functions.py`

> **Speaker notes:**
> "We have a test suite using pytest. The current tests verify that the scan function always returns a Python list, which is the contract the rest of the pipeline depends on."

```python
def test_scan_returns_list():
    result = scan_input_folder_for_new_csv()
    assert isinstance(result, list)
```

Run tests with:
```bash
pytest tests/
```

---

## Slide 10 – Full Pipeline Flow (Summary Diagram)

```
┌────────────────────────────────────────────────────────┐
│                        main.py                         │
└──┬─────────────────────────────────────────────────────┘
   │
   ▼
┌──────────────────────────────┐
│  1. scan_input_folder        │  Finds *.csv in input/
└──┬───────────────────────────┘
   │  [day.csv, jonas.csv, sample.csv]
   ▼
┌──────────────────────────────┐
│  2. auto_process_all_csv     │  Dedup → Strip → Add metadata → Drop nulls
└──┬───────────────────────────┘
   │  Writes output/processed_*.csv
   ▼
┌──────────────────────────────┐
│  3. version_output_files     │  Copies output → versions/<name>_<timestamp>.csv
└──┬───────────────────────────┘
   │
   ▼
┌──────────────────────────────┐
│  4. compare_expected_vs_actual│ Validates columns, row counts, metadata
└──┬───────────────────────────┘
   │  ✅ or ❌ per file
   ▼
┌──────────────────────────────┐
│  5. commit_results           │  git add → git commit → git push
└──────────────────────────────┘
```

---

## Slide 11 – Key Design Principles

> **Speaker notes:**
> "To wrap up the technical overview, here are the four design principles that guided how we built this."

| Principle | How it's applied |
|-----------|-----------------|
| **Single Responsibility** | Each function does exactly one job |
| **Fail-safe defaults** | Missing folders, empty inputs, and missing git all handled gracefully |
| **Audit trail** | Every run produces timestamped version files |
| **Automation** | Zero manual steps from raw CSV to committed results |

---

*End of presentation script.*
