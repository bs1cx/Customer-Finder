# BusinessBot 🚀

**Google'dan Otomatik İşletme Verisi Toplama Aracı**  
Python ile geliştirilen bu GUI uygulaması, Google arama sonuçlarından işletme bilgilerini (ad, adres, telefon, kategori, website, sosyal medya) çıkararak Excel'e aktarır.


## 🔍 Özellikler
- **Çoklu Veri Kaynağı:** Google Maps ve standart arama sonuçlarını tarar
- **Detaylı Toplama:**  
  📌 İşletme adı  
  📌 Tam adres  
  📌 Telefon numarası  
  📌 Kategori/alan bilgisi  
  📌 Website linki  
  📌 Sosyal medya hesapları (Instagram/Facebook/Twitter)
- **Excel Entegrasyonu:** Tek tıkla `.xlsx` dosyasına aktarım
- **Anti-Ban:** Rastgele User-Agent döndürme ve request aralıkları

## 🛠 Kurulum
1. **Gereksinimler:**
   ```bash
   pip install requests beautifulsoup4 pandas tkinter

   python business_bot.py

   🎯 Kullanım
Arayüzde işletme türünü girin (Örn: "restoran", "kuaför")

Konum bilgisini ekleyin (Örn: "Kadıköy, İstanbul")

"İşletmeleri Bul" butonuna basın

Excel'e aktarmak için "Excel'e Aktar" butonunu kullanın

⚙️ Teknik Detaylar
Kullanılan Kütüphaneler:

python
import requests       # Web istekleri için
from bs4 import BeautifulSoup  # HTML parsing
import pandas as pd   # Excel işlemleri
import tkinter as tk  # GUI arayüzü
Regex Patternleri:

python
# Telefon numarası bulma:
r'(\+?\d[\d\s-]{7,}\d)'

# Sosyal medya çıkarma:
r'instagram\.com/([A-Za-z0-9_.]+)'
🌟 Proje Geliştirme
Katkıda bulunmak için:

Repoyu fork edin

Yeni özellik ekleyin (Örn: email çıkarma modülü)

Pull request açın

⚠️ Sorumluluk Reddi
Bu araç eğitim amaçlıdır. Google'ın ToS'unu ihlal etmemek için:

Tarama hızını düşük tutun (dk'da 5-10 istek)

Resmi API'leri tercih edin


