import pandas as pd
from utils.transform import clean_and_transform

def test_clean_and_transform_success():
    # Setup data kotor
    raw_data = [
        {
            "Title": "Kaos Polos",
            "Price": "$10.50",
            "Rating": "Rating: ⭐ 4.0 / 5",
            "Colors": "3 Colors",
            "Size": "Size: L",
            "Gender": "Gender: Women",
            "timestamp": "2026-04-21 10:00:00.000"
        },
        {
            "Title": "Unknown Product", # Harus terhapus karena invalid
            "Price": "$100.00",
            "Rating": "Invalid Rating",
            "Colors": "5 Colors",
            "Size": "Size: M",
            "Gender": "Gender: Men",
            "timestamp": "2026-04-21 10:00:00.000"
        }
    ]
    
    df = clean_and_transform(raw_data)
    
    # Memastikan baris 'Unknown Product' terhapus, sisa 1 baris
    assert len(df) == 1
    
    # Memastikan konversi benar
    assert df.iloc[0]['Title'] == "Kaos Polos"
    assert df.iloc[0]['Price'] == 168000.0  # 10.50 * 16000
    assert df.iloc[0]['Rating'] == 4.0
    assert df.iloc[0]['Colors'] == 3
    assert df.iloc[0]['Size'] == "L"
    assert df.iloc[0]['Gender'] == "Women"

def test_clean_and_transform_empty_data():
    # Jika diberikan list kosong, harus mengembalikan DF kosong
    df = clean_and_transform([])
    assert df.empty

from unittest.mock import patch

def test_clean_and_transform_key_error():
    # Sengaja memberikan data yang tidak punya kolom 'Title' atau 'Price'
    bad_data = [{"SalahKolom": "Data Ngawur"}]
    df = clean_and_transform(bad_data)
    
    # Harus mengembalikan DataFrame kosong karena gagal transformasi
    assert df.empty

def test_clean_and_transform_exception():
    # Sengaja mengirim tipe data integer (bukan list/dict) agar pandas error ketika mencoba membuat DataFrame
    bad_input = 12345 
    df = clean_and_transform(bad_input)
    
    # Harus mengembalikan DataFrame kosong karena masuk ke blok except
    assert df.empty