<div align="center">

# ⚡ Discord Username Checker

  <p><b>Advanced Visual Color-Detection & Automated Username Sniper</b></p>
  
  <p>
    <img src="https://img.shields.io/badge/Version-UCv1.4.0--stable-blue?style=for-the-badge&logo=discord" alt="Version">
    <img src="https://img.shields.io/badge/Python-3.6%2B-yellow?style=for-the-badge&logo=python" alt="Python">
    <img src="https://img.shields.io/badge/Platform-Windows-lightgrey?style=for-the-badge&logo=windows" alt="Windows">
    <img src="https://img.shields.io/badge/License-KZI-purple?style=for-the-badge" alt="License">
  </p>
</div>



## 🚀 Genel Bakış

**Discord Username Checker**, Discord arayüzündeki kullanıcı adı müsaitlik durumunu gelişmiş renk algılama (color detection) teknolojisiyle otomatik olarak denetleyen güçlü bir araçtır. Durum alanını takip etmek için sınırsız/çerçevesiz bir görsel katman (overlay) oluşturur ve boştaki kullanıcı adlarını anında yakalamanızı sağlar.

---

## ✨ Özellikler

* **Çift Modlu Denetim (Dual-Mode):**
  * **File Sniper:** `words.txt` dosyasındaki kelime listesini sırasıyla Discord'un kullanıcı adı alanına yazar.
  * **Random Sniper:** Otomatik olarak rastgele 3-4 haneli kullanıcı adları üretir ve dener.
* **Görsel Algılama Sistemi:** Başarı (yeşil) ve hata (kırmızı) mesajlarını piksel analizleriyle kusursuz şekilde ayırt eder.
* **Canlı Border Overlay:** Hangi alanın taranmakta olduğunu renkli bir çerçeveyle tam zamanlı gösterir.
* **Anlık Discord Bildirimleri:** Boşta bir kullanıcı adı yakalandığında webhook aracılığıyla detaylı gömülü (embed) bildirimler gönderir.
* **Akıllı Girdi Yönetimi:** Denemeler arasında input alanını otomatik olarak temizler ve optimize eder.

---

## 🛠️ Gereksinimler

* **Python 3.6+**
* **Windows İşletim Sistemi** (Pencere yönetimi için Win32 API kullanır)
* Aktif bir Discord hesabı ve Webhook URL'si (Bildirimler için)

---

## 📦 Kurulum

1. **Repoyu klonlayın:**
   ```bash
   git clone [https://github.com/kzixc/UsernameChecker.git](https://github.com/kzixc/UsernameChecker.git)
   cd UsernameChecker
Bağımlılıkları yükleyin:

Bash
pip install -r requirements.txt
Wordlist oluşturun (File Sniper modu için):

Proje dizinine words.txt adında bir dosya oluşturun ve her satıra bir kullanıcı adı yazın.

🎮 Kullanım
Komut satırından betiği çalıştırın veya .bat dosyasını kullanın:

Bash
python random_word_typer.py
Veya hazır betik ile: run.bat

Sniper modunuzu seçin:

1) File Sniper (words.txt kullanır)

2) Random Sniper (Rastgele 3-4 harfli kombinasyonlar üretir)

Discord Odaklanma Aşaması:

Discord'un kullanıcı adı değiştirme ekranına gelin.

Betik size odaklanmanız için 10 saniye süre tanıyacaktır.

Algılama alanı renkli bir çerçeveyle vurgulanacaktır.

Durdurma: İşlemi istediğiniz an sonlandırmak için klavyeden ESC tuşuna basabilirsiniz.

⚙️ Yapılandırma ve Optimizasyon
Çözünürlük Ayarları
Eğer algılama kutusu ekranınızda doğru konumda değilse, random_word_typer.py içindeki RESOLUTION_POSITIONS sözlüğünü ekran çözünürlüğünüze göre güncelleyebilirsiniz:

Python
RESOLUTION_POSITIONS = {
    "2560x1440": {
        "box_width": 410,
        "box_height": 45,
        "box_y_ratio": 0.479
    },
    # Kendi çözünürlüğünüzü buraya ekleyebilirsiniz
}
Renk Hassasiyeti (color_detector_visual.py)
Tespit sorunları yaşıyorsanız color_detector_visual.py dosyasından renk mesafesi eşiklerini (color distance thresholds) ayarlayabilir, başarı/hata algılama toleranslarını özelleştirebilirsiniz.

📝 Lisans
Bu proje KZI License terms şartları altında korunmaktadır.
