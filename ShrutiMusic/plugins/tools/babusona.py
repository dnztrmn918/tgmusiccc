# -*- coding: utf-8 -*-
# 📁 siir_soz.py

import json
import random
from pyrogram import Client, filters
from pyrogram.types import Message
from ShrutiMusic import app  # bot instance
from config import OWNER_ID  # sudo kontrolü için

KANAL = "@tubidymusic"

# JSON dosyasından rastgele veri çekmek için
def veri_kontrol_et():
    try:
        with open("veri.json", "r", encoding="utf-8") as f:
            json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        with open("veri.json", "w", encoding="utf-8") as f:
            json.dump({"siirler": [], "sozler": []}, f, indent=4, ensure_ascii=False)

veri_kontrol_et()

# JSON'a veri ekleme (metin dict formatında: {'metin':..., 'yazar':...})
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

# 🔠 Şiir gönderme komutu
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
        cevap = f"📜 {metin}\n\n— {yazar}\n\n📢 Paylaşım Kanalı: {KANAL}"
        await message.reply_text(cevap)
    except Exception as e:
        await message.reply_text("❌ Şiir gönderilemedi.")

# 🔠 Söz gönderme komutu
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
        cevap = f"📝 {metin}\n\n— {yazar}\n\n📢 Paylaşım Kanalı: {KANAL}"
        await message.reply_text(cevap)
    except Exception as e:
        await message.reply_text("❌ Söz gönderilemedi.")

# 🛠️ Sadece OWNER_ID şiir ekleyebilir
@app.on_message(filters.command(["siirekle", ".siirekle"]) & filters.private)
async def siir_ekle(client: Client, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply_text("🚫 Bu komutu sadece bot sahibi kullanabilir.")

    metin = message.text.split(None, 2)
    if len(metin) < 3:
        return await message.reply_text(
            "❗ Lütfen eklenecek şiiri ve yazarını girin.\n\n"
            "Örnek: `/siirekle Geceye şiir gibi düştün. Nazım Hikmet`", quote=True)

    metin_dict = {
        "metin": metin[1].strip(),
        "yazar": metin[2].strip()
    }

    if veri_ekle("siirler", metin_dict):
        await message.reply_text("✅ Şiir başarıyla eklendi.")
    else:
        await message.reply_text("❌ Şiir eklenirken bir hata oluştu.")

# 🛠️ Sadece OWNER_ID söz ekleyebilir
@app.on_message(filters.command(["sozekle", ".sozekle"]) & filters.private)
async def soz_ekle(client: Client, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply_text("🚫 Bu komutu sadece bot sahibi kullanabilir.")

    metin = message.text.split(None, 2)
    if len(metin) < 3:
        return await message.reply_text(
            "❗ Lütfen eklenecek sözü ve yazarını girin.\n\n"
            "Örnek: `/sozekle Yalnızlık paylaşılmaz. Mevlana`", quote=True)

    metin_dict = {
        "metin": metin[1].strip(),
        "yazar": metin[2].strip()
    }

    if veri_ekle("sozler", metin_dict):
        await message.reply_text("✅ Söz başarıyla eklendi.")
    else:
        await message.reply_text("❌ Söz eklenirken bir hata oluştu.")


__MODULE__ = "Şiir & Söz"
__HELP__ = """
**Şiir ve Söz Komutları:**

/siir - Rastgele şiir gönderir  
/soz - Rastgele söz gönderir  

Yalnızca bot sahibi kullanabilir:  
/siirekle <şiir> <yazar> - Yeni şiir ekler  
/sozekle <söz> <yazar> - Yeni söz ekler
"""
