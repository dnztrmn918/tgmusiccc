import asyncio
import random
import json
from pyrogram import filters
from pyrogram.types import Message
from pyrogram import enums
from ShrutiMusic import app  # Bot uygulamanızın app nesnesi burada

# Aktif taglama yapan sohbetleri tutan global sözlük
active_chats = {}

# JSON dosyasından mesajları yükleme fonksiyonu
def load_messages():
    with open("messages.json", "r", encoding="utf-8") as f:
        return json.load(f)

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
    users = await get_chat_users(chat_id)
    
    for i in range(0, len(users), 5):
        # Eğer etiketleme durdurulduysa döngüyü kır
        if chat_id not in active_chats:
            break
        
        batch = users[i:i+5]
        # Kullanıcıları mention olarak oluştur
        mentions = " ".join([f"[{u.first_name}](tg://user?id={u.id})" for u in batch])
        
        # JSON'dan rastgele mesaj seç ve mention'ları sona ekle
        msg_text = random.choice(messages)
        full_msg = f"{msg_text} {mentions}"
        
        # Mesajı gönder, markdown ile mention aktif olacak
        await app.send_message(chat_id, full_msg, disable_web_page_preview=True, parse_mode=enums.ParseMode.MARKDOWN)
        
        # 2 saniye bekle
        await asyncio.sleep(2)
    
    # İşlem tamamlandıktan sonra durumu temizle ve bilgi mesajı at
    active_chats.pop(chat_id, None)
    await app.send_message(chat_id, f"✅ {tag_type} etiketleme tamamlandı!")

# =================== KOMUTLAR ===================

# GÜNAYDIN ETİKETLEME (gtag)
@app.on_message(filters.command("gtag") & filters.group)
async def gtag(_, message: Message):
    chat_id = message.chat.id
    if chat_id in active_chats:
        return await message.reply("⚠️ Günaydın etiketleme zaten devam ediyor.")
    active_chats[chat_id] = True
    await message.reply("☀️ Günaydın etiketleme başlatıldı...")
    await tag_users(chat_id, MESSAGES["gtag"], "Günaydın")

# İYİ GECELER ETİKETLEME (itag)
@app.on_message(filters.command("itag") & filters.group)
async def itag(_, message: Message):
    chat_id = message.chat.id
    if chat_id in active_chats:
        return await message.reply("⚠️ İyi geceler etiketleme zaten devam ediyor.")
    active_chats[chat_id] = True
    await message.reply("🌙 İyi geceler etiketleme başlatıldı...")
    await tag_users(chat_id, MESSAGES["itag"], "İyi Geceler")

# KURT OYUNU ETİKETLEME (ktag)
@app.on_message(filters.command("ktag") & filters.group)
async def ktag(_, message: Message):
    chat_id = message.chat.id
    if chat_id in active_chats:
        return await message.reply("⚠️ Kurt oyunu etiketleme zaten devam ediyor.")
    active_chats[chat_id] = True
    await message.reply("🐺 Kurt oyunu etiketleme başlatıldı...")
    await tag_users(chat_id, MESSAGES["ktag"], "Kurt Oyunu")

# SOHBETE ÇAĞIRMA ETİKETLEME (stag)
@app.on_message(filters.command("stag") & filters.group)
async def stag(_, message: Message):
    chat_id = message.chat.id
    if chat_id in active_chats:
        return await message.reply("⚠️ Sohbete çağırma etiketleme zaten devam ediyor.")
    active_chats[chat_id] = True
    await message.reply("💬 Sohbete çağırma etiketleme başlatıldı...")
    await tag_users(chat_id, MESSAGES["stag"], "Sohbete Çağırma")

# ETİKETLEMEYİ DURDURMA KOMUTU (stoptag)
@app.on_message(filters.command("stoptag") & filters.group)
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
