import time
 
import requests
from bs4 import BeautifulSoup
from datetime import datetime
 
# Header untuk simulasi browser agar tidak terblokir
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

def fetching_product(url, max_retries=3, timeout=30):
    """
    Mengambil konten HTML dari URL yang diberikan dengan retry logic.
    Menggunakan error handling jika website down atau timeout.
    """
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, headers=HEADERS, timeout=timeout)
            response.raise_for_status()
            return response.text
        except requests.exceptions.Timeout:
            if attempt < max_retries:
                wait_time = 3 * attempt  # 3, 6, 9 seconds
                print(f"  ⏱️ Timeout (attempt {attempt}/{max_retries}), coba lagi dalam {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"Terjadi kesalahan ketika melakukan requests terhadap {url}: Timeout setelah {max_retries} attempts")
                return None
        except requests.exceptions.ConnectionError as e:
            if attempt < max_retries:
                wait_time = 3 * attempt
                print(f"  🔗 Connection error (attempt {attempt}/{max_retries}), coba lagi dalam {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"Terjadi kesalahan ketika melakukan requests terhadap {url}: {e}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Terjadi kesalahan ketika melakukan requests terhadap {url}: {e}")
            return None

def extract_fashion_data(card):
    """
    Mengekstrak detail produk dari satu elemen kartu (collection-card).
    Menggunakan try-except jika ada elemen yang hilang.
    """
    try:
        # Title
        title_elem = card.find('h3', class_='product-title')
        title = title_elem.text.strip() if title_elem else None

        # Price (bisa berada di span.price atau p.price)
        price_elem = card.find(class_='price')
        price = price_elem.text.strip() if price_elem else None

        # Rating, Colors, Size, Gender
        # Pada HTML, atribut ini disimpan berurutan dalam tag <p>
        p_tags = card.find_all('p')
        
        rating = None
        colors = None
        size = None
        gender = None

        # Memastikan ada cukup tag <p> sebelum mengekstrak teksnya
        if len(p_tags) >= 4:
            rating = p_tags[0].text.strip()
            colors = p_tags[1].text.strip()
            size = p_tags[2].text.strip()
            gender = p_tags[3].text.strip()

        # Menambahkan timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

        return {
            "Title": title,
            "Price": price,
            "Rating": rating,
            "Colors": colors,
            "Size": size,
            "Gender": gender,
            "timestamp": timestamp
        }
    
    except Exception as e:
        print(f"Terjadi kesalahan saat ekstrak data card: {e}")
        return None

def scrape_fashion(base_url, total_pages=50):
    """
    Fungsi utama untuk mengambil keseluruhan data fashion dengan delay strategy.
    """
    all_data = []
    
    try:
        for page in range(1, total_pages + 1):
            # Format URL pagination berdasarkan href di HTML
            if page == 1:
                url = base_url
            else:
                url = f"{base_url.rstrip('/')}/page{page}"
                
            print(f"Scraping halaman: {url}")
            
            html_content = fetching_product(url)
            if not html_content:
                continue
            
            soup = BeautifulSoup(html_content, "html.parser")
            
            # Mencari semua kontainer produk
            cards = soup.find_all('div', class_='collection-card')
            
            for card in cards:
                product_data = extract_fashion_data(card)
                if product_data:
                    all_data.append(product_data)
            
            # Adaptive delay: lebih lama kalau lebih banyak pages
            # Pertama 20 pages: 2 detik, page 21-40: 2.5 detik, page 41+: 3 detik
            if page <= 20:
                delay = 1.5
            elif page <= 40:
                delay = 2
            else:
                delay = 2.5
            
            time.sleep(delay)
            
        print(f"Scraping selesai, total data yang didapat: {len(all_data)}")
        return all_data
        
    except Exception as e:
        print(f"Terjadi kesalahan fatal pada proses scraping utama: {e}")
        return all_data