# -*- coding: utf-8 -*-
# 📁 babusona.py

import json
import random
from pyrogram import Client, filters
from pyrogram.types import Message
from ShrutiMusic import app  # bot instance
from config import OWNER_ID  # sudo kontrolü için

KANAL = "@tubidymusic"

# JSON dosyasını kontrol et / oluştur
def veri_kontrol_et():
    try:
        with open("veri.json", "r", encoding="utf-8") as f:
            json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        with open("veri.json", "w", encoding="utf-8") as f:
            json.dump({"siirler": [], "sozler": []}, f, indent=4, ensure_ascii=False)

veri_kontrol_et()

# JSON'a veri ekleme
def veri_ekle(kategori: str, metin_dict: dict) -> bool:
    try:
        with open("veri.json", "r", encoding="utf-8") as dosya:
            veri = json.load(dosya)

        veri[kategori].append(metin_dict)

        with open("veri.json", "w", encoding="utf-8") as dosya:
            json.dump(veri, dosya, indent=4, ensure_ascii=False)

        return True
    except Exception as e:
        print(f"[HATA]: {e}")
        return False

# 🔠 Rastgele şiir gönder
@app.on_message(filters.command(["siir", ".siir"]))
async def siir_gonder(client: Client, message: Message):
    try:
        with open("veri.json", "r", encoding="utf-8") as dosya:
            veri = json.load(dosya)
        if not veri["siirler"]:
            return await message.reply_text("📭 Henüz eklenmiş bir şiir yok.")

        secilen = random.choice(veri["siirler"])
        metin = secilen.get("metin", "Şiir bulunamadı.")
        yazar = secilen.get("yazar", "Anonim")

        cevap = (
            "📜 𝐒ᴇɴɪɴ ɪᴄ̧ɪɴ şᴇᴄ̧ᴛɪɢ̆ɪᴍɪᴢ 𝐒̧ɪɪʀ\n\n"
            f"{metin}\n\n"
            f"— {yazar}\n\n"
            f"📣 𝐒̧ɪɪʀ 𝐌ᴜ̈ᴢɪᴋ 𝐊ᴀɴᴀʟɪᴍɪᴢ: {KANAL}"
        )

        await message.reply_text(cevap)
    except Exception:
        await message.reply_text("❌ Şiir gönderilemedi.")

# 🔠 Rastgele söz gönder
@app.on_message(filters.command(["soz", ".soz"]))
async def soz_gonder(client: Client, message: Message):
    try:
        with open("veri.json", "r", encoding="utf-8") as dosya:
            veri = json.load(dosya)
        if not veri["sozler"]:
            return await message.reply_text("📭 Henüz eklenmiş bir söz yok.")

        secilen = random.choice(veri["sozler"])
        metin = secilen.get("metin", "Söz bulunamadı.")
        yazar = secilen.get("yazar", "Anonim")

        cevap = (
            "📝 𝐒ᴇɴɪɴ ɪᴄ̧ɪɴ şᴇᴄ̧ᴛɪɢ̆ɪᴍɪᴢ 𝐒ᴏ̈ᴢ\n\n"
            f"{metin}\n\n"
            f"— {yazar}\n\n"
            f"📣 𝐒̧ɪɪʀ 𝐌ᴜ̈ᴢɪᴋ 𝐊ᴀɴᴀʟɪᴍɪᴢ: {KANAL}"
        )

        await message.reply_text(cevap)
    except Exception:
        await message.reply_text("❌ Söz gönderilemedi.")

# 🛠️ Şiir ekle (sadece OWNER)
@app.on_message(filters.command(["siirekle", ".siirekle"]) & filters.private)
async def siir_ekle(client: Client, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply_text("🚫 Bu komutu sadece bot sahibi kullanabilir.")

    try:
        girdi = message.text.split(None, 1)[1]  # komuttan sonrası
    except IndexError:
        return await message.reply_text("❗ Lütfen eklenecek şiiri şu formatta gir:\n`/siirekle <şiir> | <yazar>`")

    if "|" not in girdi:
        return await message.reply_text("❗ Format hatalı!\nDoğru kullanım:\n`/siirekle <şiir> | <yazar>`")

    metin, yazar = girdi.split("|", 1)
    metin_dict = {"metin": metin.strip(), "yazar": yazar.strip()}

    if veri_ekle("siirler", metin_dict):
        await message.reply_text("✅ Şiir başarıyla eklendi.")
    else:
        await message.reply_text("❌ Şiir eklenirken bir hata oluştu.")

# 🛠️ Söz ekle (sadece OWNER)
@app.on_message(filters.command(["sozekle", ".sozekle"]) & filters.private)
async def soz_ekle(client: Client, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply_text("🚫 Bu komutu sadece bot sahibi kullanabilir.")

    try:
        girdi = message.text.split(None, 1)[1]
    except IndexError:
        return await message.reply_text("❗ Lütfen eklenecek sözü şu formatta gir:\n`/sozekle <söz> | <yazar>`")

    if "|" not in girdi:
        return await message.reply_text("❗ Format hatalı!\nDoğru kullanım:\n`/sozekle <söz> | <yazar>`")

    metin, yazar = girdi.split("|", 1)
    metin_dict = {"metin": metin.strip(), "yazar": yazar.strip()}

    if veri_ekle("sozler", metin_dict):
        await message.reply_text("✅ Söz başarıyla eklendi.")
    else:
        await message.reply_text("❌ Söz eklenirken bir hata oluştu.")

__MODULE__ = "Şiir & Söz"
__HELP__ = """
**Şiir ve Söz Komutları:**

/siir - Rastgele şiir gönderir  
/soz - Rastgele söz gönderir  

📌 **Ekleme Komutları (Sadece Bot Sahibi)**  
/siirekle <şiir> | <yazar>  
/sozekle <söz> | <yazar>  
"""
