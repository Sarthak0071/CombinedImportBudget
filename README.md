# Data Pipeline

Unified data processing for Nepal trade and budget data.

## Installation

```bash
pip install git+https://github.com/Sarthak0071/CombinedImportBudget.git
```

## Usage

### Budget Processing

Extract clean year data from Excel/CSV:

```python
from data_pipeline.budget import process_monthly_data

result = process_monthly_data('data/82-83.xlsx')
# Output: 2082.csv
```

Optional - merge with historical data:

```python
result = process_monthly_data(
    xlsx_file='data/82-83.xlsx',
    old_data='done.csv',
    output_name='output.csv'
)
# Outputs: 2082.csv, output.csv
```

### Trade Processing

Calculate monthly values from cumulative import/export data:

```python
from data_pipeline.trade import process_monthly_data

result = process_monthly_data(
    xlsx_file='data/FTS_uptoAsoj_208283.xlsx',
    old_data='data/done.csv',
    output_name='updateddone.csv'
)
# Outputs: month.csv, updateddone.csv
```

## Requirements

- Python >= 3.7
- pandas >= 1.3.0
- openpyxl >= 3.0.0

## License

MIT
