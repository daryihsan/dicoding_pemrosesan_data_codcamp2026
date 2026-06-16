import pandas as pd
from unittest.mock import patch, MagicMock
from utils.load import store_to_csv, store_to_postgre, store_to_gsheets

# Setup dummy dataframe
dummy_df = pd.DataFrame({"Title": ["Test"], "Price": [160000]})

# Test CSV
@patch('pandas.DataFrame.to_csv')
def test_store_to_csv_success(mock_to_csv):
    result = store_to_csv(dummy_df, 'test.csv')
    assert result is True
    mock_to_csv.assert_called_once() # Memastikan to_csv dipanggil

def test_store_to_csv_empty():
    empty_df = pd.DataFrame()
    result = store_to_csv(empty_df, 'test.csv')
    assert result is False

# Test PostgreSQL
@patch('utils.load.create_engine')
@patch('pandas.DataFrame.to_sql')
def test_store_to_postgre_success(mock_to_sql, mock_engine):
    # Setup mock connection
    mock_con = MagicMock()
    mock_engine.return_value.connect.return_value.__enter__.return_value = mock_con
    
    result = store_to_postgre(dummy_df, 'postgresql://dummy')
    
    # Karena tidak ada return value, 
    # maka cek apakah to_sql benar-benar dijalankan oleh fungsi.
    mock_to_sql.assert_called_once()

def test_store_to_postgre_empty():
    result = store_to_postgre(pd.DataFrame(), 'postgresql://dummy')
    assert result is False

# Test Google Sheets
@patch('utils.load.build')
@patch('utils.load.Credentials.from_service_account_file')
def test_store_to_gsheets_success(mock_creds, mock_build):
    # Setup Mocks
    mock_service = MagicMock()
    mock_sheet = MagicMock()
    mock_update = MagicMock()
    
    mock_update.execute.return_value = {'updatedCells': 10}
    mock_sheet.values().update.return_value = mock_update
    mock_service.spreadsheets.return_value = mock_sheet
    mock_build.return_value = mock_service
    
    result = store_to_gsheets(dummy_df, 'dummy.json', 'dummy_id')
    assert result is True

def test_store_to_gsheets_empty():
    result = store_to_gsheets(pd.DataFrame(), 'dummy.json', 'dummy_id')
    assert result is False

# Tes block Exception (error)
@patch('pandas.DataFrame.to_csv')
def test_store_to_csv_exception(mock_to_csv):
    # Sengaja membuat to_csv melempar error
    mock_to_csv.side_effect = Exception("Sengaja Error")
    result = store_to_csv(dummy_df, 'test.csv')
    assert result is False

@patch('utils.load.create_engine')
def test_store_to_postgre_exception(mock_engine):
    # Sengaja membuat engine database error
    mock_engine.side_effect = Exception("DB Error")
    result = store_to_postgre(dummy_df, 'postgresql://dummy')
    assert result is False

@patch('utils.load.build')
@patch('utils.load.Credentials.from_service_account_file')
def test_store_to_gsheets_exception(mock_creds, mock_build):
    # Sengaja membuat API Google Sheets error
    mock_build.side_effect = Exception("API Error")
    result = store_to_gsheets(dummy_df, 'dummy.json', 'dummy_id')
    assert result is False

@patch('utils.load.Credentials.from_service_account_file')
def test_store_to_gsheets_file_not_found(mock_creds):
    # Sengaja memicu FileNotFoundError
    mock_creds.side_effect = FileNotFoundError("File JSON tidak ditemukan")
    
    result = store_to_gsheets(dummy_df, 'file_palsu_yang_ga_ada.json', 'dummy_id')
    
    # Harus return False karena gagal
    assert result is False