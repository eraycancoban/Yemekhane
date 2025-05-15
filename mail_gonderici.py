import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import time
from datetime import datetime
import os
from dotenv import load_dotenv
from main import bugunun_yemek_listesini_getir

def mail_gonder(kime_listesi, konu, icerik, gonderen_mail, gonderen_sifre):
    """
    Belirtilen alıcılara mail gönderen fonksiyon
    """
    # MIME mesajı oluştur
    mesaj = MIMEMultipart('alternative')
    mesaj['Subject'] = konu
    mesaj['From'] = gonderen_mail
    mesaj['To'] = ", ".join(kime_listesi)
    
    # HTML içerik ekle
    html_icerik = f"""
    <html>
    <head></head>
    <body>
        <pre style="font-family: monospace; white-space: pre-wrap;">{icerik}</pre>
    </body>
    </html>
    """
    mesaj.attach(MIMEText(html_icerik, 'html'))
    
    # SMTP sunucuya bağlan ve gönder
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(gonderen_mail, gonderen_sifre)
        server.sendmail(gonderen_mail, kime_listesi, mesaj.as_string())
        server.close()
        print(f"Mail başarıyla gönderildi: {datetime.now()}")
        return True
    except Exception as e:
        print(f"Mail gönderilirken hata oluştu: {e}")
        return False

def yemek_maili_gonder():
    """
    Bugünün yemek listesini mail olarak gönder
    """
    # Bugün iş günü mü kontrol et (0=Pazartesi, 6=Pazar)
    bugun = datetime.now().weekday()
    if bugun >= 5:  # Cumartesi veya Pazar
        print("Bugün hafta sonu, mail gönderilmiyor.")
        return
    
    # Yemek listesini al
    url = "https://sksdb.kocaeli.edu.tr/en/sayfalar/sosyal-tesis-yemek-listesi-14e"
    bugunun_yemegi = bugunun_yemek_listesini_getir(url)
    
    # Mail içeriğini oluştur
    bugun_tarih = datetime.now().strftime("%d.%m.%Y")
    konu = f"Yemek Listesi - {bugun_tarih}"
    
    # Mail gönder
    # .env dosyasından mail bilgilerini al
    
    # .env dosyasını yükle
    load_dotenv()
    
    # Çevre değişkenlerini al
    gonderen_mail = os.environ.get("EMAIL_USER")
    gonderen_sifre = os.environ.get("EMAIL_PASSWORD")
    
    # Mail listesini string olarak alıp listeye çevir
    mail_listesi_str = os.environ.get("EMAIL_RECIPIENTS")
    mail_listesi = [email.strip() for email in mail_listesi_str.split(",")] if mail_listesi_str else []
    
    if not gonderen_mail or not gonderen_sifre or not mail_listesi:
        print("Mail bilgileri eksik. Lütfen .env dosyasını kontrol edin.")
        return
    
    mail_gonder(mail_listesi, konu, bugunun_yemegi, gonderen_mail, gonderen_sifre)

# Her gün saat 10:00'da çalıştır
schedule.every().day.at("11:00").do(yemek_maili_gonder)

if __name__ == "__main__":
    print("Yemek listesi mail gönderici başlatıldı...")
    print("Hafta içi her gün 10:00'da mail gönderilecek")
    
    # İlk çalıştırmada test olarak bir mail gönder (opsiyonel)
    # yemek_maili_gonder()
    
    # Zamanlayıcıyı sürekli kontrol et
    while True:
        schedule.run_pending()
        time.sleep(60)  # 1 dakikada bir kontrol et