#!/usr/bin/env python3
"""
🎵 Nova Music Bot - Kurulum Scripti
Bu script bot kurulumunu otomatikleştirir
"""

import os
import sys
import subprocess
import platform

def print_banner():
    """Banner yazdırır"""
    print("=" * 60)
    print("🎵 Nova Music Bot - Kurulum Scripti")
    print("=" * 60)
    print()

def check_python_version():
    """Python versiyonunu kontrol eder"""
    print("🐍 Python versiyonu kontrol ediliyor...")
    
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 veya üzeri gerekli!")
        print(f"📦 Mevcut versiyon: {sys.version}")
        return False
    
    print(f"✅ Python versiyonu uygun: {sys.version}")
    return True

def install_requirements():
    """Gerekli paketleri yükler"""
    print("📦 Gerekli paketler yükleniyor...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Paketler başarıyla yüklendi!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Paket yükleme hatası: {e}")
        return False

def create_env_file():
    """Environment dosyası oluşturur"""
    print("📝 Environment dosyası oluşturuluyor...")
    
    if os.path.exists(".env"):
        print("⚠️ .env dosyası zaten mevcut!")
        return True
    
    try:
        with open(".env.example", "r") as f:
            example_content = f.read()
        
        with open(".env", "w") as f:
            f.write(example_content)
        
        print("✅ .env dosyası oluşturuldu!")
        print("📝 Lütfen .env dosyasını düzenleyerek gerekli değerleri girin")
        return True
    except Exception as e:
        print(f"❌ .env dosyası oluşturma hatası: {e}")
        return False

def check_ffmpeg():
    """FFmpeg kurulu olup olmadığını kontrol eder"""
    print("🎬 FFmpeg kontrol ediliyor...")
    
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        print("✅ FFmpeg kurulu!")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ FFmpeg kurulu değil!")
        print("📦 FFmpeg kurulumu:")
        
        system = platform.system().lower()
        
        if system == "linux":
            print("  Ubuntu/Debian: sudo apt update && sudo apt install ffmpeg")
            print("  CentOS/RHEL: sudo yum install ffmpeg")
        elif system == "darwin":
            print("  macOS: brew install ffmpeg")
        elif system == "windows":
            print("  Windows: https://ffmpeg.org/download.html adresinden indirin")
        
        return False

def create_directories():
    """Gerekli dizinleri oluşturur"""
    print("📁 Gerekli dizinler oluşturuluyor...")
    
    directories = ["downloads", "logs"]
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"✅ {directory}/ dizini oluşturuldu")
        except Exception as e:
            print(f"❌ {directory}/ dizini oluşturma hatası: {e}")
            return False
    
    return True

def main():
    """Ana kurulum fonksiyonu"""
    print_banner()
    
    # Python versiyonu kontrolü
    if not check_python_version():
        return False
    
    print()
    
    # FFmpeg kontrolü
    if not check_ffmpeg():
        print("\n⚠️ FFmpeg kurulumunu tamamladıktan sonra scripti tekrar çalıştırın")
        return False
    
    print()
    
    # Dizinleri oluştur
    if not create_directories():
        return False
    
    print()
    
    # Paketleri yükle
    if not install_requirements():
        return False
    
    print()
    
    # Environment dosyası oluştur
    if not create_env_file():
        return False
    
    print()
    print("=" * 60)
    print("🎉 Kurulum tamamlandı!")
    print("=" * 60)
    print()
    print("📝 Sonraki adımlar:")
    print("1. .env dosyasını düzenleyin")
    print("2. Gerekli değerleri girin:")
    print("   - API_ID ve API_HASH (my.telegram.org)")
    print("   - BOT_TOKEN (@BotFather)")
    print("   - OWNER_ID (Telegram User ID)")
    print("   - MONGO_URI (MongoDB bağlantısı)")
    print("3. python start.py ile botu başlatın")
    print()
    print("💬 Destek için: https://t.me/sohbetgo_tr")
    print("👤 Yapımcı: @dnztrmnn")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Kurulum iptal edildi")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Beklenmeyen hata: {e}")
        sys.exit(1)