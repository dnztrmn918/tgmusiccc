#!/usr/bin/env python3
"""
🎵 Nova Music Bot - Session String Oluşturucu
Bu script PyTgCalls için gerekli session string'i oluşturur
"""

import asyncio
import os
from pyrogram import Client
from dotenv import load_dotenv

# Environment variables yükle
load_dotenv()

async def generate_session():
    """Session string oluşturur"""
    print("🎵 Nova Music Bot - Session String Oluşturucu")
    print("=" * 50)
    print()
    
    # API bilgilerini al
    api_id = os.getenv("API_ID")
    api_hash = os.getenv("API_HASH")
    
    if not api_id or not api_hash:
        print("❌ API_ID ve API_HASH .env dosyasında bulunamadı!")
        print("📝 Lütfen .env dosyasını kontrol edin")
        return
    
    print("📱 Telegram hesabınızla giriş yapın...")
    print("📝 Telefon numaranızı ülke kodu ile girin (örn: +905551234567)")
    
    try:
        # Geçici client oluştur
        app = Client(
            "nova_music_session",
            api_id=int(api_id),
            api_hash=api_hash
        )
        
        # Session string oluştur
        await app.start()
        
        # Session string'i al
        session_string = app.export_session_string()
        
        print()
        print("✅ Session string başarıyla oluşturuldu!")
        print("=" * 50)
        print("📋 Bu string'i .env dosyasındaki STRING_SESSION değişkenine ekleyin:")
        print("=" * 50)
        print(session_string)
        print("=" * 50)
        print()
        print("💡 Örnek .env dosyası:")
        print("STRING_SESSION=" + session_string)
        print()
        print("⚠️ Bu string'i kimseyle paylaşmayın!")
        print("🔒 Hesabınızın güvenliği için gizli tutun!")
        
        # Session string'i dosyaya kaydet
        with open("session_string.txt", "w") as f:
            f.write(session_string)
        
        print()
        print("💾 Session string session_string.txt dosyasına kaydedildi")
        
    except Exception as e:
        print(f"❌ Session oluşturma hatası: {e}")
        print("📝 API_ID ve API_HASH değerlerini kontrol edin")
    
    finally:
        # Client'ı durdur
        await app.stop()

if __name__ == "__main__":
    try:
        asyncio.run(generate_session())
    except KeyboardInterrupt:
        print("\n🛑 İşlem iptal edildi")
    except Exception as e:
        print(f"\n❌ Beklenmeyen hata: {e}")