# Yemekhane Menü Mail Botu

Bu proje, Kocaeli Üniversitesi sosyal tesis yemek listesini her gün hafta içi saat 11:00'de belirttiğiniz e-posta adreslerine otomatik olarak gönderen bir Python uygulamasıdır.

## Özellikler

- Selenium ile yemek menüsünü çeker ve ay boyunca önbelleğe alır.
- Her gün (hafta içi) saat 11:00'de günün menüsünü mail olarak gönderir.
- Alıcı, gönderen ve şifre bilgileri `.env` dosyasından okunur.
- Gmail SMTP ile güvenli şekilde gönderim yapar.

## Kurulum

1. **Depoyu klonlayın veya indirin.**

2. **Gerekli Python paketlerini yükleyin:**
    ```
    pip install -r requirements.txt
    ```

3. **`.env` dosyasını oluşturun ve aşağıdaki gibi doldurun:**
    ```env
    EMAIL_USER="gonderen@gmail.com"
    EMAIL_PASSWORD="uygulama-sifresi"
    EMAIL_RECIPIENTS="mail1@example.com,mail2@example.com"
    ```

    > **Not:** Gmail için uygulama şifresi oluşturmanız gerekir. [Açıklama için tıklayın.](https://support.google.com/accounts/answer/185833?hl=tr)

4. **Programı başlatın:**
    ```
    python mail_gonderici.py
    ```

## Kullanım

- Program arka planda çalışır ve hafta içi her gün saat 11:00'de menüyü gönderir.
- Test için `mail_gonderici.py` dosyasındaki `yemek_maili_gonder()` fonksiyonunu elle çağırabilirsiniz.

## Notlar

- Bilgisayarınızın veya sunucunuzun açık olması gerekir.
- Ücretsiz olarak çalıştırmak için [PythonAnywhere](https://www.pythonanywhere.com/) veya [GitHub Actions](https://github.com/features/actions) gibi servisleri kullanabilirsiniz.
- Selenium ile çalıştığı için ChromeDriver ve ilgili bağımlılıkların yüklü olması gerekir.
