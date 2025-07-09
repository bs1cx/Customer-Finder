import requests
from bs4 import BeautifulSoup
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
import random
import re
from tkinter import filedialog

class BusinessBot:
    def __init__(self, root):
        self.root = root
        self.root.title("İşletme Bilgi Toplama Botu v4.0")
        self.root.geometry("1200x800")
        
        self.create_widgets()
        self.df = pd.DataFrame()
    
    def get_random_user_agent(self):
        agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'
        ]
        return random.choice(agents)
    
    def extract_phone(self, card):
        phone_elements = card.select('.UsdlK, .rllt__details div:nth-of-type(2), .rogA2c')
        for element in phone_elements:
            text = element.get_text(strip=True)
            if re.match(r'(\+?\d[\d\s-]{7,}\d)', text):
                return text
        return 'BULUNMUYOR'
    
    def extract_category(self, card):
        category_element = card.select_one('.YhemCb, .rllt__details div:nth-of-type(4)')
        return category_element.get_text(strip=True) if category_element else 'BULUNMUYOR'
    
    def extract_website(self, card):
        links = card.select('a[href*="http"]')
        for link in links:
            href = link.get('href', '')
            if 'google.com' not in href and 'maps.google' not in href:
                return href
        return 'BULUNMUYOR'
    
    def extract_social_media(self, card):
        social_media = []
        text = card.get_text()
        
        # Instagram
        instagram = re.search(r'instagram\.com/([A-Za-z0-9_.]+)', text)
        if instagram:
            social_media.append(f"Instagram: {instagram.group(1)}")
        
        # Facebook
        facebook = re.search(r'facebook\.com/([A-Za-z0-9_.]+)', text)
        if facebook:
            social_media.append(f"Facebook: {facebook.group(1)}")
        
        # Twitter
        twitter = re.search(r'twitter\.com/([A-Za-z0-9_.]+)', text)
        if twitter:
            social_media.append(f"Twitter: {twitter.group(1)}")
        
        return '\n'.join(social_media) if social_media else 'BULUNMUYOR'
    
    def create_widgets(self):
        # Arama Bölümü
        search_frame = ttk.LabelFrame(self.root, text="İşletme Arama")
        search_frame.pack(padx=15, pady=10, fill="x")
        
        ttk.Label(search_frame, text="İşletme Türü:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.query_entry = ttk.Entry(search_frame, width=40)
        self.query_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(search_frame, text="Konum:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.location_entry = ttk.Entry(search_frame, width=40)
        self.location_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(search_frame, text="İşletmeleri Bul", command=self.find_businesses).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Sonuçlar Bölümü
        results_frame = ttk.LabelFrame(self.root, text="Bulunan İşletmeler")
        results_frame.pack(padx=15, pady=10, fill="both", expand=True)
        
        columns = ("Name", "Address", "Category", "Phone", "Website", "SocialMedia")
        self.tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=20)
        
        # Sütun başlıkları
        self.tree.heading("Name", text="İşletme Adı")
        self.tree.heading("Address", text="Adres")
        self.tree.heading("Category", text="Alanı")
        self.tree.heading("Phone", text="Telefon No")
        self.tree.heading("Website", text="Web Sitesi")
        self.tree.heading("SocialMedia", text="Sosyal Medya")
        
        # Sütun genişlikleri
        self.tree.column("Name", width=200)
        self.tree.column("Address", width=250)
        self.tree.column("Category", width=150)
        self.tree.column("Phone", width=120)
        self.tree.column("Website", width=150)
        self.tree.column("SocialMedia", width=200)
        
        scrollbar_y = ttk.Scrollbar(results_frame, orient="vertical", command=self.tree.yview)
        scrollbar_y.pack(side="right", fill="y")
        
        scrollbar_x = ttk.Scrollbar(results_frame, orient="horizontal", command=self.tree.xview)
        scrollbar_x.pack(side="bottom", fill="x")
        
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        ttk.Button(results_frame, text="Excel'e Aktar", command=self.save_to_excel).pack(pady=5)
    
    def find_businesses(self):
        query = self.query_entry.get().strip()
        location = self.location_entry.get().strip()
        
        if not query or not location:
            messagebox.showerror("Hata", "Lütfen işletme türü ve konum bilgilerini giriniz")
            return
        
        try:
            # Önceki sonuçları temizle
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            self.df = pd.DataFrame(columns=[
                "İşletme Adı", "Adres", "Alanı", 
                "Telefon No", "Web Sitesi", "Sosyal Medya"
            ])
            
            url = f"https://www.google.com/search?q={query}+{location}&tbm=lcl"
            headers = {
                'User-Agent': self.get_random_user_agent(),
                'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Tüm işletme kartlarını bul
            business_cards = soup.select('.Nv2PK, .VkpGBb, .THOPZb')
            
            for card in business_cards:
                try:
                    name = card.select_one('.fontHeadlineSmall, .qBF1Pd, .dbg0pd').get_text(strip=True)
                    address = card.select_one('.W4Efsd:not(:has(span)), .rllt__details div:nth-of-type(3)').get_text(strip=True) if card.select_one('.W4Efsd:not(:has(span)), .rllt__details div:nth-of-type(3)') else 'BULUNMUYOR'
                    category = self.extract_category(card)
                    phone = self.extract_phone(card)
                    website = self.extract_website(card)
                    social_media = self.extract_social_media(card)
                    
                    self.tree.insert("", "end", values=(
                        name, address, category, 
                        phone, website, social_media
                    ))
                    
                    self.df.loc[len(self.df)] = [
                        name, address, category, 
                        phone, website, social_media
                    ]
                except Exception as e:
                    print(f"Kart işlenirken hata: {e}")
                    continue
            
            if len(self.df) == 0:
                messagebox.showwarning("Uyarı", "Hiç işletme bulunamadı. Lütfen şunları deneyin:\n\n1. Farklı arama terimleri kullanın\n2. Konumu daha genel yazın\n3. VPN kullanın")
            else:
                messagebox.showinfo("Başarılı", f"{len(self.df)} işletme bulundu")
        
        except Exception as e:
            messagebox.showerror("Hata", f"Arama sırasında hata oluştu:\n\n{str(e)}\n\nLütfen internet bağlantınızı kontrol edip tekrar deneyin")
    
    def save_to_excel(self):
        if self.df.empty:
            messagebox.showerror("Hata", "Kaydedilecek işletme bulunamadı")
            return
        
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                title="Excel dosyasını kaydet"
            )
            
            if file_path:
                self.df.to_excel(file_path, index=False)
                messagebox.showinfo("Başarılı", f"İşletmeler başarıyla kaydedildi:\n\n{file_path}")
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya kaydedilirken hata:\n\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BusinessBot(root)
    root.mainloop()