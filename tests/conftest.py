"""Pytest configuration and fixtures."""

import pytest
from pathlib import Path
import pandas as pd


@pytest.fixture(scope="session")
def data_dir():
    """Return path to data directory."""
    return Path(__file__).parent.parent / 'data'


@pytest.fixture(scope="session")
def budget_file(data_dir):
    """Return path to budget test file."""
    return str(data_dir / '82-83.xlsx')


@pytest.fixture(scope="session")
def trade_file(data_dir):
    """Return path to trade test file."""
    return str(data_dir / 'FTS_uptoAsoj_208283_ci1nozq.xlsx')


@pytest.fixture(scope="session")
def done_file(data_dir):
    """Return path to done.csv file."""
    return str(data_dir / 'done.csv')


@pytest.fixture(scope="session")
def darta_file(data_dir):
    """Return path to darta PDF file."""
    return str(data_dir / 'darta.pdf')


@pytest.fixture
def sample_trade_df():
    """Sample trade dataframe."""
    return pd.DataFrame({
        'Year': [2081, 2081],
        'Month': [4, 5],
        'Direction': ['I', 'I'],
        'HS_Code': ['1001', '1002'],
        'Country': ['IN', 'CN'],
        'Value': [100.0, 200.0],
        'Quantity': [10.0, 20.0],
        'Unit': ['kg', 'kg'],
        'Revenue': [50.0, 100.0]
    })

