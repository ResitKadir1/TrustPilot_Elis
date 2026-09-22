import re
import time
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

print("Tarayıcı başlatılıyor ve güvenlik duvarı aşılıyor...")

# 1. Chrome Ayarlarını Yapılandırma
chrome_options = Options()
chrome_options.add_argument("--headless")  # Arka planda çalışması için
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# 2. Driver Başlatma
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

base_url = "https://dk.trustpilot.com/review/dk.elis.com/da"

reviews_list = []
current_page = 1

try:
    while True:
        page_url = f"{base_url}?page={current_page}"
        print(f"Sayfa {current_page} çekiliyor: {page_url}")

        driver.get(page_url)
        time.sleep(3)  # Sayfanın dinamik yüklenmesi için bekleme

        soup = BeautifulSoup(driver.page_source, "html.parser")
        articles = soup.find_all("article")

        if not articles:
            print("Bu sayfada yorum bulunamadı. Tarama tamamlandı.")
            break

        for article in articles:
            # Kullanıcı İsmi
            name_elem = article.find("span", {"data-consumer-name-typography": "true"}) or article.find("span",
                                                                                                        class_=lambda
                                                                                                            c: c and "consumer-name" in c)
            name = name_elem.get_text(strip=True) if name_elem else "Anonim"

            # --- Tarih ve Saat Formatlama (Gün.Ay.Yıl Saat:Dakika) ---
            time_elem = article.find("time")
            formatted_date = "-"
            if time_elem and time_elem.has_attr("datetime"):
                iso_date_str = time_elem["datetime"]
                try:
                    # ISO 8601 tarih formatını ayrıştırma (Örn: 2024-02-08T14:35:10.000Z)
                    dt_obj = datetime.strptime(iso_date_str.split(".")[0].replace("Z", ""), "%Y-%m-%dT%H:%M:%S")
                    formatted_date = dt_obj.strftime("%d.%m.%Y %H:%M")
                except Exception:
                    # Alternatif düz zaman okuma
                    formatted_date = iso_date_str[:10]

            # Yıldız Puanı
            rating = 0
            star_elem = article.find("div", {"data-service-review-rating": True})
            if star_elem and star_elem.get("data-service-review-rating"):
                rating = int(star_elem["data-service-review-rating"])
            else:
                rating_img = article.find("img",
                                          alt=lambda a: a and ("stjerne" in a.lower() or "stjerner" in a.lower()))
                if rating_img and rating_img.has_attr("alt"):
                    match = re.search(r'\d+', rating_img["alt"])
                    if match:
                        rating = int(match.group())

            # --- Yorum Metni (Müşterinin Yazdığı İçerik) ---
            review_body_elem = (
                    article.find("p", {"data-review-title-typography": "true"}) or
                    article.find("p", class_=lambda c: c and "review-content" in c) or
                    article.find("div", class_=lambda c: c and "reviewText" in c)
            )
            # Hem başlık hem açıklama varsa ikisini birleştirme
            text_elems = article.find_all(["h2", "p"], {"data-review-title-typography": "true"})
            if text_elems:
                review_text = " - ".join([t.get_text(strip=True) for t in text_elems])
            else:
                review_text = review_body_elem.get_text(strip=True) if review_body_elem else ""

            # Görsel URL (im_url)
            img_elem = article.find("img", class_=lambda c: c and "review-media" in c)
            im_url = img_elem["src"] if img_elem and img_elem.has_attr("src") else ""

            # --- Şirketin Yorum Yanıtı / Cevabı ---
            reply_elem = (
                    article.find("div", class_=lambda c: c and "reply" in c) or
                    article.find("p", {"data-owner-reply-text-typography": "true"}) or
                    article.find("div", class_=lambda c: c and "brand-reply" in c)
            )
            reply_text = reply_elem.get_text(strip=True) if reply_elem else ""

            reviews_list.append({
                "Isim": name,
                "Tarih_Saat": formatted_date,
                "Yildiz_Sayisi": rating,
                "Musteri_Yorumu": review_text,
                "IM_URL": im_url,
                "Sirket_Cevabi": reply_text
            })

        # Sonraki Sayfa Kontrolü
        next_button = soup.find("a", {"aria-label": "Næste side"}) or soup.find("a", {
            "data-pagination-button-next-link": "true"})
        if not next_button or next_button.get("aria-disabled") == "true":
            print("\nSon sayfaya ulaşıldı.")
            break

        current_page += 1

    # DataFrame Oluşturma ve Ortalama Puan Hesaplama
    df = pd.DataFrame(reviews_list)

    if not df.empty and "Yildiz_Sayisi" in df.columns:
        avg_rating = round(df["Yildiz_Sayisi"].mean(), 2)
    else:
        avg_rating = 0.0

    # En Alt Satıra Ortalama Puan Satırı Ekleme
    summary_row = {
        "Isim": "ORTALAMA / DEĞERLENDİRME",
        "Tarih_Saat": "-",
        "Yildiz_Sayisi": avg_rating,
        "Musteri_Yorumu": f"Toplam {len(df)} adet yorum incelendi.",
        "IM_URL": "-",
        "Sirket_Cevabi": "-"
    }

    df_final = pd.concat([df, pd.DataFrame([summary_row])], ignore_index=True)

    # CSV Olarak Kaydetme
    csv_filename = "trustpilot_elis_reviews.csv"
    df_final.to_csv(csv_filename, index=False, encoding="utf-8-sig")

    print(f"\n İşlem Tamamlandı! Toplam {len(df)} adet yorum çekildi.")
    print(f" Dosya oluşturuldu: {csv_filename}")

finally:
    driver.quit()