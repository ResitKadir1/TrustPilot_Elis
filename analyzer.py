import pandas as pd


def detect_problem_category(text):
    if not isinstance(text, str) or not text.strip():
        return "Belirtilmedi / Cevap Yok"

    text_lower = text.lower()
    if any(k in text_lower for k in ["gecikme", "fatura", "teslimat", "hata", "delay", "invoice", "fejl", "regning"]):
        return "Operasyonel / Fatura Problemi"
    elif any(
            k in text_lower for k in ["kalite", "hasar", "bozuk", "servis", "quality", "damaged", "dårlig", "service"]):
        return "Ürün / Hizmet Kalitesi"
    elif any(k in text_lower for k in ["iletişim", "telefon", "yanıt", "destek", "kontakt", "svar"]):
        return "Müşteri İletişim Aksaklığı"
    else:
        return "Diğer / Genel Yanıt"


try:
    # 1. CSV Yükleme
    csv_file = "trustpilot_elis_reviews.csv"
    df_reviews = pd.read_csv(csv_file)

    # 2. Sütun Adı Kontrolü ve Esneklik Sağlama
    if "Sirket_Cevabi" in df_reviews.columns and "Cevap" not in df_reviews.columns:
        df_reviews.rename(columns={"Sirket_Cevabi": "Cevap"}, inplace=True)

    # 3. Müşteri Yorumu Üzerinden Problem Tespiti
    if "Musteri_Yorumu" in df_reviews.columns:
        df_reviews["Tespit_Edilen_Problem"] = df_reviews["Musteri_Yorumu"].apply(detect_problem_category)
    elif "Cevap" in df_reviews.columns:
        df_reviews["Tespit_Edilen_Problem"] = df_reviews["Cevap"].apply(detect_problem_category)

    # 4. Sonuçları Ekrana Yazdırma ve Yeni CSV Oluşturma
    print("--- ANALİZ SONUÇLARI ---")
    print(df_reviews[["Isim", "Yildiz_Sayisi", "Tespit_Edilen_Problem"]].head(10))

    output_file = "trustpilot_elis_analyzed.csv"
    df_reviews.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"\nAnaliz tamamlandı. Sonuçlar '{output_file}' dosyasına kaydedildi.")

except FileNotFoundError:
    print(f"Hata: '{csv_file}' bulunamadı. Lütfen önce 'elis2.py' kodunu çalıştırın.")
except Exception as e:
    print(f"Analiz sırasında beklenmeyen bir hata oluştu: {e}")