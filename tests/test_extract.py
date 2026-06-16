import pytest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from utils.extract import fetching_product, extract_fashion_data, scrape_fashion

# Test fetching_product berhasil
@patch('utils.extract.requests.get')
def test_fetching_product_success(mock_get):
    # Setup pemeran pengganti
    mock_response = MagicMock()
    mock_response.text = "<html>Sukses</html>"
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    # Jalankan fungsi
    result = fetching_product('http://test.com')
    
    # Memastikan hasilnya sesuai skenario
    assert result == "<html>Sukses</html>"

# Test fetching_product gagal (timeout/error)
@patch('utils.extract.requests.get')
def test_fetching_product_error(mock_get):
    # Membuat seolah-olah website down
    import requests
    mock_get.side_effect = requests.exceptions.RequestException("Error")
    
    result = fetching_product('http://test.com')
    assert result is None

# Test extract_fashion_data
def test_extract_fashion_data():
    html = """
    <div class="collection-card">
        <h3 class="product-title">Baju Keren</h3>
        <span class="price">$10.00</span>
        <p>Rating: ⭐ 4.5 / 5</p>
        <p>2 Colors</p>
        <p>Size: M</p>
        <p>Gender: Men</p>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    card = soup.find('div', class_='collection-card')
    
    result = extract_fashion_data(card)
    
    assert result['Title'] == "Baju Keren"
    assert result['Price'] == "$10.00"
    assert "timestamp" in result

# Test scrape_fashion 
@patch('utils.extract.fetching_product')
def test_scrape_fashion(mock_fetch):
    # Setup HTML palsu untuk di-scrape
    mock_fetch.return_value = """
    <div class="collection-card">
        <h3 class="product-title">Baju Dummy</h3>
    </div>
    """
    
    # Test 1 halaman 
    result = scrape_fashion("http://test.com", total_pages=1)
    
    assert len(result) == 1
    assert result[0]['Title'] == "Baju Dummy"

# Test scrape_fashion dengan halaman kosong
def test_extract_fashion_data_exception():
    # Membuat elemen HTML palsu yang akan error ketika dipanggil fungsi .find()
    mock_card = MagicMock()
    mock_card.find.side_effect = Exception("Sengaja bikin error di card")
    
    result = extract_fashion_data(mock_card)
    
    # Harus return None karena masuk ke blok except
    assert result is None