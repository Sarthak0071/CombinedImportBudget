# Data Pipeline - Unified Processing System

A consolidated Python package for processing Nepal **trade data** (import/export) and **budget data** with shared utilities and domain-specific operations.

## Overview

This unified platform combines two previously separate projects:
- **Trade Processing** (ImportExportB): Calculate monthly values from cumulative import/export data
- **Budget Processing**: Extract and merge multi-year budget data

### Key Consolidation Benefits

✅ **~40% Code Reuse**: Shared modules for file I/O, validation, and utilities  
✅ **Unified Logging & Backup**: Consistent patterns across all operations  
✅ **Clear Separation**: Domain-specific logic in separate namespaces (`trade/`, `budget/`)  
✅ **Single Repository**: One source of truth for all data processing

---

## Installation

```bash
# From local directory
cd data-pipeline
pip install -e .

# Or from GitHub (when published)
pip install git+https://github.com/yourusername/data-pipeline.git
```

---

## Quick Start

### Trade Data Processing

Process cumulative import/export data to calculate monthly values:

```python
from data_pipeline.trade import process_monthly_data

# Process Excel file with cumulative trade data
result = process_monthly_data(
    xlsx_file='FTS_uptoAsoj_208283.xlsx',
    old_data='done.csv',
    output_name='updateddone.csv'
)

print(f"Processed {len(result):,} records")
```

**Outputs created:**
- `month.csv` - Monthly data only (for current month)
- `updateddone.csv` - Historical + new monthly data combined

---

### Budget Data Processing

Extract budget data and merge with historical records:

```python
from data_pipeline.budget import process_monthly_data

# Process budget Excel file
result = process_monthly_data(
    xlsx_file='82-83.xlsx',
    old_data='done.csv',
    output_name='output.csv'
)

print(f"Processed {len(result):,} records")
```

**Outputs created:**
- `2082.csv` - Year-specific clean data (for that year)
- `output.csv` - Combined all years

---

### Extract Year Data Only (Budget)

Extract and clean a single year without merging:

```python
from data_pipeline.budget import extract_year_data

# Extract year data only
df = extract_year_data('82-83.xlsx')
# Creates: 2082.csv
```

---

## Project Structure

```
data-pipeline/
├── data_pipeline/
│   ├── core/                   # Shared utilities (REUSABLE)
│   │   ├── io/                # File operations
│   │   │   ├── csv_handler.py # CSV read/write/backup
│   │   │   └── excel_reader.py # Base Excel reader
│   │   └── utils/             # Shared utilities
│   │       ├── data_utils.py  # Data transformation
│   │       └── logging_config.py
│   │
│   ├── trade/                  # Import/Export processing
│   │   ├── api.py             # process_monthly_data
│   │   ├── calculator.py      # Cumulative → Monthly
│   │   ├── cleaner.py         # Country code normalization
│   │   └── config.py          # Trade-specific configs
│   │
│   └── budget/                 # Budget processing
│       ├── api.py             # process_monthly_data, extract_year_data
│       ├── excel_reader.py    # Federal/Province/Local sheets
│       └── config.py          # Budget-specific configs
│
├── setup.py
├── requirements.txt
└── README.md
```

---

## Features

### Shared Core Modules

- **File I/O**: Unified CSV/Excel reading with encoding support
- **Backup Management**: Automatic timestamped backups
- **Data Validation**: Column validation and structure checks
- **Logging**: Consistent logging across all modules
- **Utilities**: Year extraction, numeric cleaning, column standardization

### Trade Module Features

- Auto-detect import (Table 4) and export (Table 6) sheets
- Calculate monthly values from cumulative data
- Country code normalization to ISO2
- HS Code processing
- Revenue tracking for imports

### Budget Module Features

- Auto-detect Federal/Province/Local sheets
- Extract fiscal year from filename
- Standardize budget columns
- Government level classification
- Support for Excel and CSV inputs

---

## Command Line Usage

After installation, use console commands:

```bash
# Process trade data
python -m data_pipeline.trade <xlsx_file> <old_data> [output_name]

# Process budget data
python -m data_pipeline.budget <xlsx_file> [old_data] [output_file]
```

---

## Requirements

- Python >= 3.7
- pandas >= 1.3.0
- openpyxl >= 3.0.0
- xlrd >= 2.0.0
- pycountry >= 20.7.0

---

## Migration from Previous Projects

If you were using the old separate packages:

**Old ImportExportB:**
```python
from UpdatedImp_exp import process_monthly_data
```

**New unified:**
```python
from data_pipeline.trade import process_monthly_data
```

---

**Old budget_processor:**
```python
from budget_processor import process_monthly_data
```

**New unified:**
```python
from data_pipeline.budget import process_monthly_data
```

---

## What's Reusable?

Components shared between trade and budget operations:
- CSV read/write operations
- Backup mechanism
- Year extraction and cleaning
- Numeric column cleaning
- Excel sheet detection
- Data validation
- Logging configuration

**Result:** Less duplication, easier maintenance, consistent behavior!

---

## License

MIT License (or your preferred license)

## Author

[Your Name]

## Contributing

Contributions welcome! Please open an issue or submit a pull request.
