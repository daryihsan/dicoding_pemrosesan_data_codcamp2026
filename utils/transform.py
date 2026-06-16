import pandas as pd

def clean_and_transform(raw_data):
    """
    Melakukan transformasi data mentah hasil scraping:
    1. Menghapus data invalid ('Unknown Product', 'Price Unavailable', 'Invalid Rating', 'Not Rated')
    2. Menghapus duplikat dan null
    3. Mengonversi tipe data
    4. Mengonversi harga (USD) menjadi IDR (Rp16.000)
    """
    try:
        # Konversi list of dicts ke DataFrame
        df = pd.DataFrame(raw_data)
        
        # Jika dataframe kosong, langsung kembalikan dataframe kosong
        if df.empty:
            print("Peringatan: DataFrame kosong saat memulai transformasi.")
            return df
            
        print(f"Data awal sebelum transformasi: {len(df)} baris")

        # Membersihkan data Invalid di kolom Title dan Price
        df = df[~df['Title'].str.contains('Unknown Product', case=False, na=False)]
        df = df[~df['Price'].str.contains('Price Unavailable', case=False, na=False)]

        # Transformasi kolom 'Price' dengan menghapus '$', mengubah ke float, serta dikalikan 16.000
        # Menggunakan regex=False karena karakter '$' adalah spesial karakter di regex
        df['Price'] = df['Price'].astype(str).str.replace('$', '', regex=False)
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce') * 16000

        # Transformasi kolom 'Rating' dengan hanya mengambil float di depannya (misal "Rating: ⭐ 3.9 / 5")
        # Regex r'(\d+\.\d+)' akan mengambil angka desimal seperti 3.9 atau 4.8
        df['Rating'] = df['Rating'].astype(str).str.extract(r'(\d+\.\d+)').astype(float)
        
        # Menghapus baris yang rating-nya gagal diekstrak (yaitu "Not Rated" atau "Invalid Rating")
        df = df.dropna(subset=['Rating'])

        # Transformasi kolom 'Colors' dengan mengambil angkanya saja (misal "3 Colors" menjadi 3)
        df['Colors'] = df['Colors'].astype(str).str.extract(r'(\d+)').astype(int)

        # Transformasi kolom 'Size' dengan menghapus teks (yaitu "Size: ")
        df['Size'] = df['Size'].astype(str).str.replace('Size: ', '', regex=False).str.strip()

        # Transformasi kolom 'Gender' dengan menghapus teks (yaitu "Gender: ")
        df['Gender'] = df['Gender'].astype(str).str.replace('Gender: ', '', regex=False).str.strip()

        # Transformasi kolom 'timestamp' menjadi tipe datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

        # Menghapus duplikat dan baris yang memiliki nilai Null (NaN) 
        df = df.drop_duplicates()
        df = df.dropna()
        
        # Reset index agar menyesuaikan setelah banyak baris dihapus
        df = df.reset_index(drop=True)

        print(f"Transformasi selesai, sisa data bersih: {len(df)} baris")
        return df

    except KeyError as e:
        print(f"Error saat transformasi: Kolom tidak ditemukan {e}")
        return pd.DataFrame() 
    except Exception as e:
        print(f"Error tak terduga saat transformasi: {e}")
        return pd.DataFrame()