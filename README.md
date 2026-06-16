# ETL Pipeline - Fashion Data Scraping & Integration

Proyek Extract, Transform, Load (ETL) untuk scraping data fashion dari website, kemudian menyimpan ke PostgreSQL, Google Sheets, dan CSV.

## 📁 Struktur Folder

```
submission-pemda/
├── tests/
│   ├── test_extract.py      # Unit tests untuk scraping
│   ├── test_transform.py    # Unit tests untuk transformasi data
│   └── test_load.py         # Unit tests untuk penyimpanan data
├── utils/
│   ├── __init__.py
│   ├── extract.py           # Web scraping logic
│   ├── transform.py         # Data cleaning & transformation
│   └── load.py              # Save to PostgreSQL, Google Sheets, CSV
├── main.py                  # Entry point - orchestrates ETL pipeline
├── requirements.txt         # Python dependencies
├── README.md                # (This file)
├── submission.txt           # Submission notes & URLs
├── products.csv             # Output: Cleaned product data
└── google-sheets-api.json   # (NOT PUSHED) Google Sheets API credentials
```

## 📊 Deskripsi Proyek

### Pipeline ETL

**Extract** → **Transform** → **Load**

1. **Extract** (E)
   - Web scraping dari: `https://fashion-studio.dicoding.dev/`
   - Menggunakan BeautifulSoup untuk parsing HTML
   - Header User-Agent untuk menghindari blocking
   - Error handling untuk timeouts & connection errors

2. **Transform** (T)
   - Data cleaning (handle missing values, duplicates)
   - Data normalization (consistent formats)
   - Feature engineering (jika diperlukan)
   - Output: Clean DataFrame

3. **Load** (L)
   - **PostgreSQL**: Simpan ke tabel fashion database
   - **Google Sheets**: Sinkronisasi ke spreadsheet online
   - **CSV**: Export ke local file (`products.csv`)

### Data Destinations

| Destination | Purpose | File/Config |
|------------|---------|-------------|
| PostgreSQL | Primary database | `postgresql+psycopg2://...` |
| Google Sheets | Shared spreadsheet | `SPREADSHEET_ID` |
| CSV | Local backup | `products.csv` |

## 🚀 Cara Menggunakan

### Prerequisites

- Python 3.8+
- PostgreSQL installed & running
- Google Cloud Project dengan Sheets API enabled
- Google Sheets API credentials

### Setup Environment

1. **Clone Repository**:
```bash
git clone https://github.com/your-username/submission-pemda.git
cd submission-pemda
```

2. **Create Virtual Environment**:
```bash
# Windows
python -m venv .env
.env\Scripts\Activate.ps1

# Linux/Mac
python3 -m venv .env
source .env/bin/Activate.ps1
```

3. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

4. **Setup Google Sheets API Credentials**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create Service Account
   - Download JSON credentials as `google-sheets-api.json`
   - Place in project root directory
   - **⚠️ NEVER commit this file to GitHub!**

5. **Setup Database Connection**:
   - Edit `main.py` line 12:
   ```python
   postgres_db_url = 'postgresql+psycopg2://username:password@localhost:5432/fashionsdb'
   ```
   - Atau gunakan environment variables (lebih aman)

6. **Update Spreadsheet ID** (jika pakai custom spreadsheet):
   - Edit `main.py` line 13:
   ```python
   SPREADSHEET_ID = 'your-spreadsheet-id-here'
   ```

### Running the Pipeline

**Run full ETL pipeline**:
```bash
python main.py
```

**Run unit tests**:
```bash
python -m pytest tests/
```

**Run tests dengan coverage report**:
```bash
python -m pytest --cov=utils tests/
```

**Run specific test file**:
```bash
python -m pytest tests/test_extract.py -v
```

## 📋 Dependencies

### Core Libraries
- **requests** - HTTP library untuk web scraping
- **beautifulsoup4** - HTML parsing & data extraction
- **pandas** - Data manipulation & analysis
- **sqlalchemy** - ORM untuk database operations
- **psycopg2-binary** - PostgreSQL driver

### Google Integration
- **google-auth** - Authentication untuk Google APIs
- **google-api-python-client** - Google Sheets API client

### Testing & Utilities
- **pytest-cov** - Testing dengan coverage metrics
- **python-crontab** - Task scheduling (optional)

Lihat `requirements.txt` untuk detail lengkap dengan version constraints.

## 🧪 Testing

Project ini dilengkapi dengan unit tests untuk setiap modul:

```bash
# All tests
pytest tests/

# Verbose output
pytest tests/ -v

# With coverage
pytest tests/ --cov=utils

# Single test file
pytest tests/test_extract.py

# Single test function
pytest tests/test_extract.py::test_fetching_product
```

## 📊 Output & Results

### CSV Output
File: `products.csv`
- Cleaned product data
- Ready untuk analisis lebih lanjut

### PostgreSQL Storage
Database: `fashionsdb`
- Stored untuk long-term persistence
- Query-able untuk business intelligence

### Google Sheets
Sheet: [Link di submission.txt](submission.txt)
- Real-time collaboration
- Easy sharing dengan tim

## 🔍 Module Overview

### `utils/extract.py`
```python
scrape_fashion(base_url)  # Main scraping function
fetching_product(url)     # Fetch HTML content
extract_fashion_data()    # Parse individual product
```

### `utils/transform.py`
```python
clean_and_transform(raw_data)  # Data cleaning & transformation
```

### `utils/load.py`
```python
store_to_postgre()      # Save to PostgreSQL
store_to_gsheets()      # Save to Google Sheets
store_to_csv()          # Save to CSV file
```

## 🔒 Security & Best Practices

### Files NOT Pushed to GitHub (Protected):
- ✅ `.env/` - Virtual environment
- ✅ `google-sheets-api.json` - API credentials
- ✅ `.coverage/` - Test coverage reports
- ✅ `htmlcov/` - HTML coverage reports
- ✅ `__pycache__/` - Python cache
- ✅ `.env` - Environment variables

### Sensitive Information:
**NEVER commit these to public repositories:**
- ❌ Database credentials
- ❌ API keys & tokens
- ❌ Google Sheets API credentials
- ❌ Private URLs
- ❌ User passwords

### Best Practices:
1. Use `.env` file untuk credentials (tidak di-push)
2. Use environment variables di production
3. Jangan share `google-sheets-api.json`
4. Review `.gitignore` sebelum push
5. Gunakan Private repository jika ada sensitive data

## 📱 Environment Variables (Recommended)

Buat `.env` file di root folder (copy .env.example):
```bash
DATABASE_URL=postgresql+psycopg2://user:password@localhost/fashionsdb
GOOGLE_SHEETS_ID=your-spreadsheet-id
SERVICE_ACCOUNT_FILE=./google-sheets-api.json
```

Kemudian di code:
```python
from dotenv import load_dotenv
import os

load_dotenv()
postgres_db_url = os.getenv('DATABASE_URL')
SPREADSHEET_ID = os.getenv('GOOGLE_SHEETS_ID')
```

## 📈 Performance & Monitoring

- ⏱️ Scraping timeout: 10 detik per URL
- 🔄 Error handling: Try-except untuk network issues
- 📊 Logging: Print statements untuk monitoring progress
- 🧪 Coverage: Unit tests untuk data quality assurance

## 🐛 Troubleshooting

### Error: "Connection refused" PostgreSQL
```bash
# Pastikan PostgreSQL running
# Windows: Services > PostgreSQL
# Linux: sudo systemctl start postgresql
```

### Error: "google-sheets-api.json not found"
```bash
# Download credentials dari Google Cloud Console
# Rename to google-sheets-api.json
# Place di root folder
```

### Error: "No module named 'utils'"
```bash
# Pastikan current directory adalah root folder
cd /path/to/submission-pemda
python main.py
```

### Tests failing
```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Run with verbose output
pytest tests/ -v -s
```

## 📚 Resources

- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [SQLAlchemy Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/)
- [Google Sheets API Guide](https://developers.google.com/sheets/api/guides/concepts)
- [Pytest Documentation](https://docs.pytest.org/)

## 📧 Author

**Dary Ihsan Amanullah**
- Program: Coding Camp Powered by DBS Foundation 2026, Dicoding - Data Scientist Path
- Subject: Data Processing (Pemrosesan Data)

## 📄 License

Project ini adalah submission untuk Dicoding learning path.
Lihat terms & conditions dari Dicoding untuk usage rights.

---

**Status**: Submission Ready  
**Last Updated**: 2026  
**Test Coverage**: Run `pytest --cov=utils tests/` untuk check coverage
