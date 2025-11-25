"""Configuration settings and constants."""
from pathlib import Path
from typing import Dict

NEPALI_MONTHS: Dict[int, str] = {
    1: 'Baishakh',
    2: 'Jestha',
    3: 'Ashad',
    4: 'Shrawan',
    5: 'Bhadra',
    6: 'Ashwin',
    7: 'Kartik',
    8: 'Mangsir',
    9: 'Poush',
    10: 'Magh',
    11: 'Falgun',
    12: 'Chaitra'
}

MONTH_NAME_TO_NUMBER: Dict[str, int] = {
    'Baishakh': 1, 'Jestha': 2, 'Ashad': 3, 'Shrawan': 4,
    'Bhadra': 5, 'Ashwin': 6, 'Kartik': 7, 'Mangsir': 8,
    'Poush': 9, 'Magh': 10, 'Falgun': 11, 'Chaitra': 12
}

CUSTOM_COUNTRY_MAPPINGS: Dict[str, str] = {
    'Namibia': 'NA',
    'Wallis and Futuna Islands': 'WF',
    'Yugoslavia': 'RS',
    'Zaire': 'CD',
    'Swaziland': 'SZ',
    'Kazakstan': 'KZ',
    'Viet Nam': 'VN',
    'Libyan Arab Jamahiriya': 'LY',
    'Holy See (Vatican)': 'VA',
    'Brunei Darussalam': 'BN',
    "Cote d'Ivoire": 'CI',
    'Turkey': 'TR',
    'Congo': 'CG',
    'East Timor': 'TL',
    'Christmas Island[Australia]': 'CX',
    'Cocos (Keeling) Islands': 'CC',
    'Bouvet Island': 'BV',
    'British Indian Ocean Territory': 'IO',
    'Kosovo': 'XK',
    'Taiwan, Province of China': 'TW',
    'Serbia (Europe)': 'RS',
    'The former Yugoslav Rep. Macedonia': 'MK',
    'Johnston Island': 'UM',
    'Midway Islands': 'UM',
    'Wake Island': 'UM',
    'Many Countries': 'MANY',
    'Not_Specified': 'NOT_SPECIFIED',
    'Saint Helena': 'SH',
    'Saint Lucia': 'LC',
    'Saint Vincent and the Grenadines': 'VC',
}

COUNTRY_NAME_NORMALIZATIONS: Dict[str, str] = {
    'Iran, Islamic Republic of': 'Iran',
    "Korea, Democratic People's Rep. of": "Korea, Democratic People's Republic of",
    'Korea, Republic of': 'Korea, Republic of',
    "Lao People's Democratic Republic": "Lao People's Democratic Republic",
    'Syrian Arab Republic': 'Syrian Arab Republic',
    'United Republic of Tanzania': 'Tanzania, United Republic of',
    'Republic of Moldova': 'Moldova, Republic of',
    'Russian Federation': 'Russian Federation',
    'United States Virgin Islands': 'Virgin Islands, U.S.',
    'British Virgin Islands': 'Virgin Islands, British',
    'Micronesia, Federated States of': 'Micronesia, Federated States of',
    'Cape Verde': 'Cabo Verde',
}

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / 'data'

DONE_CSV_PATH = DATA_DIR / 'done.csv'
CUMULATIVE_EXCEL_PATH = DATA_DIR / 'FTS_uptoAsoj_208283_ci1nozq.xlsx'

OUTPUT_DIR = DATA_DIR
UPDATED_CSV_NAME = 'doneupdated.csv'
CUMULATIVE_CSV = 'ashwin_cumulative.csv'
MONTHLY_CSV = 'ashwin_monthly.csv'

TARGET_YEAR = 2082
TARGET_MONTH = 6
PREVIOUS_MONTH = 5

EXPECTED_COLUMNS = ['Year', 'Month', 'Direction', 'HS_Code', 'Country', 
                   'Value', 'Quantity', 'Unit', 'Revenue']

IMPORT_SHEET_KEYWORDS = ['4', 'import', 'table 4']
EXPORT_SHEET_KEYWORDS = ['6', 'export', 'table 6']