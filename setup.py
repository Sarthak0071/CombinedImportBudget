"""
Unified Data Processing Pipeline
=================================

A consolidated Python package for processing Nepal trade data, budget data, and darta (registration) data.

Modules:
- trade: Import/Export trade data processing (monthly calculations)
- budget: Budget data extraction and processing
- darta: PDF darta (registration) data processing
- core: Shared utilities and I/O operations
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding='utf-8') if readme_path.exists() else ""

setup(
    name="data-pipeline",
    version="1.0.0",
    description="Unified data processing pipeline for Nepal trade and budget data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/data-pipeline",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "pandas>=1.3.0",
        "openpyxl>=3.0.0",
        "xlrd>=2.0.0",
        "pycountry>=20.7.0",
        "pdfplumber>=0.10.0"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    entry_points={
        'console_scripts': [
            'process-trade=data_pipeline.trade.api:main',
            'process-budget=data_pipeline.budget.api:main',
            'process-darta=data_pipeline.darta.api:main',
        ],
    },
)
