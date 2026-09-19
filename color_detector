"""
KZI - Renk Algılama Modülü
Sürüm: UCv1.4.0-stable
(Çalışan kararlı sürüm, bozmayalım lütfen)
"""

import pyautogui
import numpy as np
import time
import tkinter as tk
import keyboard
from PIL import Image
import colorsys
import os  # Konsolu temizlemek için lazım oluyor

# Discord mesaj renklerini buraya koyduk
DISCORD_HATA_RENGI = (237, 66, 69)     # Kırmızı hata yazısı
DISCORD_BASARI_RENGI = (87, 242, 135)  # Yeşil başarı yazısı
DISCORD_UYARI_RENGI = (254, 231, 92)   # Sarı uyarı yazısı

# Discord arayüzünde sık kullanılan renkler
DISCORD_MOR = (88, 101, 242)     # Discord'un kendi moru (blurple)
DISCORD_KOYU_MOR = (78, 93, 148) # Koyu tema mor tonu

# Ekrandan yakaladığımız özel renkler
DISCORD_MUSAIT_YESIL = (40, 92, 54)  # "Kullanıcı adı müsait" yazısının yeşili
DISCORD_UI_GRI = (60, 60, 65)        # Arayüzdeki gri yazılar

# Kullanımda olan adlar için kırmızı tonları
DISCORD_KULLANIMDA_KIRMIZI = (237, 66, 69)  
DISCORD_HATA_METNI_KIRMIZI = (229, 57, 53)   

# Genişlettiğimiz kırmızı tonları listesi
KIRMIZI_RENKLER = [
    DISCORD_HATA_RENGI,
    DISCORD_KULLANIMDA_KIRMIZI,
    DISCORD_HATA_METNI_KIRMIZI,
    (0xaa, 0x58, 0x57),
    (0x6a, 0x3a, 0x3a),
    (0xeb, 0x75, 0x71),
    (0x97, 0x4f, 0x4e),
    (0xbc, 0x61, 0x5f),
    (106, 81, 107),
    (186, 106, 143),
    (186, 81, 107),
    (255, 99, 71),
    (240, 128, 128),
    (205, 92, 92),
    (220, 20, 60),
    (189, 5, 6)
]

# Yeşil renklerin listesi (daha stabil çalışması için elden geçirildi)
YESIL_RENKLER = [
    DISCORD_BASARI_RENGI,
    DISCORD_MUSAIT_YESIL,
    (0x39, 0x96, 0x51),
    (0x33, 0x7e, 0x46),
    (46, 204, 113),
    (80, 220, 100),
    (118, 172, 63),
    (47, 114, 65),
    (49, 122, 69),
    (59, 157, 84),
    (57, 151, 81),
    (58, 155, 83),
    (53, 140, 76),
    (60, 179, 113),
    (46, 139, 87),
    (143, 188, 143),
    (152, 251, 152)
]

# Sarı renklerin listesi
SARI_RENKLER = [
    DISCORD_UYARI_RENGI,
    (76, 76, 22),
    (77, 73, 20),
    (79, 79, 25),
    (255, 255, 0),
    (255, 215, 0),
    (255, 165, 0),
    (255, 140, 0),
    (255, 191, 0),
    (240, 230, 140),
    (250, 250, 210),
    (238, 232, 170),
    (255, 222, 173),
    (254, 231, 92),
    (241, 196, 15),
    (248, 148, 6)
]

# Çerçeve için dikkat çeken morumsu renk (mesajlarla karışmasın diye)
KENAR_RENGI = "#8A2BE2"

# Arayüz öğelerini ayırt etmek için renkler
UI_RENKLERI = [
    DISCORD_MOR,
    DISCORD_KOYU_MOR,
    DISCORD_UI_GRI,
    (53, 54, 56),
    (41, 28, 54),
    (37, 27, 53),
    (72, 73, 75),
    (56, 57, 60),
    (79, 84, 92),
    (114, 137, 218),
    (153, 170, 181),
    (220, 221, 222)
]

class BasitKenar:
    """İzlenen alanın etrafına renkli çerçeve çizen ufak sınıf"""
    def __init__(self, x, y, genislik, yukseklik, kenar_kalinligi=2):
        self.x = x
        self.y = y
        self.genislik = genislik
        self.yukseklik = yukseklik
        self.kalinlik = kenar_kalinligi
        self.pencereler = []
        self._pencereleri_olustur()
    
    def _pencereleri_olustur(self):
        # Çerçevenin dört kenarı için şefffsiz/çerçevesiz pencereler açıyoruz
        
        # Üst kenar
        ust = tk.Tk()
        ust.title("")
        ust.overrideredirect(True)
        ust.configure(background=KENAR_RENGI)
        ust.geometry(f"{self.genislik}x{self.kalinlik}+{self.x}+{self.y}")
        ust.attributes('-topmost', True)
        ust.attributes('-alpha', 1.0)
        ust.wm_attributes("-topmost", 1)
        ust.focus_set()
        ust.focus_force()
        ust.lift()
        self.pencereler.append(ust)
        
        # Alt kenar
        alt = tk.Toplevel()
        alt.title("")
        alt.overrideredirect(True)
        alt.configure(background=KENAR_RENGI)
        alt.geometry(f"{self.genislik}x{self.kalinlik}+{self.x}+{self.y+self.yukseklik-self.kalinlik}")
        alt.attributes('-topmost', True)
        alt.attributes('-alpha', 1.0)
        alt.lift()
        self.pencereler.append(alt)
        
        # Sol kenar
        sol = tk.Toplevel()
        sol.title("")
        sol.overrideredirect(True)
        sol.configure(background=KENAR_RENGI)
        sol.geometry(f"{self.kalinlik}x{self.yukseklik}+{self.x}+{self.y}")
        sol.attributes('-topmost', True)
        sol.attributes('-alpha', 1.0)
        sol.lift()
        self.pencereler.append(sol)
        
        # Sağ kenar
        sag = tk.Toplevel()
        sag.title("")
        sag.overrideredirect(True)
        sag.configure(background=KENAR_RENGI)
        sag.geometry(f"{self.kalinlik}x{self.yukseklik}+{self.x+self.genislik-self.kalinlik}+{self.y}")
        sag.attributes('-topmost', True)
        sag.attributes('-alpha', 1.0)
        sag.lift()
        self.pencereler.append(sag)
        
        for pencere in self.pencereler:
            pencere.update()
        
        pencereleri_en_uste_zorla(self.pencereler)
    
    def guncelle(self):
        """Çerçevenin her zaman en üstte kalmasını sağlıyoruz"""
        for pencere in self.pencereler:
            try:
                pencere.attributes('-topmost', True)
                pencere.lift()
                pencere.update()
            except:
                pass
        
        pencereleri_en_uste_zorla(self.pencereler)
    
    def yok_et(self):
        """İşim bittiğinde pencereleri kapatıyorum"""
        try:
            import win32gui
            import win32con
            for pencere in self.pencereler:
                if hasattr(pencere, 'winfo_id'):
                    try:
                        hwnd = win32gui.GetParent(pencere.winfo_id())
                        win32gui.SetWindowPos(
                            hwnd,
                            win32con.HWND_NOTOPMOST,
                            0, 0, 0, 0,
                            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE
                        )
                    except:
                        pass
        except:
            pass
            
        for pencere in self.pencereler:
            try:
                pencere.destroy()
            except:
                pass
                
        self.pencereler = []

def kutu_rengini_al(x, y, genislik, yukseklik):
    """Belirtilen alanın ortalama rengini hesaplar"""
    ekran_goruntusu = pyautogui.screenshot(region=(x, y, genislik, yukseklik))
    img_dizi = np.array(ekran_goruntusu)
    ortalama_renk = np.mean(img_dizi, axis=(0, 1))
    return tuple(map(int, ortalama_renk))

def koyu_arkaplan_mi(renk, esik=50):
    """Arka planın koyu olup olmadığını anlamak için"""
    return sum(renk) < esik * 3

def parlak_renk_mi(renk, esik=100):
    """Renk yeterince parlak mı diye bakar"""
    return any(c > esik for c in renk)

def doygunlugu_al(renk):
    """Rengin doygunluk oranını verir"""
    r, g, b = [c/255.0 for c in renk]
    if max(r, g, b) == 0:
        return 0
    _, doygunluk, _ = colorsys.rgb_to_hsv(r, g, b)
    return doygunluk

def kenar_rengi_mi(renk, kenar_rgb=(138, 43, 226), esik=50):
    """Kendi çizdiğimiz çerçeve rengi mi diye kontrol eder (karışmasın diye)"""
    r_fark = abs(renk[0] - kenar_rgb[0])
    g_fark = abs(renk[1] - kenar_rgb[1])
    b_fark = abs(renk[2] - kenar_rgb[2])
    return sum([r_fark, g_fark, b_fark]) < esik

def metin_renklerini_bul(x, y, genislik, yukseklik):
    """Ekrandaki yazı renklerini yakalamaya yarayan ana fonksiyon"""
    ekran_goruntusu = pyautogui.screenshot(region=(x, y, genislik, yukseklik))
    img_dizi = np.array(ekran_goruntusu)
    
    # Önce hata kırmızısı var mı diye piksel piksel tarayalım
    for i in range(img_dizi.shape[0]):
        for j in range(img_dizi.shape[1]):
            piksel = img_dizi[i, j]
            piksel_demeti = tuple(piksel)
            
            if renk_mesafesi(piksel_demeti, DISCORD_HATA_RENGI) < 30:
                return [DISCORD_HATA_RENGI]
                
            if renk_mesafesi(piksel_demeti, DISCORD_KULLANIMDA_KIRMIZI) < 30:
                return [DISCORD_KULLANIMDA_KIRMIZI]
                
            if renk_mesafesi(piksel_demeti, DISCORD_HATA_METNI_KIRMIZI) < 30:
                return [DISCORD_HATA_METNI_KIRMIZI]
    
    # Hafif kırmızımsı pikselleri yakala
    for i in range(img_dizi.shape[0]):
        for j in range(img_dizi.shape[1]):
            piksel = img_dizi[i, j]
            if piksel[0] > 120 and piksel[0] > piksel[1] * 1.5 and piksel[0] > piksel[2] * 1.5:
                return [tuple(piksel)]
    
    # Başarı yeşillerini ve uyarı sarılarını kontrol et
    for i in range(img_dizi.shape[0]):
        for j in range(img_dizi.shape[1]):
            piksel = img_dizi[i, j]
            piksel_demeti = tuple(piksel)
            
            if renk_mesafesi(piksel_demeti, DISCORD_BASARI_RENGI) < 30:
                return [DISCORD_BASARI_RENGI]
            if renk_mesafesi(piksel_demeti, DISCORD_UYARI_RENGI) < 30:
                return [DISCORD_UYARI_RENGI]
            if renk_mesafesi(piksel_demeti, DISCORD_MUSAIT_YESIL) < 20:
                return [DISCORD_MUSAIT_YESIL]
            
            for arayuz_rengi in UI_RENKLERI[:5]:
                if renk_mesafesi(piksel_demeti, arayuz_rengi) < 20:
                    return [arayuz_rengi]
    
    pikseller = img_dizi.reshape(-1, 3)
    benzersiz_renkler, sayimlar = np.unique(pikseller, axis=0, return_counts=True)
    renk_ciftleri = [(tuple(renk), sayi) for renk, sayi in zip(benzersiz_renkler, sayimlar)]
    renk_ciftleri.sort(key=lambda x: x[1], reverse=True)
    
    arkaplan_rengi = renk_ciftleri[0][0] if renk_ciftleri else (0, 0, 0)
    metin_adaylari = []
    
    toplam_piksel = sum(sayimlar)
    for renk, sayi in renk_ciftleri:
        if renk == arkaplan_rengi:
            continue
        if kenar_rengi_mi(renk):
            continue
        if renk_mesafesi(renk, arkaplan_rengi) < 30:
            continue
        
        muhtemelen_kirmizi = False
        for kirmizi_renk in KIRMIZI_RENKLER[:5]:
            if renk_mesafesi(renk, kirmizi_renk) < 50:
                muhtemelen_kirmizi = True
                metin_adaylari.append((renk, sayi))
                break
                
        if muhtemelen_kirmizi:
            continue
            
        muhtemelen_yesil = False
        for yesil_renk in YESIL_RENKLER:
            if renk_mesafesi(renk, yesil_renk) < 40:
                muhtemelen_yesil = True
                metin_adaylari.append((renk, sayi))
                break
                
        if muhtemelen_yesil:
            continue
            
        if koyu_arkaplan_mi(arkaplan_rengi) and koyu_arkaplan_mi(renk):
            continue
            
        doygunluk = doygunlugu_al(renk)
        if doygunluk < 0.1:
            continue
            
        frekans = sayi / toplam_piksel
        if 0.0005 < frekans < 0.5:
            metin_adaylari.append((renk, sayi))
    
    if not metin_adaylari:
        for renk, sayi in renk_ciftleri:
            if renk != arkaplan_rengi and not kenar_rengi_mi(renk) and sayi / toplam_piksel < 0.6:
                arayuz_rengi_mi = False
                for arayuz_rengi in UI_RENKLERI:
                    if renk_mesafesi(renk, arayuz_rengi) < 40:
                        arayuz_rengi_mi = True
                        metin_adaylari.append((renk, sayi))
                        break
                if not arayuz_rengi_mi:
                    metin_adaylari.append((renk, sayi))
    
    return [renk for renk, _ in metin_adaylari]

def baskin_metin_rengini_al(x, y, genislik, yukseklik):
    """Bölgedeki en belirgin rengi bulup ne olduğunu (RED/GREEN vs.) döndürür"""
    metin_renkleri = metin_renklerini_bul(x, y, genislik, yukseklik)
    
    if metin_renkleri:
        for renk in metin_renkleri:
            if renk in KIRMIZI_RENKLER or any(renk_yakin_mi(renk, k) for k in KIRMIZI_RENKLER):
                return "RED", renk
            if renk in YESIL_RENKLER or any(renk_yakin_mi(renk, y_) for y_ in YESIL_RENKLER):
                return "GREEN", renk
            if renk in SARI_RENKLER or any(renk_yakin_mi(renk, s) for s in SARI_RENKLER):
                return "YELLOW", renk
    
    sonuc = renk_eslesmelerini_kontrol_et(kutu_rengini_al(x, y, genislik, yukseklik))
    
    if sonuc == "UNKNOWN":
        for renk in metin_renkleri:
            sonuc = renk_eslesmelerini_kontrol_et(renk)
            if sonuc != "UNKNOWN":
                return sonuc, renk
                
    return sonuc, None

def renk_mesafesi(renk1, renk2, agirliklar=(1.0, 1.2, 0.8)):
    """İki renk arasındaki farkı hesaplar"""
    try:
        return sum(agirlik * (c1 - c2)**2 for c1, c2, agirlik in zip(renk1, renk2, agirliklar))**0.5
    except OverflowError:
        return 1000

def renk_yakin_mi(renk1, renk2, esik=40):
    """Renkler birbirine yakın mı diye kontrol eder"""
    mesafe = renk_mesafesi(renk1, renk2)
    return mesafe < esik, mesafe

def en_yakin_eslesmeyi_bul(renk, renk_listesi):
    """Listeden en yakın rengi bulur"""
    en_yakin_mesafe = float('inf')
    en_yakin_renk = None
    
    for hedef_renk in renk_listesi:
        mesafe = renk_mesafesi(renk, hedef_renk)
        if mesafe < en_yakin_mesafe:
            en_yakin_mesafe = mesafe
            en_yakin_renk = hedef_renk
    
    return en_yakin_renk, en_yakin_mesafe

def renk_eslesmelerini_kontrol_et(renk):
    """Rengin hangi kategoriye girdiğini çözer"""
    discord_esik = 40
    
    if renk_mesafesi(renk, DISCORD_HATA_RENGI) < 35:
        return "RED (Discord hata mesajı)"
        
    if renk_mesafesi(renk, DISCORD_KULLANIMDA_KIRMIZI) < 35:
        return "RED (Kullanıcı adı kullanımda)"
        
    if renk_mesafesi(renk, DISCORD_HATA_METNI_KIRMIZI) < 35:
        return "RED (Discord hata metni)"
    
    if renk_mesafesi(renk, DISCORD_BASARI_RENGI) < discord_esik:
        return "GREEN (Discord başarı mesajı)"
        
    if renk_mesafesi(renk, DISCORD_MUSAIT_YESIL) < 30:
        return "GREEN (Kullanıcı adı müsait mesajı)"
    
    if renk_mesafesi(renk, DISCORD_UYARI_RENGI) < discord_esik:
        return "YELLOW (Discord uyarı mesajı)"
    
    arayuz_esik = 40
    for i, arayuz_rengi in enumerate(UI_RENKLERI):
        if renk_mesafesi(renk, arayuz_rengi) < arayuz_esik:
            return f"UI (Discord arayüz öğesi #{i+1})"
    
    yesil_esik = 45
    for i, yesil_renk in enumerate(YESIL_RENKLER):
        yakin_mi, mesafe = renk_yakin_mi(renk, yesil_renk, esik=yesil_esik)
        if yakin_mi:
            return f"GREEN (eşleşen #{i+1}, mesafe: {int(mesafe)})"
    
    kirmizi_esik = 45
    for i, kirmizi_renk in enumerate(KIRMIZI_RENKLER):
        yakin_mi, mesafe = renk_yakin_mi(renk, kirmizi_renk, esik=kirmizi_esik)
        if yakin_mi:
            return f"RED (eşleşen #{i+1}, mesafe: {int(mesafe)})"
    
    sari_esik = 60
    for i, sari_renk in enumerate(SARI_RENKLER):
        yakin_mi, mesafe = renk_yakin_mi(renk, sari_renk, esik=sari_esik)
        if yakin_mi:
            return f"YELLOW (eşleşen #{i+1}, mesafe: {int(mesafe)})"
    
    en_yakin_kirmizi, kirmizi_mesafe = en_yakin_eslesmeyi_bul(renk, KIRMIZI_RENKLER)
    en_yakin_yesil, yesil_mesafe = en_yakin_eslesmeyi_bul(renk, YESIL_RENKLER)
    en_yakin_sari, sari_mesafe = en_yakin_eslesmeyi_bul(renk, SARI_RENKLER)
    en_yakin_arayuz, arayuz_mesafe = en_yakin_eslesmeyi_bul(renk, UI_RENKLERI)
    
    en_kucuk_mesafe = min(kirmizi_mesafe, yesil_mesafe, sari_mesafe, arayuz_mesafe)
    
    if en_kucuk_mesafe == arayuz_mesafe:
        return f"UNKNOWN (arayüze yakın, mesafe: {int(arayuz_mesafe)})"
    elif en_kucuk_mesafe == kirmizi_mesafe:
        return f"UNKNOWN (KIRMIZI'ya yakın, mesafe: {int(kirmizi_mesafe)})"
    elif en_kucuk_mesafe == yesil_mesafe:
        return f"UNKNOWN (YESIL'e yakın, mesafe: {int(yesil_mesafe)})"
    else:
        return f"UNKNOWN (SARI'ya yakın, mesafe: {int(sari_mesafe)})"

def hata_ayiklama_metin_rengi_algilama(x, y, genislik, yukseklik):
    """Test amaçlı renkleri konsola döken fonksiyon"""
    print("\n--- RENK ANALİZİ ---")
    metin_renkleri = metin_renklerini_bul(x, y, genislik, yukseklik)
    
    if not metin_renkleri:
        print("Hiçbir renk yakalanamadı.")
        return
    
    print(f"Bulunan renk sayısı: {len(metin_renkleri)}")
    for i, renk in enumerate(metin_renkleri):
        durum = renk_eslesmelerini_kontrol_et(renk)
        print(f"{i+1}. RGB{renk} -> {durum}")
    print("--------------------\n")

def hata_ayiklama_ekran_goruntusu_al(x, y, genislik, yukseklik, dosya_adi="ekran_goruntusu.png"):
    """Anlık ekran görüntüsü kaydeder"""
    ekran_goruntusu = pyautogui.screenshot(region=(x, y, genislik, yukseklik))
    ekran_goruntusu.save(dosya_adi)

def tek_renk_kontrol_et(kutu):
    """Bölgeyi tek seferlik kontrol eder ve durumu döndürür"""
    x, y, genislik, yukseklik = kutu
    
    try:
        ekran_goruntusu = pyautogui.screenshot(region=(x, y, genislik, yukseklik))
        img_dizi = np.array(ekran_goruntusu)
        
        yesil_bulundu = False
        kirmizi_bulundu = False
        
        for i in range(img_dizi.shape[0]):
            for j in range(img_dizi.shape[1]):
                piksel = tuple(img_dizi[i, j])
                
                for yesil_renk in YESIL_RENKLER[:5]:
                    if renk_mesafesi(piksel, yesil_renk) < 30:
                        yesil_bulundu = True
                        break
                
                for kirmizi_renk in KIRMIZI_RENKLER[:5]:
                    if renk_mesafesi(piksel, kirmizi_renk) < 35:
                        kirmizi_bulundu = True
                        break
                        
        if yesil_bulundu and not kirmizi_bulundu:
            return "GREEN", YESIL_RENKLER[0]
        elif kirmizi_bulundu and not yesil_bulundu:
            return "RED", KIRMIZI_RENKLER[0]
    except Exception as e:
        pass
    
    durum, renk = baskin_metin_rengini_al(x, y, genislik, yukseklik)
    
    if durum in ["RED", "GREEN", "YELLOW", "UI"]:
        return durum, renk
    
    if renk is None:
        renk = kutu_rengini_al(x, y, genislik, yukseklik)
    
    durum = renk_eslesmelerini_kontrol_et(renk)
    
    if "RED" in durum:
        return "RED", renk
    elif "GREEN" in durum:
        return "GREEN", renk
    elif "YELLOW" in durum:
        return "YELLOW", renk
    elif "UI" in durum:
        return "UI", renk
    else:
        return "UNKNOWN", renk

def kutu_rengini_izle(kutu, aralik=0.1, metin_algilama_kullan=True, hata_ayiklama_modu=False, tekli_kontrol=False):
    """Belirtilen kutuyu sürekli izleyen döngü"""
    if tekli_kontrol:
        durum, _ = tek_renk_kontrol_et(kutu)
        return durum
        
    x, y, genislik, yukseklik = kutu
    
    kenar = BasitKenar(x, y, genislik, yukseklik)
    
    import atexit
    atexit.register(lambda: kenar.yok_et())
    
    if metin_algilama_kullan:
        mevcut_durum, mevcut_renk = baskin_metin_rengini_al(x, y, genislik, yukseklik)
        if mevcut_durum == "UNKNOWN" or mevcut_renk is None:
            mevcut_renk = kutu_rengini_al(x, y, genislik, yukseklik)
            mevcut_durum = renk_eslesmelerini_kontrol_et(mevcut_renk)
    else:
        mevcut_renk = kutu_rengini_al(x, y, genislik, yukseklik)
        mevcut_durum = renk_eslesmelerini_kontrol_et(mevcut_renk)
    
    izlemeyi_durdur = False
    
    def tusa_basildi(e):
        nonlocal izlemeyi_durdur, hata_ayiklama_modu
        if e.name == 'esc':
            izlemeyi_durdur = True
            kenar.yok_et()
        elif e.name == 'd' and keyboard.is_pressed('ctrl+alt'):
            hata_ayiklama_modu = not hata_ayiklama_modu
        elif e.name == 's' and keyboard.is_pressed('ctrl+alt'):
            hata_ayiklama_ekran_goruntusu_al(x, y, genislik, yukseklik)
    
    keyboard.on_press(tusa_basildi)
    
    try:
        while not izlemeyi_durdur:
            kenar.guncelle()
            
            if metin_algilama_kullan:
                yeni_durum, yeni_renk = baskin_metin_rengini_al(x, y, genislik, yukseklik)
                if yeni_durum == "UNKNOWN" or yeni_renk is None:
                    yeni_renk = kutu_rengini_al(x, y, genislik, yukseklik)
                    yeni_durum = renk_eslesmelerini_kontrol_et(yeni_renk)
            else:
                yeni_renk = kutu_rengini_al(x, y, genislik, yukseklik)
                yeni_durum = renk_eslesmelerini_kontrol_et(yeni_renk)
            
            if "RED" in yeni_durum and "RED" not in mevcut_durum:
                mevcut_durum = yeni_durum
                mevcut_renk = yeni_renk
                hata_ayiklama_ekran_goruntusu_al(x, y, genislik, yukseklik, f"hata_{int(time.time())}.png")
            elif "GREEN" in yeni_durum and "GREEN" not in mevcut_durum:
                mevcut_durum = yeni_durum
                mevcut_renk = yeni_renk
                hata_ayiklama_ekran_goruntusu_al(x, y, genislik, yukseklik, f"basari_{int(time.time())}.png")
            elif "YELLOW" in yeni_durum and "YELLOW" not in mevcut_durum:
                mevcut_durum = yeni_durum
                mevcut_renk = yeni_renk
                hata_ayiklama_ekran_goruntusu_al(x, y, genislik, yukseklik, f"uyari_{int(time.time())}.png")
            elif "UI" in yeni_durum and "UI" not in mevcut_durum:
                mevcut_durum = yeni_durum
                mevcut_renk = yeni_renk
            elif "UNKNOWN" in yeni_durum and not ("UNKNOWN" in mevcut_durum):
                mevcut_durum = yeni_durum
                mevcut_renk = yeni_renk
            
            time.sleep(aralik)
    except KeyboardInterrupt:
        pass
    finally:
        keyboard.unhook_all()
        kenar.yok_et()
        atexit.unregister(lambda: kenar.yok_et())

def imlec_konumunu_al():
    """Mouse'un anlık konumunu verir"""
    return pyautogui.position()

def kutuyu_etkilesimli_konumlandir():
    """Kullanıcının ekranda alan seçmesini sağlar"""
    print("İzlenecek alanın sol üst köşesine gelip Ctrl+Alt+C yapın:")
    
    while True:
        try:
            if keyboard.is_pressed('ctrl+alt+c'):
                konum = imlec_konumunu_al()
                print(f"Sol üst ayarlandı: {konum}")
                x1, y1 = konum
                break
        except:
            pass
        time.sleep(0.01)
    
    time.sleep(0.5)
    print("Şimdi sağ alt köşeye gelip tekrar Ctrl+Alt+C yapın:")
    
    while True:
        try:
            if keyboard.is_pressed('ctrl+alt+c'):
                konum = imlec_konumunu_al()
                print(f"Sağ alt ayarlandı: {konum}")
                x2, y2 = konum
                break
        except:
            pass
        time.sleep(0.01)
    
    genislik = x2 - x1
    yukseklik = y2 - y1
    
    return (x1, y1, genislik, yukseklik)

def pencereleri_en_uste_zorla(pencereler):
    """Pencerelerin hep önde kalmasını sağlayan Windows fonksiyonu"""
    try:
        import win32gui
        import win32con
        for pencere in pencereler:
            if hasattr(pencere, 'winfo_id'):
                hwnd = win32gui.GetParent(pencere.winfo_id())
                win32gui.SetWindowPos(
                    hwnd, 
                    win32con.HWND_TOPMOST,
                    0, 0, 0, 0,
                    win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE
                )
    except:
        pass

if __name__ == "__main__":
    print("Kutuyu elle ayarlamak ister misin? (y/n)")
    secim = input().strip().lower()
    
    if secim == 'y':
        kutu = kutuyu_etkilesimli_konumlandir()
        print("\nMetin algılama modu kullanılsın mı? (y/n)")
        metin_modu = input().strip().lower() == 'y'
        hata_ayiklama_modu = True
    else:
        ekran_genisligi = pyautogui.size().width
        ekran_yuksekligi = pyautogui.size().height
        
        kutu_genisligi = 410
        kutu_yuksekligi = 45
        kutu_x = (ekran_genisligi - kutu_genisligi) // 2
        kutu_y = int(ekran_yuksekligi * 0.481)
        
        kutu = (kutu_x, kutu_y, kutu_genisligi, kutu_yuksekligi)
        metin_modu = True
        hata_ayiklama_modu = True
    
    kutu_rengini_izle(kutu, metin_algilama_kullan=metin_modu, hata_ayiklama_modu=hata_ayiklama_modu)
