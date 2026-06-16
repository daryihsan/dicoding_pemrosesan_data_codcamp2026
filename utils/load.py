from sqlalchemy import create_engine
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

def store_to_csv(data, filename='products.csv'):
    """ Fungsi untuk menyimpan data ke dalam flat file (.CSV). """
    try:
        if data.empty:
            print("Peringatan data kosong, tidak ada yang disimpan ke CSV.")
            return False
            
        data.to_csv(filename, index=False)
        print("Data berhasil ditambahkan ke CSV.")
        return True
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data: {e}")
        return False

def store_to_postgre(data, db_url):
    """Fungsi untuk menyimpan data ke dalam PostgreSQL. """
    try:
        if data.empty:
            print("Peringatan data kosong, tidak ada yang disimpan ke PostgreSQL.")
            return False
        
        # Membuat engine database
        engine = create_engine(db_url)
        
        # Menyimpan data ke tabel 'fashiontoscrape' jika tabel sudah ada, data akan ditambahkan (append)
        with engine.connect() as con:
            data.to_sql('fashiontoscrape', con=con, if_exists='append', index=False)
            print("Data berhasil ditambahkan ke PostgreSQL.")
    
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data: {e}")
        return False


def store_to_gsheets(data, credentials_file, spreadsheet_id, range_name='Sheet1!A1'):
    """ Fungsi untuk menyimpan data ke dalam Google Sheets menggunakan Google Sheets API dengan retry logic. """
    import time
    import socket
    
    try:
        if data.empty:
            print("Peringatan data kosong, tidak ada yang disimpan ke Google Sheets.")
            return False

        # Setup Scopes & Credetials untuk Google Sheets API
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        credential = Credentials.from_service_account_file(credentials_file, scopes=SCOPES)
        
        # Membangun service API dengan timeout
        from googleapiclient.http import HttpRequest
        HttpRequest.timeout = 60  # 60 second timeout
        
        service = build('sheets', 'v4', credentials=credential)
        sheet = service.spreadsheets()

        # Ubah semua tipe data menjadi string agar kompatibel dengan format JSON (API Google)
        data_string = data.astype(str)
        
        # Menyiapkan nilai untuk ditulis (Header + Data baris)
        values = [data_string.columns.tolist()] + data_string.values.tolist()
        body = {'values': values}

        # Retry logic - coba hingga 3 kali jika gagal
        max_retries = 3
        for attempt in range(1, max_retries + 1):
            try:
                print(f"Upload ke Google Sheets (attempt {attempt}/{max_retries})...")
                result = sheet.values().update(
                    spreadsheetId=spreadsheet_id, 
                    range=range_name,
                    valueInputOption='RAW', 
                    body=body
                ).execute()

                print("Data berhasil ditambahkan ke Google Sheets.")
                return True
                
            except (socket.error, OSError, TimeoutError) as e:
                # Network/connection errors - retry
                if attempt < max_retries:
                    print(f"⚠️ Connection error (attempt {attempt}): {str(e)[:60]}...")
                    wait_time = 3 * attempt  # 3, 6, 9 seconds
                    print(f"Coba lagi dalam {wait_time} detik...")
                    time.sleep(wait_time)
                else:
                    raise
                    
    except FileNotFoundError:
        print(f"File kredensial '{credentials_file}' tidak ditemukan.")
        return False
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan ke Google Sheets: {e}")
        return False