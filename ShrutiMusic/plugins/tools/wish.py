import asyncio
import random
import json
import os
from pyrogram import filters
from pyrogram.types import Message
from pyrogram import enums
from ShrutiMusic import app  # Bot uygulamanızın app nesnesi

# Aktif taglama yapan sohbetleri tutan global sözlük
active_chats = {}

# JSON dosyasından mesajları yükleme fonksiyonu
def load_messages():
    """messages.json dosyasını yükler"""
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, "messages.json")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Mesaj dosyası bulunamadı: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# Mesajlar messages.json'dan yüklenir
MESSAGES = load_messages()

# Sohetteki bot olmayan ve silinmemiş kullanıcıları getiren fonksiyon
async def get_chat_users(chat_id):
    users = []
    async for member in app.get_chat_members(chat_id):
        if member.user.is_bot or member.user.is_deleted:
            continue
        users.append(member.user)
    return users

# Genel etiketleme fonksiyonu
async def tag_users(chat_id, messages, tag_type):
    if not messages:
        return await app.send_message(chat_id, f"⚠️ {tag_type} için mesaj listesi boş!")

    users = await get_chat_users(chat_id)
    if not users:
        return await app.send_message(chat_id, "❌ Etiketlenecek kullanıcı bulunamadı.")

    for i in range(0, len(users), 5):
        # Eğer etiketleme durdurulduysa döngüyü kır
        if chat_id not in active_chats:
            break
        
        batch = users[i:i+5]
        mentions = " ".join([f"[{u.first_name}](tg://user?id={u.id})" for u in batch])
        
        msg_text = random.choice(messages)
        full_msg = f"{msg_text} {mentions}"
        
        await app.send_message(chat_id, full_msg, disable_web_page_preview=True, parse_mode=enums.ParseMode.MARKDOWN)
        
        await asyncio.sleep(5)
    
    active_chats.pop(chat_id, None)
    await app.send_message(chat_id, f"✅ {tag_type} etiketleme tamamlandı!")

# =================== KOMUTLAR ===================

@app.on_message(filters.command("gtag") & filters.group)
async def gtag(_, message: Message):
    chat_id = message.chat.id
    if chat_id in active_chats:
        return await message.reply("⚠️ Günaydın etiketleme zaten devam ediyor.")
    active_chats[chat_id] = True
    await message.reply("☀️ Günaydın etiketleme başlatıldı...")
    await tag_users(chat_id, MESSAGES.get("gtag", []), "Günaydın")

@app.on_message(filters.command("itag") & filters.group)
async def itag(_, message: Message):
    chat_id = message.chat.id
    if chat_id in active_chats:
        return await message.reply("⚠️ İyi geceler etiketleme zaten devam ediyor.")
    active_chats[chat_id] = True
    await message.reply("🌙 İyi geceler etiketleme başlatıldı...")
    await tag_users(chat_id, MESSAGES.get("itag", []), "İyi Geceler")

@app.on_message(filters.command("ktag") & filters.group)
async def ktag(_, message: Message):
    chat_id = message.chat.id
    if chat_id in active_chats:
        return await message.reply("⚠️ Kurt oyunu etiketleme zaten devam ediyor.")
    active_chats[chat_id] = True
    await message.reply("🐺 Kurt oyunu etiketleme başlatıldı...")
    await tag_users(chat_id, MESSAGES.get("ktag", []), "Kurt Oyunu")

@app.on_message(filters.command("stag") & filters.group)
async def stag(_, message: Message):
    chat_id = message.chat.id
    if chat_id in active_chats:
        return await message.reply("⚠️ Sohbete çağırma etiketleme zaten devam ediyor.")
    active_chats[chat_id] = True
    await message.reply("💬 Sohbete çağırma etiketleme başlatıldı...")
    await tag_users(chat_id, MESSAGES.get("stag", []), "Sohbete Çağırma")

# ETİKETLEMEYİ DURDURMA KOMUTU
@app.on_message(filters.command(["stoptag", "cancel"]) & filters.group)
async def stoptag(_, message: Message):
    chat_id = message.chat.id
    if chat_id in active_chats:
        del active_chats[chat_id]
        await message.reply("🛑 Etiketleme durduruldu.")
    else:
        await message.reply("❌ Şu anda aktif bir etiketleme yok.")

# YARDIM KOMUTU
@app.on_message(filters.command("tagyardim") & filters.group)
async def tagyardim(_, message: Message):
    help_text = """
🏷️ **Etiketleme Komutları Yardım**

• `/gtag` - Günaydın mesajlarıyla etiketleme  
• `/itag` - İyi geceler mesajlarıyla etiketleme  
• `/ktag` - Kurt oyununa çağırma etiketlemesi  
• `/stag` - Sohbete çağırma etiketlemesi  
• `/stoptag` - Aktif etiketlemeyi durdur

**Not:** Aynı anda sadece bir etiketleme çalışabilir.
"""
    await message.reply(help_text)

# ©️ 2025 Nand Yaduwanshi (aka @NoxxOP)
# 🔗 GitHub: https://github.com/NoxxOP/ShrutiMusic
# 📢 Telegram Kanalı: https://t.me/ShrutiBots
