# -*- coding: utf-8 -*-
# 📁 siir_soz.py

import json
import random
from pyrogram import Client, filters
from pyrogram.types import Message
from ShrutiMusic import app  # bot instance
from config import OWNER_ID  # sudo kontrolü için

# JSON dosyasını kontrol et veya oluştur
def veri_kontrol_et():
    try:
        with open("veri.json", "r", encoding="utf-8") as f:
            json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        with open("veri.json", "w", encoding="utf-8") as f:
            # örnek yapıda paylasim_kanali da ekledim
            json.dump({"siirler": [], "sozler": [], "paylasim_kanali": "t.me/tubidymusic"}, f, indent=4, ensure_ascii=False)

veri_kontrol_et()

# JSON'a veri ekleme fonksiyonu
def veri_ekle(kategori: str, veri_icerik: dict) -> bool:
    try:
        with open("veri.json", "r", encoding="utf-8") as dosya:
            veri = json.load(dosya)

        veri[kategori].append(veri_icerik)

        with open("veri.json", "w", encoding="utf-8") as dosya:
            json.dump(veri, dosya, indent=4, ensure_ascii=False)

        return True
    except Exception as e:
        print(f"[HATA]: {e}")
        return False

# Şiir gönderme komutu
@app.on_message(filters.command(["siir", ".siir"]))
async def siir_gonder(client: Client, message: Message):
    try:
        with open("veri.json", "r", encoding="utf-8") as dosya:
            veri = json.load(dosya)

        if not veri["siirler"]:
            return await message.reply_text("📭 Henüz eklenmiş bir şiir yok.")

        siir = random.choice(veri["siirler"])
        kanal = veri.get("paylasim_kanali", "t.me/tubidymusic")

        metin = (
            f"💫 İşte senin için seçtiğim özel bir şiir:\n\n"
            f"{siir['metin']}\n\n"
            f"— {siir['yazar']}\n\n"
            f"Paylaşım Kanalımız: {kanal}"
        )

        await message.reply_text(metin)
    except Exception:
        await message.reply_text("❌ Şiir gönderilemedi.")

# Söz gönderme komutu
@app.on_message(filters.command(["soz", ".soz"]))
async def soz_gonder(client: Client, message: Message):
    try:
        with open("veri.json", "r", encoding="utf-8") as dosya:
            veri = json.load(dosya)

        if not veri["sozler"]:
            return await message.reply_text("📭 Henüz eklenmiş bir söz yok.")

        soz = random.choice(veri["sozler"])
        kanal = veri.get("paylasim_kanali", "t.me/tubidymusic")

        metin = (
            f"✨ İşte senin için anlam dolu bir söz:\n\n"
            f"\"{soz['metin']}\"\n\n"
            f"— {soz['yazar']}\n\n"
            f"Paylaşım Kanalımız: {kanal}"
        )

        await message.reply_text(metin)
    except Exception:
        await message.reply_text("❌ Söz gönderilemedi.")

# Sadece OWNER_ID şiir ekleyebilir
@app.on_message(filters.command(["siirekle", ".siirekle"]) & filters.private)
async def siir_ekle(client: Client, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply_text("🚫 Bu komutu sadece bot sahibi kullanabilir.")

    metin = message.text.split(None, 1)
    if len(metin) < 2:
        return await message.reply_text(
            "❗ Lütfen eklenecek şiiri ve yazarı girin. Örnek:\n"
            "/siirekle {'metin': 'Geceye şiir gibi düştün.', 'yazar': 'Nazım Hikmet'}",
            quote=True
        )

    try:
        veri_dict = json.loads(metin[1].replace("'", '"'))
    except Exception:
        return await message.reply_text("❗ Lütfen JSON formatında ve düzgün yazın.", quote=True)

    if "metin" not in veri_dict or "yazar" not in veri_dict:
        return await message.reply_text("❗ 'metin' ve 'yazar' alanları zorunludur.", quote=True)

    if veri_ekle("siirler", veri_dict):
        await message.reply_text("✅ Şiir başarıyla eklendi.")
    else:
        await message.reply_text("❌ Şiir eklenirken bir hata oluştu.")

# Sadece OWNER_ID söz ekleyebilir
@app.on_message(filters.command(["sozekle", ".sozekle"]) & filters.private)
async def soz_ekle(client: Client, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply_text("🚫 Bu komutu sadece bot sahibi kullanabilir.")

    metin = message.text.split(None, 1)
    if len(metin) < 2:
        return await message.reply_text(
            "❗ Lütfen eklenecek sözü ve yazarı girin. Örnek:\n"
            "/sozekle {'metin': 'Yalnızlık paylaşılmaz.', 'yazar': 'Hz. Mevlana'}",
            quote=True
        )

    try:
        veri_dict = json.loads(metin[1].replace("'", '"'))
    except Exception:
        return await message.reply_text("❗ Lütfen JSON formatında ve düzgün yazın.", quote=True)

    if "metin" not in veri_dict or "yazar" not in veri_dict:
        return await message.reply_text("❗ 'metin' ve 'yazar' alanları zorunludur.", quote=True)

    if veri_ekle("sozler", veri_dict):
        await message.reply_text("✅ Söz başarıyla eklendi.")
    else:
        await message.reply_text("❌ Söz eklenirken bir hata oluştu.")


__MODULE__ = "Şiir & Söz"
__HELP__ = """
**Şiir ve Söz Komutları:**

/siir - Rastgele şiir gönderir  
/soz - Rastgele söz gönderir  

Yalnızca bot sahibi kullanabilir:  
/siirekle <JSON formatında şiir> - Yeni şiir ekler  
/sozekle <JSON formatında söz> - Yeni söz ekler

Örnek:  
/siirekle {'metin': 'Geceye şiir gibi düştün.', 'yazar': 'Nazım Hikmet'}  
/sozekle {'metin': 'Yalnızlık paylaşılmaz.', 'yazar': 'Hz. Mevlana'}
"""
