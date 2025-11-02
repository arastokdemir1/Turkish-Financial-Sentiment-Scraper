import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import sys

# =======================================================================
# BÖLÜM 1: TÜRKÇE FİNANSAL SÖZLÜK VE KELİMELER
# =======================================================================

# Duygu Skorlaması için Finansal Sözlük
FINANSAL_SOZLUK = {
    # POZİTİF DUYGU KELİMELERİ (+1)
    "yükseliş": 1, "artış": 1, "rekor": 1, "kazanç": 1, "fırsat": 1, "büyüme": 1, "kar": 1, "güçlü": 1, "yükseldi": 1,
    
    # NEGATİF DUYGU KELİMELERİ (-1)
    "düşüş": -1, "kayıp": -1, "çöküş": -1, "kriz": -1, "iflas": -1, "zarar": -1, "gerileme": -1, "tehlike": -1, "düştü": -1,
    
    # SİSTEM KELİMELERİ (NÖTR, Skorlamaya Etkisi Yok)
    "fiyatları": 0, "piyasada": 0, "son durum": 0, "haberi": 0, "gündem": 0
}

# Önyargı (Bias) Tespiti İçin Anahtar Kelimeler
ONYARGI_KELIMELERI = [
    "beklenti", "iddia", "tahmin", "söylenti", "analiz", 
    "spekülasyon", "potansiyel", "görüş", "uzman", "açıklaması"
]

# =======================================================================
# BÖLÜM 2: VERİ ÇEKME FONKSİYONU (Scraper)
# =======================================================================

def scrape_financial_news():
    """
    Dunya Gazetesi'nin finansal haber başlıklarını çeker.
    """
    url = "https://www.dunya.com/finans"
    # Basit header kullanmaya devam ediyoruz, çünkü bu çalışmıştı.
    headers = {'User-Agent': 'Mozilla/5.0'} 
    list1 = []

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() 
        soup = BeautifulSoup(response.content, "html.parser")

        # Sayfadaki tüm <a> etiketlerini çekerek haber başlıklarını filtrele
        all_links = soup.find_all("a")

        for link in all_links:
            list1.append(link.text.strip())
            
        # Boş girdileri, çok kısa metinleri ve alakasız metinleri temizle
        clean_list = [t for t in list1 if len(t) > 20 and 'Okumaya Devam Et' not in t and '\n' not in t]
        
        return clean_list

    except Exception as e:
        print(f"HATA: Veri çekme başarısız oldu. Detay: {e}")
        return []

# =======================================================================
# BÖLÜM 3: SKORLAMA SINIFI (FinancialScorer - Kütüphane Yapısı)
# =======================================================================

class FinancialScorer:
    """
    Türkçe finansal metinler için Duygu ve Önyargı (Bias) skorlamasını yapan ana sınıf.
    """
    
    def __init__(self, sentiment_lexicon, bias_keywords):
        self.sozluk = sentiment_lexicon
        self.onyargi_kelimeleri = bias_keywords
        
    def _analyze_text(self, text):
        """Metin için duygu ve önyargı skorlarını hesaplayan temel metod."""
        
        # Noktalama işaretlerini temizler ve küçük harfe çevirir.
        clean_text = re.sub(r'[^\w\s]', '', text.lower())
        words = clean_text.split()
        
        duygu_skoru = 0
        onyargi_skoru = 0
        
        for word in words:
            # Duygu Skorlaması
            if word in self.sozluk:
                duygu_skoru += self.sozluk[word]
                
            # Önyargı Skorlaması
            if word in self.onyargi_kelimeleri:
                onyargi_skoru += 1
                
        # Duygu skorunu normalize et (kelime sayısına böleriz)
        normalized_duygu = duygu_skoru / (len(words) if words else 1)
        
        return normalized_duygu, onyargi_skoru

    def score_titles(self, news_titles):
        """
        Haber başlıklarının listesini alır ve skorlanmış bir DataFrame döndürür.
        """
        turkish_results = []
        for title in news_titles:
            duygu, onyargi = self._analyze_text(title)
            
            turkish_results.append({
                "Baslik": title,
                "TR_Duygu_Skoru": duygu,
                "TR_Önyargı_Skoru": onyargi
            })
            
        sentiment_df = pd.DataFrame(turkish_results)
        
        # Duygu Etiketi Ekleme
        sentiment_df['Duygu Etiketi'] = sentiment_df['TR_Duygu_Skoru'].apply(
            lambda x: 'POZİTİF' if x > 0.0 else ('NEGATİF' if x < 0.0 else 'NÖTR')
        )
        
        # Önyargı Etiketi Ekleme (Skor 1 veya daha fazlaysa Yüksek Bias)
        sentiment_df['Önyargı Etiketi'] = sentiment_df['TR_Önyargı_Skoru'].apply(
            lambda x: 'YÜKSEK BİAS' if x >= 1 else 'DÜŞÜK BİAS'
        )
        
        return sentiment_df

# =======================================================================
# BÖLÜM 4: ANA ÇALIŞTIRMA BLOĞU
# =======================================================================

if __name__ == "__main__":
    
    # 1. Haber Başlıklarını Çekme
    news_titles = scrape_financial_news()
    
    if not news_titles:
        print("\n❌ Veri çekilemedi, analiz yapılamıyor.")
        sys.exit()

    print(f"\n✅ Çekilen {len(news_titles)} adet başlık analize hazır.")
    
    # 2. Scorer Sınıfını Başlatma
    scorer = FinancialScorer(FINANSAL_SOZLUK, ONYARGI_KELIMELERI)
    
    # 3. Skorlama işlemini yap
    final_df = scorer.score_titles(news_titles)
    
    print("\n--- NİHAİ FİNANSAL ANALİZ SONUÇLARI (Top 5) ---")
    # En pozitif ve önyargısı en yüksek olanları öne çıkarır.
    print(final_df.sort_values(by=['TR_Duygu_Skoru', 'TR_Önyargı_Skoru'], ascending=[False, False]).head())
    
    print("\n--- YÜKSEK BİAS (ÖNYARGI) İÇEREN BAŞLIKLAR ---")
    # Önyargı içeren başlıkları filtreler
    high_bias_df = final_df[final_df['Önyargı Etiketi'] == 'YÜKSEK BİAS']
    
    if high_bias_df.empty:
        print("Çekilen haberlerde belirlediğimiz spekülatif/önyargı kelimeleri bulunamadı.")
        print("Lütfen daha fazla önyargı kelimesi ekleyerek sözlüğü genişletin.")
    else:
        print(high_bias_df)

    print("\nPROJE 4: FİNANSAL SKORLAYICI BAŞARIYLA TAMAMLANDI!")