"""Budget-specific configuration constants."""

STANDARD_COLUMNS = [
    "Year", "Project_Code", "Sub_Project_Code", "Economic_Code",
    "District_Code", "Component_Code", "Donor_Code", 
    "Source_Type_Code", "Activity_Code", "Amount"
]

COLUMN_MAPPING = {
    "BUD_YEAR": "Year", "PROJECT_CODE": "Project_Code",
    "SUB_PROJECT_CODE": "Sub_Project_Code", "ECONOMIC_CODE5": "Economic_Code",
    "DISTRICT_CODE": "District_Code", "COMPONENT_CODE": "Component_Code",
    "DONOR_CODE": "Donor_Code", "SOURCE_TYPE_CODE": "Source_Type_Code",
    "ACTIVITY_CODE": "Activity_Code", "AMOUNT": "Amount"
}

COLUMNS_TO_REMOVE = [
    "VIN", "VOUT", "NET_BUDGET", "SUM(EXP)",
    "MINISTRY_CODE", "MINISTRY_NDESC", "MAIN_ACTIVITY_NDESC4",
    "PROJECT_NDESC", "SUB_PROJECT_NDESC", "MINISTRY", "GOVERNMENT_LEVEL"
]

SHEET_PATTERNS = {
    "federal": ["federal", "Federal", "FEDERAL"],
    "province": ["province", "Province", "PROVINCE", "provience"],
    "local": ["local", "Local", "LOCAL"]
}
