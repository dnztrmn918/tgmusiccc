#!/usr/bin/env python3
"""
🎵 Nova Music Bot - Gelişmiş Telegram Müzik Botu
✨ Özellikler:
- Yüksek kaliteli müzik oynatma
- Video ve ses indirme
- Broadcast sistemi
- Çoklu dil desteği
- Gelişmiş yönetim paneli
- Otomatik playlist yönetimi
"""

import asyncio
import logging
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional

import pyrogram
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped, AudioParameters
import yt_dlp
import requests
import json
import aiofiles
import aiohttp
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Environment variables
load_dotenv()

# Configuration
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
OWNER_ID = int(os.getenv("OWNER_ID", 0))
SUDO_USERS = [int(x) for x in os.getenv("SUDO_USERS", "").split(",") if x]

# Bot Bilgileri
BOT_NAME = "Nova Music"
OWNER_USERNAME = "dnztrmnn"
SUPPORT_GROUP = "https://t.me/sohbetgo_tr"
SUPPORT_CHANNEL = ""  # Boş bırakıldı, sonra eklenecek

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class NovaMusicBot:
    def __init__(self):
        self.app = Client(
            "nova_music_bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN
        )
        self.calls = PyTgCalls(self.app)
        self.mongo_client = AsyncIOMotorClient(MONGO_URI)
        self.db = self.mongo_client.nova_music_bot
        
        # Bot state
        self.active_chats: Dict[int, Dict] = {}
        self.queues: Dict[int, List] = {}
        self.current_track: Dict[int, Dict] = {}
        self.is_broadcasting = False
        
        # Commands
        self.setup_commands()
        
    def setup_commands(self):
        """Bot komutlarını ayarlar"""
        
        # Start komutu - Hem özel hem grup
        @self.app.on_message(filters.command(["start", "başla"]))
        async def start_command(client, message: Message):
            await self.start_handler(message)
            
        # Müzik oynatma komutları
        @self.app.on_message(filters.command(["play", "oynat", "çal"]))
        async def play_command(client, message: Message):
            await self.play_handler(message)
            
        # Duraklatma komutları
        @self.app.on_message(filters.command(["pause", "durdur", "duraklat"]))
        async def pause_command(client, message: Message):
            await self.pause_handler(message)
            
        # Devam ettirme komutları
        @self.app.on_message(filters.command(["resume", "devam", "devamet"]))
        async def resume_command(client, message: Message):
            await self.resume_handler(message)
            
        # Durdurma komutları
        @self.app.on_message(filters.command(["stop", "bitir", "durdur"]))
        async def stop_command(client, message: Message):
            await self.stop_handler(message)
            
        # Atlama komutları
        @self.app.on_message(filters.command(["skip", "atla", "geç"]))
        async def skip_command(client, message: Message):
            await self.skip_handler(message)
            
        # Kuyruk komutları
        @self.app.on_message(filters.command(["queue", "list", "kuyruk", "liste"]))
        async def queue_command(client, message: Message):
            await self.queue_handler(message)
            
        # İndirme komutları
        @self.app.on_message(filters.command(["download", "indir", "download"]))
        async def download_command(client, message: Message):
            await self.download_handler(message)
            
        # Broadcast komutları
        @self.app.on_message(filters.command(["broadcast", "yayınla"]))
        async def broadcast_command(client, message: Message):
            await self.broadcast_handler(message)
            
        # İstatistik komutları
        @self.app.on_message(filters.command(["stats", "istatistik", "durum"]))
        async def stats_command(client, message: Message):
            await self.stats_handler(message)
            
        # Yardım komutları
        @self.app.on_message(filters.command(["help", "yardım", "komutlar"]))
        async def help_command(client, message: Message):
            await self.help_handler(message)
        
        # Callback query handler'ları
        @self.app.on_callback_query()
        async def callback_handler(client, callback_query):
            await self.callback_handler(callback_query)

    async def start_handler(self, message: Message):
        """Start komutu işleyicisi"""
        user = message.from_user
        chat_type = message.chat.type
        
        # Özel mesaj kontrolü
        if chat_type == "private":
            welcome_text = f"""
🎵 **Hoş Geldiniz {user.first_name}!**

Ben **{BOT_NAME}** asistanıyım. Size şu özellikleri sunuyorum:

🎧 **Müzik Oynatma**
• YouTube, Spotify, SoundCloud desteği
• Yüksek kaliteli ses akışı
• Playlist yönetimi

📥 **İndirme**
• Video ve ses dosyası indirme
• Farklı kalite seçenekleri

📢 **Broadcast**
• Toplu mesaj gönderme
• Kullanıcı ve grup yönetimi

🔧 **Yönetim**
• Gelişmiş istatistikler
• Otomatik moderasyon

**Komutlar için /help yazın**
            """
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("💬 Sohbet Grubu", url=SUPPORT_GROUP)],
                [InlineKeyboardButton("📢 Resmi Kanal", url=SUPPORT_CHANNEL) if SUPPORT_CHANNEL else InlineKeyboardButton("📢 Resmi Kanal", callback_data="channel_soon")],
                [InlineKeyboardButton("👤 Yapımcı", url=f"https://t.me/{OWNER_USERNAME}")],
                [InlineKeyboardButton("📖 Komutlar", callback_data="help")],
                [InlineKeyboardButton("🎧 Müzik Çal", callback_data="play")]
            ])
            
            await message.reply_text(welcome_text, reply_markup=keyboard)
            
        else:
            # Grup mesajı
            welcome_text = f"""
🎵 **{BOT_NAME} Bot Aktif!**

Merhaba {user.first_name}! Ben müzik asistanınızım.

**Temel Komutlar:**
• `/oynat <şarkı>` - Şarkı çalar
• `/durdur` - Müziği duraklatır
• `/devam` - Müziği devam ettirir
• `/bitir` - Müziği durdurur
• `/atla` - Şarkıyı atlar
• `/liste` - Kuyruğu gösterir

**Detaylı komutlar için /yardım yazın**
            """
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("💬 Sohbet Grubu", url=SUPPORT_GROUP)],
                [InlineKeyboardButton("👤 Yapımcı", url=f"https://t.me/{OWNER_USERNAME}")],
                [InlineKeyboardButton("📖 Tüm Komutlar", callback_data="help")]
            ])
            
            await message.reply_text(welcome_text, reply_markup=keyboard)
    
    async def play_handler(self, message: Message):
        """Müzik çalma işleyicisi"""
        if not message.from_user:
            return
            
        chat_id = message.chat.id
        
        # Sesli sohbette olup olmadığını kontrol et
        if not await self.check_voice_chat(chat_id):
            await message.reply_text("❌ Sesli sohbette değilsiniz!")
            return
            
        # URL veya arama terimi al
        if len(message.command) < 2:
            await message.reply_text("❌ Lütfen bir şarkı adı veya URL girin!\nÖrnek: `/oynat despacito`")
            return
            
        query = " ".join(message.command[1:])
        status_msg = await message.reply_text("🔍 Şarkı aranıyor...")
        
        try:
            # YouTube'dan şarkı bilgilerini al
            track_info = await self.get_track_info(query)
            if not track_info:
                await status_msg.edit_text("❌ Şarkı bulunamadı!")
                return
                
            # Kuyruğa ekle
            if chat_id not in self.queues:
                self.queues[chat_id] = []
                
            self.queues[chat_id].append(track_info)
            
            # Eğer şu anda çalan şarkı yoksa çalmaya başla
            if chat_id not in self.current_track:
                await self.play_next(chat_id)
                await status_msg.edit_text(
                    f"🎵 **Şimdi Çalıyor:** {track_info['title']}\n"
                    f"👤 **Sanatçı:** {track_info['uploader']}\n"
                    f"⏱️ **Süre:** {self.format_duration(track_info['duration'])}"
                )
            else:
                await status_msg.edit_text(
                    f"✅ **{track_info['title']}** kuyruğa eklendi!\n"
                    f"🎵 Sıra: {len(self.queues[chat_id])}"
                )
                
        except Exception as e:
            logger.error(f"Play error: {e}")
            await status_msg.edit_text("❌ Bir hata oluştu!")
    
    async def get_track_info(self, query: str) -> Optional[Dict]:
        """YouTube'dan şarkı bilgilerini alır"""
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'extractaudio': True,
                'audioformat': 'mp3',
                'outtmpl': '%(title)s.%(ext)s',
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch:{query}", download=False)
                if info and 'entries' in info and info['entries']:
                    entry = info['entries'][0]
                    return {
                        'title': entry.get('title', 'Unknown'),
                        'duration': entry.get('duration', 0),
                        'url': entry.get('url', ''),
                        'thumbnail': entry.get('thumbnail', ''),
                        'uploader': entry.get('uploader', 'Unknown'),
                        'webpage_url': entry.get('webpage_url', '')
                    }
        except Exception as e:
            logger.error(f"Track info error: {e}")
            return None
    
    async def play_next(self, chat_id: int):
        """Sıradaki şarkıyı çalar"""
        if chat_id not in self.queues or not self.queues[chat_id]:
            return
            
        track = self.queues[chat_id].pop(0)
        self.current_track[chat_id] = track
        
        try:
            await self.calls.join_group_call(
                chat_id,
                AudioPiped(
                    track['url'],
                    AudioParameters(
                        bitrate=48000,
                    )
                )
            )
            
        except Exception as e:
            logger.error(f"Play next error: {e}")
    
    async def pause_handler(self, message: Message):
        """Duraklatma işleyicisi"""
        chat_id = message.chat.id
        
        if chat_id not in self.current_track:
            await message.reply_text("❌ Şu anda çalan şarkı yok!")
            return
            
        try:
            await self.calls.pause_stream(chat_id)
            await message.reply_text("⏸️ Müzik duraklatıldı!")
        except Exception as e:
            await message.reply_text("❌ Duraklatma hatası!")
    
    async def resume_handler(self, message: Message):
        """Devam ettirme işleyicisi"""
        chat_id = message.chat.id
        
        if chat_id not in self.current_track:
            await message.reply_text("❌ Şu anda çalan şarkı yok!")
            return
            
        try:
            await self.calls.resume_stream(chat_id)
            await message.reply_text("▶️ Müzik devam ediyor!")
        except Exception as e:
            await message.reply_text("❌ Devam ettirme hatası!")
    
    async def stop_handler(self, message: Message):
        """Durdurma işleyicisi"""
        chat_id = message.chat.id
        
        try:
            await self.calls.leave_group_call(chat_id)
            if chat_id in self.current_track:
                del self.current_track[chat_id]
            if chat_id in self.queues:
                self.queues[chat_id].clear()
            await message.reply_text("⏹️ Müzik durduruldu!")
        except Exception as e:
            await message.reply_text("❌ Durdurma hatası!")
    
    async def skip_handler(self, message: Message):
        """Şarkı atlama işleyicisi"""
        chat_id = message.chat.id
        
        if chat_id not in self.current_track:
            await message.reply_text("❌ Şu anda çalan şarkı yok!")
            return
            
        try:
            await self.calls.leave_group_call(chat_id)
            await self.play_next(chat_id)
            await message.reply_text("⏭️ Şarkı atlandı!")
        except Exception as e:
            await message.reply_text("❌ Atlama hatası!")
    
    async def queue_handler(self, message: Message):
        """Kuyruk görüntüleme işleyicisi"""
        chat_id = message.chat.id
        
        if chat_id not in self.queues or not self.queues[chat_id]:
            await message.reply_text("📭 Kuyruk boş!")
            return
            
        queue_text = "📋 **Müzik Kuyruğu:**\n\n"
        
        for i, track in enumerate(self.queues[chat_id][:10], 1):
            queue_text += f"{i}. **{track['title']}** - {track['uploader']}\n"
            
        if len(self.queues[chat_id]) > 10:
            queue_text += f"\n... ve {len(self.queues[chat_id]) - 10} şarkı daha"
            
        await message.reply_text(queue_text)
    
    async def download_handler(self, message: Message):
        """İndirme işleyicisi"""
        if len(message.command) < 2:
            await message.reply_text("❌ Lütfen bir URL girin!\nÖrnek: `/indir https://youtube.com/...`")
            return
            
        url = message.command[1]
        status_msg = await message.reply_text("⬇️ İndiriliyor...")
        
        try:
            # Video bilgilerini al
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': 'downloads/%(title)s.%(ext)s',
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'video')
                duration = info.get('duration', 0)
                
                # Video indir
                ydl.download([url])
                
                # Dosyayı gönder
                video_path = f"downloads/{title}.mp4"
                if os.path.exists(video_path):
                    await self.app.send_video(
                        message.chat.id,
                        video_path,
                        caption=f"📹 **{title}**\n⏱️ Süre: {self.format_duration(duration)}"
                    )
                    os.remove(video_path)
                    
        except Exception as e:
            logger.error(f"Download error: {e}")
            await status_msg.edit_text("❌ İndirme hatası!")
    
    async def broadcast_handler(self, message: Message):
        """Broadcast işleyicisi"""
        if message.from_user.id not in SUDO_USERS and message.from_user.id != OWNER_ID:
            await message.reply_text("❌ Bu komutu kullanma yetkiniz yok!")
            return
            
        if not message.reply_to_message:
            await message.reply_text("❌ Lütfen yayınlamak istediğiniz mesaja yanıt verin!")
            return
            
        if self.is_broadcasting:
            await message.reply_text("❌ Zaten bir yayın işlemi devam ediyor!")
            return
            
        # Broadcast türünü belirle
        broadcast_type = "all"
        if "-u" in message.text or "-user" in message.text:
            broadcast_type = "users"
        elif "-g" in message.text or "-group" in message.text:
            broadcast_type = "groups"
            
        self.is_broadcasting = True
        status_msg = await message.reply_text("📢 Yayın başlatılıyor...")
        
        try:
            sent_count = 0
            
            if broadcast_type == "users":
                # Sadece kullanıcılara gönder
                users = await self.db.users.find().to_list(length=None)
                for user in users:
                    try:
                        await message.reply_to_message.copy(user['user_id'])
                        sent_count += 1
                        await asyncio.sleep(0.1)
                    except Exception:
                        continue
                        
            elif broadcast_type == "groups":
                # Sadece gruplara gönder
                chats = await self.db.chats.find().to_list(length=None)
                for chat in chats:
                    try:
                        await message.reply_to_message.copy(chat['chat_id'])
                        sent_count += 1
                        await asyncio.sleep(0.1)
                    except Exception:
                        continue
                        
            else:
                # Herkese gönder
                users = await self.db.users.find().to_list(length=None)
                chats = await self.db.chats.find().to_list(length=None)
                
                for user in users:
                    try:
                        await message.reply_to_message.copy(user['user_id'])
                        sent_count += 1
                        await asyncio.sleep(0.1)
                    except Exception:
                        continue
                        
                for chat in chats:
                    try:
                        await message.reply_to_message.copy(chat['chat_id'])
                        sent_count += 1
                        await asyncio.sleep(0.1)
                    except Exception:
                        continue
                        
            await status_msg.edit_text(f"✅ Yayın tamamlandı! {sent_count} kişiye gönderildi.")
            
        except Exception as e:
            logger.error(f"Broadcast error: {e}")
            await status_msg.edit_text("❌ Yayın hatası!")
        finally:
            self.is_broadcasting = False
    
    async def stats_handler(self, message: Message):
        """İstatistik işleyicisi"""
        if message.from_user.id not in SUDO_USERS and message.from_user.id != OWNER_ID:
            await message.reply_text("❌ Bu komutu kullanma yetkiniz yok!")
            return
            
        try:
            # İstatistikleri al
            total_users = await self.db.users.count_documents({})
            total_chats = await self.db.chats.count_documents({})
            total_tracks = await self.db.tracks.count_documents({})
            
            stats_text = f"""
📊 **{BOT_NAME} İstatistikleri**

👥 **Toplam Kullanıcı:** {total_users:,}
💬 **Toplam Sohbet:** {total_chats:,}
🎵 **Toplam Şarkı:** {total_tracks:,}
🎧 **Aktif Sohbet:** {len(self.active_chats)}
📋 **Toplam Kuyruk:** {sum(len(q) for q in self.queues.values())}

🕐 **Son Güncelleme:** {datetime.now().strftime('%H:%M:%S')}
            """
            
            await message.reply_text(stats_text)
            
        except Exception as e:
            await message.reply_text("❌ İstatistik hatası!")
    
    async def help_handler(self, message: Message):
        """Yardım işleyicisi"""
        help_text = f"""
🎵 **{BOT_NAME} Komutları**

🎧 **Müzik Oynatma:**
• `/oynat <şarkı>` - Şarkı çalar
• `/durdur` - Müziği duraklatır
• `/devam` - Müziği devam ettirir
• `/bitir` - Müziği durdurur
• `/atla` - Şarkıyı atlar
• `/liste` - Kuyruğu gösterir

📥 **İndirme:**
• `/indir <url>` - Video indirir

📢 **Yönetim:**
• `/yayınla` - Toplu mesaj gönderir
• `/yayınla -u` - Sadece kullanıcılara gönderir
• `/yayınla -g` - Sadece gruplara gönderir
• `/istatistik` - Bot istatistiklerini gösterir

❓ **Yardım:**
• `/yardım` - Bu mesajı gösterir

💡 **İpucu:** Sesli sohbette olmadan müzik çalamazsınız!

👤 **Yapımcı:** @{OWNER_USERNAME}
💬 **Sohbet Grubu:** {SUPPORT_GROUP}
        """
        
        await message.reply_text(help_text)
    
    async def check_voice_chat(self, chat_id: int) -> bool:
        """Sesli sohbette olup olmadığını kontrol eder"""
        try:
            chat = await self.app.get_chat(chat_id)
            return chat.voice_chat is not None
        except:
            return False
    
    def format_duration(self, seconds: int) -> str:
        """Süreyi formatlar"""
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes}:{seconds:02d}"
    
    async def start(self):
        """Botu başlatır"""
        logger.info(f"🎵 {BOT_NAME} Bot başlatılıyor...")
        
        # Downloads klasörünü oluştur
        os.makedirs("downloads", exist_ok=True)
        
        # PyTgCalls'ı başlat
        await self.calls.start()
        
        # Botu başlat
        await self.app.start()
        
        logger.info(f"✅ {BOT_NAME} Bot başarıyla başlatıldı!")
        
        # Bot çalışır durumda kal
        await pyrogram.idle()
    
    async def stop(self):
        """Botu durdurur"""
        logger.info(f"🛑 {BOT_NAME} Bot durduruluyor...")
        await self.app.stop()
        await self.calls.stop()
        await self.mongo_client.close()

    async def callback_handler(self, callback_query):
        """Callback query işleyicisi"""
        data = callback_query.data
        
        if data == "help":
            await self.help_callback(callback_query)
        elif data == "play":
            await self.play_callback(callback_query)
        elif data == "stats":
            await self.stats_callback(callback_query)
        elif data == "channel_soon":
            await self.channel_soon_callback(callback_query)
        else:
            await callback_query.answer("❌ Geçersiz seçenek!")
    
    async def help_callback(self, callback_query):
        """Yardım callback'i"""
        help_text = f"""
🎵 **{BOT_NAME} Komutları**

🎧 **Müzik Oynatma:**
• `/oynat <şarkı>` - Şarkı çalar
• `/durdur` - Müziği duraklatır
• `/devam` - Müziği devam ettirir
• `/bitir` - Müziği durdurur
• `/atla` - Şarkıyı atlar
• `/liste` - Kuyruğu gösterir

📥 **İndirme:**
• `/indir <url>` - Video indirir

📢 **Yönetim:**
• `/yayınla` - Toplu mesaj gönderir
• `/yayınla -u` - Sadece kullanıcılara gönderir
• `/yayınla -g` - Sadece gruplara gönderir
• `/istatistik` - Bot istatistiklerini gösterir

❓ **Yardım:**
• `/yardım` - Bu mesajı gösterir

💡 **İpucu:** Sesli sohbette olmadan müzik çalamazsınız!

👤 **Yapımcı:** @{OWNER_USERNAME}
💬 **Sohbet Grubu:** {SUPPORT_GROUP}
        """
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Geri", callback_data="back_to_start")]
        ])
        
        await callback_query.edit_message_text(help_text, reply_markup=keyboard)
    
    async def play_callback(self, callback_query):
        """Müzik çalma callback'i"""
        await callback_query.answer("🎧 Müzik çalmak için bir gruba gidin ve /oynat komutunu kullanın!")
    
    async def stats_callback(self, callback_query):
        """İstatistik callback'i"""
        if callback_query.from_user.id not in SUDO_USERS and callback_query.from_user.id != OWNER_ID:
            await callback_query.answer("❌ Bu özelliği kullanma yetkiniz yok!")
            return
            
        try:
            # İstatistikleri al
            total_users = await self.db.users.count_documents({})
            total_chats = await self.db.chats.count_documents({})
            total_tracks = await self.db.tracks.count_documents({})
            
            stats_text = f"""
📊 **{BOT_NAME} İstatistikleri**

👥 **Toplam Kullanıcı:** {total_users:,}
💬 **Toplam Sohbet:** {total_chats:,}
🎵 **Toplam Şarkı:** {total_tracks:,}
🎧 **Aktif Sohbet:** {len(self.active_chats)}
📋 **Toplam Kuyruk:** {sum(len(q) for q in self.queues.values())}

🕐 **Son Güncelleme:** {datetime.now().strftime('%H:%M:%S')}
            """
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Geri", callback_data="back_to_start")]
            ])
            
            await callback_query.edit_message_text(stats_text, reply_markup=keyboard)
            
        except Exception as e:
            await callback_query.answer("❌ İstatistik hatası!")
    
    async def channel_soon_callback(self, callback_query):
        """Kanal yakında callback'i"""
        await callback_query.answer("📢 Resmi kanal yakında açılacak!")

# Ana fonksiyon
async def main():
    bot = NovaMusicBot()
    try:
        await bot.start()
    except KeyboardInterrupt:
        await bot.stop()
    except Exception as e:
        logger.error(f"Bot error: {e}")
        await bot.stop()

if __name__ == "__main__":
    asyncio.run(main())