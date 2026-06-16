from utils.extract import scrape_fashion
from utils.transform import clean_and_transform
from utils.load import store_to_csv, store_to_postgre, store_to_gsheets
from dotenv import load_dotenv
import os

def main():
    """Fungsi utama untuk keseluruhan proses ETL."""
    BASE_URL = 'https://fashion-studio.dicoding.dev/'

    load_dotenv()
    postgres_db_url = os.getenv('DATABASE_URL')
    SPREADSHEET_ID = os.getenv('GOOGLE_SHEETS_ID')
    SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')

    print("=== Mulai Proses Scraping ===")
    raw_data = scrape_fashion(BASE_URL) 
    
    print("\n=== Mulai Proses Transform ===")
    clean_df = clean_and_transform(raw_data)
    
    if not clean_df.empty:
        print("\n=== Mulai Proses Load PostgreSQL ===")
        store_to_postgre(clean_df, postgres_db_url)

        print("\n=== Mulai Proses Load Google Sheets ===")
        store_to_gsheets(clean_df, SERVICE_ACCOUNT_FILE, SPREADSHEET_ID)

        print("\n=== Mulai Proses Load CSV ===")
        store_to_csv(clean_df)
    else:
        print("Data bersih kosong, tidak ada yang disimpan ke PostgreSQL, Google Sheets, atau CSV.")   

if __name__ == '__main__':
    main()
