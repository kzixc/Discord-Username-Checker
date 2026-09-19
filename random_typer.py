"""
KZI - Kullanıcı Adı Denetleyicisi ve Otomatik Yazıcı
Sürüm: UCv1.4.0-stable
(Çalışan kararlı sürüm, ellemiyoruz)
"""

import time
import random
import pyautogui
import keyboard
import requests
import json
import datetime
import os
import sys
import win32gui
import win32con
import subprocess   
import socket   
import string
from color_detector_visual import check_single_color, SimpleBorder

# ASCII Başlık Yazısı
ASCII_TITLE = r"""
 _   _                                       
| | | |___  ___ _ __ _ __   __ _ _ __ ___  ___ 
| | | / __|/ _ \ '__| '_ \ / _` | '_ ` _ \/ __|
| |_| \__ \  __/ |  | | | | (_| | | | | | \__ \
 \___/|___/\___|_|  |_| |_|\__,_|_| |_| |_|___/
                                              
  ____ _               _             
 / ___| |__   ___  ___| | _____ _ __ 
| |   | '_ \ / _ \/ __| |/ / _ \ '__|
| |___| | | |  __/ (__|   <  __/ |   
 \____|_| |_|\___|\___|_|\_\___|_|   
"""

# Hata kayıt tutucu fonksiyon
def debug_log(msg):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"[DEBUG] {timestamp} | {msg}"
    print(log_line)
    with open('debug.log', 'a', encoding='utf-8') as f:
        f.write(log_line + '\n')

# Çıkış kontrol bayrağı
should_exit = False

# Webhook ayarları
WEBHOOK_URL = ""
SNIPE_IMAGE_URL = "https://raw.githubusercontent.com/Daziusm/Daziusm/refs/heads/main/sniped.jpg"

# Çözünürlüğe göre konumlar
RESOLUTION_POSITIONS = {
    "2560x1440": {
        "box_width": 410,
        "box_height": 45,
        "box_y_ratio": 0.479
    },
    "1920x1440": {
        "box_width": 410,
        "box_height": 45,
        "box_y_ratio": 0.479
    },
    "1920x1200": {
        "box_width": 410,
        "box_height": 45,
        "box_y_ratio": 0.479
    },
    "1920x1080": {
        "box_width": 410,
        "box_height": 45,
        "box_y_ratio": 0.479
    }
}

# Terminal renkleri
class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"

def center_text(text, width=80):
    """Metni terminalde ortalar"""
    lines = text.split("\n")
    centered_lines = [line.center(width) for line in lines]
    return "\n".join(centered_lines)

def clear_screen():
    """Konsol ekranını temizler"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_status(message, color=None, centered=True, width=80):
    """Düzenli durum mesajı basar"""
    if color:
        message = f"{color}{message}{Colors.END}"
    
    if centered:
        message = center_text(message, width)
    
    print(message)

def print_separator(char="=", length=80):
    """Araç çizgisi çeker"""
    print(char * length)

def on_esc_press(e):
    """ESC tuşuna basılınca çalışacak fonksiyon"""
    global should_exit
    should_exit = True

def get_resolution():
    """Ekran çözünürlüğünü öğrenir"""
    width, height = pyautogui.size()
    return f"{width}x{height}"

def get_box_position():
    """Çözünürlüğe göre kutu konumunu hesaplar"""
    resolution = get_resolution()
    screen_width, screen_height = pyautogui.size()
    
    if resolution in RESOLUTION_POSITIONS:
        settings = RESOLUTION_POSITIONS[resolution]
    else:
        settings = RESOLUTION_POSITIONS["1920x1080"]
    
    box_width = settings["box_width"]
    box_height = settings["box_height"]
    box_y_ratio = settings["box_y_ratio"]
    
    box_x = (screen_width - box_width) // 2
    box_y = int(screen_height * box_y_ratio)
    
    return (box_x, box_y, box_width, box_height)

def load_words(filename):
    """Kelime listesini dosyadan okur"""
    try:
        with open(filename, 'r') as file:
            words = [line.strip() for line in file if line.strip()]
        return words
    except FileNotFoundError:
        debug_log(f"Hata: '{filename}' dosyası bulunamadı.")
        return []

def send_webhook(username, status="Available"):
    """Bulunan kullanıcı adını Discord webhook'una bildirir"""
    current_time = datetime.datetime.now()
    timestamp = current_time.isoformat()
    unix_timestamp = int(current_time.timestamp())
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    
    username_length = len(username)
    has_numbers = any(c.isdigit() for c in username)
    has_special = any(not c.isalnum() for c in username)
    
    complexity = "Basit"
    if has_numbers and has_special:
        complexity = "Karmaşık"
    elif has_numbers or has_special:
        complexity = "Orta"
    
    colors = [
        5793266,   
        5763719,   
        3066993,   
        2067276,   
        3447003,   
        10181046,  
        15277667,  
        15844367,  
        16705372,  
    ]
    
    embed = {
        "title": "🎮 Kullanıcı Adı Yakalandı!",
        "description": f"```{username}```\n**Discord'da boşta kullanıcı adı bulundu!**",
        "color": random.choice(colors),
        "fields": [
            {
                "name": "📊 İstatistikler",
                "value": f"**Uzunluk:** {username_length} karakter\n**Yapı:** {complexity}\n**Durum:** {status}",
                "inline": True
            },
            {
                "name": "⏱️ Zaman",
                "value": f"<t:{unix_timestamp}:F>\n<t:{unix_timestamp}:R>",
                "inline": True
            }
        ],
        "image": {
            "url": SNIPE_IMAGE_URL
        },
        "footer": {
            "text": f"KZI v1.4.0 • {formatted_time}"
        },
        "timestamp": timestamp
    }
    
    data = {
        "content": f"🚨 **BOŞTA KULLANICI ADI BULUNDU!** 🚨\n`{username}` Discord'da müsait!",
        "embeds": [embed],
        "username": "KZI Sniper",
        "avatar_url": "https://cdn.discordapp.com/emojis/1009148035633156146.webp"
    }
    
    try:
        response = requests.post(
            WEBHOOK_URL,
            data=json.dumps(data),
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 204:
            debug_log(f"Webhook başarıyla gönderildi: {username}")
        else:
            debug_log(f"Webhook gönderilemedi: {response.status_code}, {response.text}")
    except Exception as e:
        debug_log(f"Webhook gönderirken hata oluştu: {str(e)}")

def make_console_topmost():
    """Konsol penceresinin hep önde kalmasını sağlar"""
    try:
        console_window = win32gui.GetForegroundWindow()
        
        win32gui.SetWindowPos(
            console_window, 
            win32con.HWND_TOPMOST, 
            0, 0, 0, 0, 
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE
        )
        
        import atexit
        
        def restore_normal_window():
            try:
                win32gui.SetWindowPos(
                    console_window,
                    win32con.HWND_NOTOPMOST,
                    0, 0, 0, 0,
                    win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE
                )
                debug_log("Normal pencere düzenine dönüldü")
            except:
                pass
                
        atexit.register(restore_normal_window)
        debug_log("Konsol penceresi en üstte kalacak şekilde ayarlandı")
    except Exception as e:
        print_status(f"Uyarı: Pencere en üste sabitlenemedi: {str(e)}", color=Colors.YELLOW)

def generate_random_username(length):
    """Belirtilen uzunlukta rastgele ad üretir"""
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def generate_3letter_username():
    """3 harfli rastgele isim üretir"""
    return ''.join(random.choices(string.ascii_lowercase, k=3))

def generate_4letter_username():
    """4 harfli rastgele isim üretir"""
    return ''.join(random.choices(string.ascii_lowercase, k=4))

def verify_webhook_url(url):
    """Webhook adresinin geçerli olup olmadığını test eder"""
    if not url or url == "YOUR_DISCORD_WEBHOOK_URL_HERE" or "discord.com/api/webhooks/" not in url:
        return False
    
    try:
        response = requests.get(url)
        return response.status_code == 200
    except:
        return False

class UsernameChecker:
    def __init__(self, mode="file", words_file="words.txt", delay=2):
        self.mode = mode
        self.delay = delay
        self.valid_usernames = []
        self.current_word = ""
        
        if mode == "file":
            self.words = load_words(words_file)
        else:  
            self.words = []  
        
        self.monitoring_box = get_box_position()
        
        resolution = get_resolution()
        debug_log(f"Çözünürlük: {resolution}")
        debug_log(f"İzlenen Kutu: {self.monitoring_box}")
        
        self.border = SimpleBorder(
            self.monitoring_box[0],
            self.monitoring_box[1],
            self.monitoring_box[2],
            self.monitoring_box[3],
            border_thickness=4
        )
        
        debug_log("Çerçeve başarıyla oluşturuldu")
        
        self.terminal_width = 80
        try:
            self.terminal_width = os.get_terminal_size().columns
        except:
            pass

    def get_next_word(self):
        """Sıradaki kelimeyi getirir"""
        if self.mode == "file":
            if not self.words:
                return None
            return self.words.pop(0)
        elif self.mode == "3letter":
            return generate_3letter_username()
        elif self.mode == "4letter":
            return generate_4letter_username()

    def check_color(self):
        """Kutunun rengini kontrol ederek durum çıkarır"""
        self.border.update()
        status, color = check_single_color(self.monitoring_box)
        return status
    
    def type_username(self, word):
        """Discord'un kullanıcı adı alanına kelimeyi yazar"""
        self.current_word = word
        
        self.border.update()
        
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.2)
        pyautogui.press('delete')
        time.sleep(0.2)
        
        self.border.update()
        
        pyautogui.write(word)
        
        self.border.update()
        
        time.sleep(0.5)  
    
    def display_progress(self, word, index, total, status=""):
        """İlerleme durumunu ekrana basar"""
        clear_screen()
        
        term_width = self.terminal_width
        
        print(Colors.CYAN + center_text(ASCII_TITLE, term_width) + Colors.END)
        print_separator("=", term_width)
        
        progress_percent = int((index / total) * 100) if total > 0 else 0
        filled_length = int(progress_percent / 2)  
        empty_length = 50 - filled_length
        
        filled_bar = Colors.GREEN + "#" * filled_length + Colors.END
        empty_bar = "-" * empty_length
        progress_bar = f"[{filled_bar}{empty_bar}] {progress_percent}%"
        
        print("\n" + Colors.BOLD + "İLERLEME" + Colors.END)
        print_separator("-", term_width)
        print_status(f"Kontrol edilen: {Colors.BOLD}{Colors.YELLOW}{word}{Colors.END}", centered=False)
        print_status(f"Durum Çubuğu: {progress_bar}", centered=False)
        print_status(f"Bakılan: {index}/{total if total != 1000 else 'sınırsız'}", centered=False)
        
        if status:
            status_color = Colors.YELLOW
            status_text = "BİLİNMİYOR ❓"
            
            if status == "GREEN":
                status_color = Colors.GREEN
                status_text = "MÜSAİT ✅"
            elif status == "RED":
                status_color = Colors.RED
                status_text = "DOLU ❌"
                
            print_status(f"Sonuç: {status_color}{status_text}{Colors.END}", centered=False)
        
        if self.valid_usernames:
            print_separator("-", term_width)
            print_status(f"Bulunan boş ad sayısı: {len(self.valid_usernames)}", color=Colors.GREEN, centered=False)
            
            print("\n" + Colors.GREEN + "BOŞTA OLANLAR:" + Colors.END)
            show_count = min(5, len(self.valid_usernames))
            for i in range(show_count):
                username = self.valid_usernames[-(i+1)]  
                print_status(f"  ▶ {username}", color=Colors.GREEN, centered=False)
        
        print_separator("=", term_width)
        print_status("Durdurmak için ESC tuşuna basın", color=Colors.YELLOW, centered=False)
    
    def display_summary(self, attempts):
        """İşlem bitiminde özet ekranı gösterir"""
        clear_screen()
        
        term_width = self.terminal_width
        
        print(Colors.CYAN + center_text(ASCII_TITLE, term_width) + Colors.END)
        print_separator("=", term_width)
        
        print_status("ÖZET", color=Colors.BOLD + Colors.PURPLE)
        print_separator("-", term_width)
        
        print_status(f"Toplam {attempts} kullanıcı adı denendi", centered=False)
        print_status(f"{len(self.valid_usernames)} adet müsait ad bulundu", 
                     color=Colors.GREEN if self.valid_usernames else None, 
                     centered=False)
        
        if self.valid_usernames:
            print_separator("-", term_width)
            print_status("Müsait Kullanıcı Adları:", color=Colors.GREEN, centered=False)
            
            for i, username in enumerate(self.valid_usernames):
                print_status(f"  {i+1}. {username}", color=Colors.GREEN, centered=False)
        
        print_separator("=", term_width)
        print_status("KZI kullandığınız için teşekkürler!", color=Colors.CYAN)
        print_status("Çıkmak için herhangi bir tuşa basın...", color=Colors.YELLOW, centered=False)
    
    def run(self, max_attempts=None):
        """Süreci başlatan ana döngü"""
        global should_exit
        
        if os.name == 'nt':
            os.system('color')
        
        clear_screen()
        print(Colors.CYAN + center_text(ASCII_TITLE, self.terminal_width) + Colors.END)
        print_separator("=", self.terminal_width)
        
        if self.mode == "file":
            mode_message = "Dosyadan kelime okuma modunda başlatılıyor..."
        elif self.mode == "3letter":
            mode_message = "3 Harfli Üretici modunda başlatılıyor..."
        elif self.mode == "4letter":
            mode_message = "4 Harfli Üretici modunda başlatılıyor..."
        
        print_status(mode_message, color=Colors.GREEN)
        print_status("Durdurmak için ESC tuşuna basın", color=Colors.YELLOW)
        
        keyboard.on_press_key('esc', on_esc_press)
        
        attempts = 0
        total = len(self.words) if self.mode == "file" else 1000  
        
        try:
            while not should_exit:
                word = self.get_next_word()
                if word is None:
                    break
                
                if max_attempts and attempts >= max_attempts:
                    break
                
                self.type_username(word)
                
                status = self.check_color_with_verification()
                
                self.display_progress(word, attempts, total, status)
                
                if status == "GREEN":
                    self.valid_usernames.append(word)
                    debug_log(f"MÜSAİT AD BULUNDU: {word}")
                    send_webhook(word)
                
                attempts += 1
                time.sleep(0.5)  
        
        except KeyboardInterrupt:
            print_status("Kullanıcı tarafından durduruldu.", color=Colors.RED)
        finally:
            self.border.destroy()
            keyboard.unhook_all()
        
        self.display_summary(attempts)
        
        print_status("Çıkmak için herhangi bir tuşa basın...", color=Colors.YELLOW, centered=False)
        keyboard.read_key()
    
    def check_color_with_verification(self):
        """Doğruluk payını artırmak için rengi birkaç kez kontrol eder"""
        color_samples = []
        for _ in range(3):  
            status, _ = check_single_color(self.monitoring_box)
            color_samples.append(status)
            time.sleep(0.1)  
        
        if "GREEN" in color_samples:
            debug_log(f"Renk doğrulaması: Örneklerde GREEN bulundu {color_samples}")
            return "GREEN"
        
        if color_samples.count("RED") >= 2:
            debug_log(f"Renk doğrulaması: Örneklerde RED doğrulandı {color_samples}")
            return "RED"
        
        from collections import Counter
        most_common = Counter(color_samples).most_common(1)[0][0]
        debug_log(f"Renk doğrulaması: En yaygın renk {color_samples} -> {most_common}")
        return most_common

def show_menu():
    """Ana menüyü gösterip seçim alır"""
    clear_screen()
    print(Colors.CYAN + center_text(ASCII_TITLE, term_width) + Colors.END)
    print_separator("=", term_width)
    print_status("Mod seçiniz:", color=Colors.YELLOW)
    print("\n1) Dosya Modu - words.txt içindeki kelimeleri dener")
    print("2) 3-4 Harfli Üretici Modu")
    
    while True:
        choice = input("\nSeçiminiz (1 veya 2): ").strip()
        if choice == '1':
            return 'file'
        elif choice == '2':
            clear_screen()
            print(Colors.CYAN + center_text(ASCII_TITLE, term_width) + Colors.END)
            print_separator("=", term_width)
            print_status("Üretici alt modunu seçin:", color=Colors.YELLOW)
            print("\n1) 3 Harfli Üretici")
            print("2) 4 Harfli Üretici")
            
            while True:
                sub_choice = input("\nSeçiminiz (1 veya 2): ").strip()
                if sub_choice == '1':
                    return '3letter'
                elif sub_choice == '2':
                    return '4letter'
                print_status("Geçersiz seçim. 1 veya 2 girin.", color=Colors.RED)
        else:
            print_status("Geçersiz seçim. 1 veya 2 girin.", color=Colors.RED)

if __name__ == "__main__":
    make_console_topmost()
    
    term_width = 80
    try:
        term_width = os.get_terminal_size().columns
    except:
        pass
    
    mode = show_menu()
    
    checker = UsernameChecker(mode=mode, words_file="words.txt", delay=2)
    
    webhook_valid = verify_webhook_url(WEBHOOK_URL)
    
    if not webhook_valid:
        print_separator("-", term_width)
        print_status("⚠️ UYARI: Webhook adresi geçersiz veya ayarlanmamış! ⚠️", color=Colors.RED, centered=True)
        print_status("Müsait kullanıcı adları Discord'a bildirilmeyecek.", color=Colors.YELLOW, centered=True)
        print_separator("-", term_width)
        print_status("Geçerli bir webhook adresi girmek ister misiniz? (y/n)", color=Colors.YELLOW)
        choice = input(center_text("> ", term_width)).strip().lower()
        
        if choice == 'y':
            print_status("Discord webhook adresini girin:", color=Colors.YELLOW)
            webhook_url = input(center_text("> ", term_width))
            if webhook_url and verify_webhook_url(webhook_url):
                WEBHOOK_URL = webhook_url
                print_status("Webhook adresi doğrulandı ve ayarlandı!", color=Colors.GREEN)
                webhook_valid = True
            else:
                print_status("Geçersiz webhook adresi. Bildirimler kapalı devam ediliyor.", color=Colors.RED)
    else:
        print_status("✓ Webhook adresi geçerli ve aktif!", color=Colors.GREEN)
    
    print_status("Kontrole başlamak için herhangi bir tuşa basın...", color=Colors.GREEN)
    keyboard.read_key()
    
    checker.run()
