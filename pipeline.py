import subprocess
import sys
import time

def run_step(step_name, command):
    print(f"\n==========================================")
    print(f"🚀 BAŞLATILIYOR: {step_name}")
    print(f"==========================================")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"❌ {step_name} ADIMINDA HATA OLUŞTU!")
        sys.exit(1)
    print(f"✅ {step_name} BAŞARIYLA TAMAMLANDI.")

if __name__ == "__main__":
    # 1. Adım: Veri Kazıma (Scraping)
    run_step("1. Veri Kazıma (Scraper)", f"{sys.executable} scraper.py")

    # 2. Adım: NLP ve Problem Tespiti Analizi
    run_step("2. Şikayet ve Problem Analizi", f"{sys.executable} analyzer.py")

    # 3. Adım: Streamlit Dashboard Başlatma
    print("\n==========================================")
    print("📊 3. Streamlit Dashboard Başlatılıyor...")
    print("==========================================")
    subprocess.run(f"{sys.executable} -m streamlit run dashboard.py", shell=True)