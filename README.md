# CSV Pipeline - Automation Control

A robust CI/CD-automated CSV processing pipeline that validates, cleans, and versions CSV data. This project demonstrates DevOps best practices using GitHub Actions, Python scripting, and collaborative development workflows.

## Overview

This pipeline automatically processes CSV files whenever code is pushed to the repository. It provides data cleaning, validation, versioning, and automated commit functionality—all orchestrated through GitHub Actions.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Core Functions](#core-functions)
- [Installation](#installation)
- [Usage](#usage)
- [CI/CD Pipeline](#cicd-pipeline)
- [Contributing](#contributing)

## Features

- ✅ **Automated CSV Processing** - Removes duplicates, strips whitespace, handles null values
- 📊 **Data Validation** - Compares input/output integrity and verifies data transformations
- 🗂️ **File Versioning** - Creates timestamped archives of processed files
- 📤 **Git Integration** - Automatically commits and pushes processed results
- 🔄 **CI/CD Ready** - Fully integrated with GitHub Actions for automated execution
- 🧪 **Testing Support** - Includes pytest framework and coverage analysis

## Project Structure

```
csv-pipeline-group10/
├── functions/              # Core processing modules (main component)
│   ├── scan_input_folder.py                    # Detect new CSV files
│   ├── auto_process_all_csv.py                 # Main data cleaning logic
│   ├── version_output_files.py                 # Archive processed files
│   ├── compare_expected_vs_actual.py           # Validation & verification
│   ├── commit_results.py                       # Git automation
│   └── __init__.py
├── input/                 # CSV input files
├── output/                # Processed CSV files
├── versions/              # Timestamped file archives
├── tests/                 # Unit and integration tests
├── main.py                # Pipeline orchestrator
├── requirements.txt       # Python dependencies
└── .github/workflows/     # GitHub Actions configuration
```

## Core Functions

The **`functions/`** folder contains the heart of the pipeline—modular functions that handle each stage of CSV processing:

### 1. **scan_input_folder.py** - Input Detection
```python
def scan_input_folder_for_new_csv(input_folder="input")
```
- Scans the `input/` directory for CSV files
- Returns a list of detected filenames
- Used as the first step to identify which files need processing

### 2. **auto_process_all_csv.py** - Data Processing Engine
```python
def auto_process_all_csv_files()
```
**The core processing function performs:**
- ✓ Duplicate row removal
- ✓ String column whitespace stripping
- ✓ Null value row removal
- ✓ Metadata injection (`processed_at`, `record_id`)
- ✓ Output saved to `output/processed_[filename].csv`

**Processing Pipeline:**
1. Read CSV from `input/`
2. Remove duplicate rows
3. Strip whitespace from string columns
4. Add processing timestamp and record IDs
5. Remove rows with missing values
6. Write cleaned data to `output/`

### 3. **version_output_files.py** - File Archival
```python
def version_output_files(csv_files: List[str])
```
- Creates timestamped copies of processed files
- Stores archives in `versions/` folder
- Format: `{filename}_{YYYYMMDD_HHMMSS}.csv`
- Enables audit trails and historical data retention

### 4. **compare_expected_vs_actual.py** - Data Validation
```python
def compare_expected_vs_actual_output()
```
**Validates output integrity by checking:**
- ✓ Output file exists for each input
- ✓ All original columns preserved
- ✓ Processing metadata added (`processed_at`, `record_id`)
- ✓ Reports row count changes with explanations
- ✓ Returns pass/fail status

### 5. **commit_results.py** - Git Automation
```python
def commit_results_to_repository()
```
- Stages `output/` and `versions/` folders
- Creates automated commit with message: `"Auto: commit processed output files [skip ci]"`
- Pushes changes to remote repository
- Gracefully handles non-git environments (CI-safe)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MatthewJames6184/csv-pipeline-group10.git
   cd csv-pipeline-group10
   ```

2. **Create virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Dependencies

- **pandas** - CSV processing and data manipulation
- **numpy** - Numerical operations
- **pytest** - Unit testing framework
- **mypy** - Static type checking
- **coverage** - Test coverage reporting

## Usage

### Manual Execution

Run the complete pipeline locally:
```bash
python main.py
```

This executes all five function stages in sequence:
1. 🔍 Scans `input/` for CSV files
2. ⚙️ Processes and cleans data
3. 🗂️ Versions output files
4. ✅ Compares expected vs actual output
5. 📤 Commits results to git

### Individual Function Usage

```python
from functions.auto_process_all_csv import auto_process_all_csv_files
from functions.compare_expected_vs_actual import compare_expected_vs_actual_output

# Process CSV files
auto_process_all_csv_files()

# Validate results
is_valid = compare_expected_vs_actual_output()
```

## CI/CD Pipeline

GitHub Actions automatically triggers this pipeline on every push via `.github/workflows/ci.yml`.

**Automated workflow:**
1. Checkout code
2. Setup Python environment
3. Install dependencies
4. Run `python main.py`
5. Commit and push processed files

The `[skip ci]` tag in commit messages prevents infinite workflow loops.

## Testing

Run the test suite:
```bash
pytest tests/
```

Generate coverage report:
```bash
pytest --cov=functions tests/
```

## Contributing

This is a collaborative DevOps learning project. When contributing:

1. Create a feature branch from `development`
2. Make changes and ensure tests pass
3. Push to your branch
4. Submit a pull request to `main`

All processing functions are located in the `functions/` folder—modify these when adding features or fixes to the pipeline.
