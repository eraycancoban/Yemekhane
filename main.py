from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from datetime import datetime
import pickle
from bs4 import BeautifulSoup

def sayfayi_render_et_ve_html_al(url):
    # Başsız tarayıcı (ekran açılmaz)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # WebDriver başlat
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        driver.get(url)

        # Sayfanın tamamen yüklenmesi için birkaç saniye bekle
        time.sleep(3)

        # Sayfanın tam HTML içeriğini al
        html = driver.page_source
        return html
    finally:
        driver.quit()

def yemek_listesi_getir(url):
    # Mevcut ay ve yıl bilgisini al
    simdiki_zaman = datetime.now()
    ay_yil = f"{simdiki_zaman.year}_{simdiki_zaman.month}"
    
    # Kaydedilecek dosya adı
    dosya_adi = f"yemek_listesi_{ay_yil}.pkl"
    
    # Eğer aynı ay için daha önce çekilmiş veri varsa, onu kullan
    if os.path.exists(dosya_adi):
        print(f"Kaydedilmiş veri bulundu: {dosya_adi}")
        with open(dosya_adi, 'rb') as dosya:
            html_icerik = pickle.load(dosya)
    else:
        print(f"Yeni ay için veri çekiliyor: {ay_yil}")
        # Veri çek
        html_icerik = sayfayi_render_et_ve_html_al(url)
        
        # Veriyi kaydet
        with open(dosya_adi, 'wb') as dosya:
            pickle.dump(html_icerik, dosya)
    
    return html_icerik

def bugunun_yemek_listesini_getir(url):
    """
    Bugüne ait yemek listesini okunaklı bir şekilde döndüren fonksiyon
    Her gün için iki satır (tr) içeren HTML yapısını düzgün şekilde işler
    """
    html_icerik = yemek_listesi_getir(url)
    soup = BeautifulSoup(html_icerik, "html.parser")
    
    # Tabloyu seç
    tablo = soup.find("table")
    if not tablo:
        return "Yemek listesi tablosuna erişilemedi."
    
    # Bugünün tarihi
    bugun = datetime.now()
    bugun_gun = bugun.day
    
    # Tablo satırlarını al
    satirlar = tablo.find_all("tr")
    
    # İlk 4 satır başlık, onları atla
    i = 4
    while i < len(satirlar) - 1:  # İki satırı birlikte işleyeceğimiz için -1
        # İlk satır ana yemekleri içerir
        ana_satir = satirlar[i]
        ana_hucreler = ana_satir.find_all("td")
        
        if len(ana_hucreler) < 2:
            i += 1
            continue
            
        # İlk hücre tarih bilgisini içerir
        tarih_hucresi = ana_hucreler[0]
        
        # div içindeki tarih bilgisini al
        tarih_div = tarih_hucresi.find('div')
        if tarih_div:
            tarih_metni = tarih_div.get_text().strip()
        else:
            tarih_metni = tarih_hucresi.text.strip()
            
        # Tarih metnini işle (örn: "05.05.2025\n     Pazartesi")
        tarih_parcalari = tarih_metni.split('.')
        if len(tarih_parcalari) >= 2:
            try:
                gun = int(tarih_parcalari[0])
                
                # Bugünün günüyle eşleşiyorsa
                if gun == bugun_gun:
                    # Yemekleri ve kalorileri topla
                    yemekler = []
                    kaloriler = []
                    
                    # İlk satırdaki yemekleri al
                    j = 1
                    while j < len(ana_hucreler):
                        # Yemek hücresi
                        yemek_hucresi = ana_hucreler[j]
                        yemek_div = yemek_hucresi.find('div')
                        
                        if yemek_div and yemek_div.text.strip() and not yemek_div.text.strip().isdigit():
                            yemek = yemek_div.text.strip()
                            yemekler.append(yemek)
                            
                            # Kalori hücresi genellikle yemek hücresinden sonra gelir
                            if j+1 < len(ana_hucreler):
                                kalori_hucresi = ana_hucreler[j+1]
                                kalori_div = kalori_hucresi.find('div')
                                
                                if kalori_div and kalori_div.text.strip().isdigit():
                                    kalori = kalori_div.text.strip()
                                    kaloriler.append(kalori)
                                    j += 2  # Yemek ve kalori hücresini atla
                                else:
                                    kaloriler.append("?")
                                    j += 1
                            else:
                                kaloriler.append("?")
                                j += 1
                        else:
                            j += 1
                    
                    # İkinci satırdaki (varsa) ek yemekleri al
                    if i + 1 < len(satirlar):
                        ek_satir = satirlar[i + 1]
                        ek_hucreler = ek_satir.find_all("td")
                        
                        j = 0
                        while j < len(ek_hucreler):
                            # Yemek hücresi
                            yemek_hucresi = ek_hucreler[j]
                            yemek_div = yemek_hucresi.find('div')
                            
                            if yemek_div and yemek_div.text.strip() and not yemek_div.text.strip().isdigit():
                                yemek = yemek_div.text.strip()
                                yemekler.append(yemek)
                                
                                # Kalori hücresi
                                if j+1 < len(ek_hucreler):
                                    kalori_hucresi = ek_hucreler[j+1]
                                    kalori_div = kalori_hucresi.find('div')
                                    
                                    if kalori_div and kalori_div.text.strip().isdigit():
                                        kalori = kalori_div.text.strip()
                                        kaloriler.append(kalori)
                                        j += 2  # Yemek ve kalori hücresini atla
                                    else:
                                        kaloriler.append("?")
                                        j += 1
                                else:
                                    kaloriler.append("?")
                                    j += 1
                            else:
                                j += 1
                    
                    # Sonucu formatla - tarih metnini düzgün şekilde göster
                    sonuc = f"📅 {tarih_metni.replace('\n', ' - ')} 📅\n"
                    sonuc += "=" * 40 + "\n"
                    
                    # Yemekleri kategorilere ayır ve kalorilerle birlikte göster
                    yemek_kategorileri = ["Çorba", "Ana Yemek", "Yardımcı Yemek", "İçecek/Tatlı"]
                    emojiler = ["🍲", "🍖", "🥗", "🥤"]
                    
                    for idx, (yemek, kalori) in enumerate(zip(yemekler, kaloriler)):
                        if idx < len(yemek_kategorileri):
                            kategori = yemek_kategorileri[idx]
                            emoji = emojiler[idx]
                            sonuc += f"{emoji} {kategori}: {yemek} ({kalori} kcal)\n"
                        else:
                            sonuc += f"📋 Ek Yemek: {yemek} ({kalori} kcal)\n"
                    
                    sonuc += "=" * 40
                    return sonuc
            except (ValueError, IndexError) as e:
                pass
                
        # Her iki satırı (ana ve ek yemekler) birlikte işlediğimiz için 2 arttır
        i += 2
    
    return "Bugüne ait yemek bilgisi bulunamadı."

# Kullanım örneği
if __name__ == "__main__":
    url = "https://sksdb.kocaeli.edu.tr/en/sayfalar/sosyal-tesis-yemek-listesi-14e"
    bugunun_yemegi = bugunun_yemek_listesini_getir(url)
    print(bugunun_yemegi)