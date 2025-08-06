# -*- coding: utf-8 -*-
# 📁 siir_soz.py

import json
from pyrogram import Client, filters
from pyrogram.types import Message
from ShrutiMusic import app  # bot instance
from config import OWNER_ID  # sudo kontrolü için

# JSON dosyasından rastgele veri çekmek için
import random

# JSON dosyasını oku ya da oluştur
def veri_kontrol_et():
    try:
        with open("veri.json", "r", encoding="utf-8") as f:
            json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        with open("veri.json", "w", encoding="utf-8") as f:
            json.dump({"siirler": [], "sozler": []}, f, indent=4, ensure_ascii=False)

veri_kontrol_et()

# JSON'a veri ekleme
def veri_ekle(kategori: str, metin: str) -> bool:
    try:
        with open("veri.json", "r", encoding="utf-8") as dosya:
            veri = json.load(dosya)

        veri[kategori].append(metin.strip())

        with open("veri.json", "w", encoding="utf-8") as dosya:
            json.dump(veri, dosya, indent=4, ensure_ascii=False)

        return True
    except Exception as e:
        print(f"[HATA]: {e}")
        return False

# 🔠 Şiir gönderme komutu
@app.on_message(filters.command(["siir", ".siir"]))
async def siir_gonder(client: Client, message: Message):
    try:
        with open("veri.json", "r", encoding="utf-8") as dosya:
            veri = json.load(dosya)
        if not veri["siirler"]:
            return await message.reply_text("📭 Henüz eklenmiş bir şiir yok.")
        await message.reply_text(f"📜 {random.choice(veri['siirler'])}")
    except:
        await message.reply_text("❌ Şiir gönderilemedi.")

# 🔠 Söz gönderme komutu
@app.on_message(filters.command(["soz", ".soz"]))
async def soz_gonder(client: Client, message: Message):
    try:
        with open("veri.json", "r", encoding="utf-8") as dosya:
            veri = json.load(dosya)
        if not veri["sozler"]:
            return await message.reply_text("📭 Henüz eklenmiş bir söz yok.")
        await message.reply_text(f"📝 {random.choice(veri['sozler'])}")
    except:
        await message.reply_text("❌ Söz gönderilemedi.")

# 🛠️ Sadece OWNER_ID şiir ekleyebilir
@app.on_message(filters.command(["siirekle", ".siirekle"]) & filters.private)
async def siir_ekle(client: Client, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply_text("🚫 Bu komutu sadece bot sahibi kullanabilir.")

    metin = message.text.split(None, 1)
    if len(metin) < 2:
        return await message.reply_text("❗ Lütfen eklenecek şiiri girin.\n\nÖrnek: `/siirekle Geceye şiir gibi düştün.`", quote=True)

    if veri_ekle("siirler", metin[1]):
        await message.reply_text("✅ Şiir başarıyla eklendi.")
    else:
        await message.reply_text("❌ Şiir eklenirken bir hata oluştu.")

# 🛠️ Sadece OWNER_ID söz ekleyebilir
@app.on_message(filters.command(["sozekle", ".sozekle"]) & filters.private)
async def soz_ekle(client: Client, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply_text("🚫 Bu komutu sadece bot sahibi kullanabilir.")

    metin = message.text.split(None, 1)
    if len(metin) < 2:
        return await message.reply_text("❗ Lütfen eklenecek sözü girin.\n\nÖrnek: `/sozekle Yalnızlık paylaşılmaz.`", quote=True)

    if veri_ekle("sozler", metin[1]):
        await message.reply_text("✅ Söz başarıyla eklendi.")
    else:
        await message.reply_text("❌ Söz eklenirken bir hata oluştu.")


__MODULE__ = "Şiir & Söz"
__HELP__ = """
**Şiir ve Söz Komutları:**

/siir - Rastgele şiir gönderir  
/soz - Rastgele söz gönderir  

Yalnızca bot sahibi kullanabilir:
/siirekle <şiir> - Yeni şiir ekler  
/sozekle <söz> - Yeni söz ekler
"""
