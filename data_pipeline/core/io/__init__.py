"""Core I/O module."""

from .csv_handler import (
    read_csv,
    save_csv,
    create_backup,
    merge_with_base,
    detect_file_type,
    validate_csv_structure
)

from .excel_reader import BaseExcelReader

__all__ = [
    'read_csv',
    'save_csv',
    'create_backup',
    'merge_with_base',
    'detect_file_type',
    'validate_csv_structure',
    'BaseExcelReader'
]
