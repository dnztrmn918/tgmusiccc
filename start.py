#!/usr/bin/env python3
"""
🎵 Nova Music Bot - Başlatma Scripti
Bu script botu başlatır ve hata durumunda yeniden başlatır
"""

import asyncio
import sys
import os
import logging
from datetime import datetime

# Nova Music Bot'u import et
try:
    from nova_music_bot import NovaMusicBot
except ImportError as e:
    print(f"❌ Nova Music Bot import hatası: {e}")
    print("📦 requirements.txt dosyasındaki paketleri yüklediğinizden emin olun")
    sys.exit(1)

# Logging ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('nova_music_bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

async def main():
    """Ana fonksiyon"""
    print("🎵 Nova Music Bot başlatılıyor...")
    print("=" * 50)
    
    # Environment variables kontrolü
    required_vars = ['API_ID', 'API_HASH', 'BOT_TOKEN']
    optional_vars = ['STRING_SESSION']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Eksik environment variables: {', '.join(missing_vars)}")
        print("📝 .env dosyasını kontrol edin ve gerekli değerleri girin")
        return
    
    # Session string kontrolü
    if not os.getenv('STRING_SESSION'):
        print("⚠️ STRING_SESSION bulunamadı!")
        print("📝 Session string oluşturmak için: python generate_session.py")
        print("⚠️ PyTgCalls çalışmayabilir!")
    
    # Bot instance'ı oluştur
    bot = NovaMusicBot()
    
    try:
        # Botu başlat
        await bot.start()
    except KeyboardInterrupt:
        print("\n🛑 Bot kullanıcı tarafından durduruldu")
        await bot.stop()
    except Exception as e:
        logger.error(f"❌ Bot hatası: {e}")
        print(f"❌ Bot hatası: {e}")
        await bot.stop()
        return False
    
    return True

if __name__ == "__main__":
    try:
        # Event loop'u başlat
        loop = asyncio.get_event_loop()
        success = loop.run_until_complete(main())
        
        if not success:
            print("❌ Bot başlatılamadı!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Script kullanıcı tarafından durduruldu")
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")
        sys.exit(1)