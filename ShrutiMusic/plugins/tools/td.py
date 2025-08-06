# -*- coding: utf-8 -*-
# 📁 dogruluk_cesaret.py

import json
import random
from pyrogram import Client, filters
from ShrutiMusic import app  # bot instance

# JSON dosyası yolu
JSON_DOSYA = "truth_dare.json"

# JSON dosyasını kontrol et / oluştur
def veri_kontrol_et():
    try:
        with open(JSON_DOSYA, "r", encoding="utf-8") as f:
            json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        with open(JSON_DOSYA, "w", encoding="utf-8") as f:
            json.dump({"dogruluk": [], "cesaret": []}, f, indent=4, ensure_ascii=False)

veri_kontrol_et()

# JSON'dan rastgele veri çek
def rastgele_soru(kategori: str) -> str:
    try:
        with open(JSON_DOSYA, "r", encoding="utf-8") as f:
            veri = json.load(f)

        if not veri.get(kategori):
            return None

        return random.choice(veri[kategori])
    except Exception as e:
        print(f"[HATA]: {e}")
        return None

# /t → Doğruluk
@app.on_message(filters.command(["t"]))
async def dogruluk_gonder(client, message):
    soru = rastgele_soru("dogruluk")
    if not soru:
        return await message.reply_text("📭 Henüz eklenmiş bir doğruluk sorusu yok.")
    await message.reply_text(f"🎯 **Doğruluk Sorusu:**\n\n{soru}")

# /c → Cesaret
@app.on_message(filters.command(["c"]))
async def cesaret_gonder(client, message):
    gorev = rastgele_soru("cesaret")
    if not gorev:
        return await message.reply_text("📭 Henüz eklenmiş bir cesaret görevi yok.")
    await message.reply_text(f"🔥 **Cesaret Görevi:**\n\n{gorev}")

# JSON'a veri ekleme (sadece bot sahibi ekleyebilir istersen buraya OWNER_ID ekleyebilirsin)
def veri_ekle(kategori: str, metin: str) -> bool:
    try:
        with open(JSON_DOSYA, "r", encoding="utf-8") as f:
            veri = json.load(f)

        veri[kategori].append(metin)

        with open(JSON_DOSYA, "w", encoding="utf-8") as f:
            json.dump(veri, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[HATA]: {e}")
        return False

# /te ekleme komutu → doğruluk
@app.on_message(filters.command(["te"]))
async def dogruluk_ekle(client, message):
    try:
        soru = message.text.split(None, 1)[1]
    except IndexError:
        return await message.reply_text("❗ Lütfen eklenecek doğruluk sorusunu girin.\n`/te <soru>`")

    if veri_ekle("dogruluk", soru.strip()):
        await message.reply_text("✅ Doğruluk sorusu başarıyla eklendi.")
    else:
        await message.reply_text("❌ Doğruluk sorusu eklenemedi.")

# /ce ekleme komutu → cesaret
@app.on_message(filters.command(["ce"]))
async def cesaret_ekle(client, message):
    try:
        gorev = message.text.split(None, 1)[1]
    except IndexError:
        return await message.reply_text("❗ Lütfen eklenecek cesaret görevini girin.\n`/ce <görev>`")

    if veri_ekle("cesaret", gorev.strip()):
        await message.reply_text("✅ Cesaret görevi başarıyla eklendi.")
    else:
        await message.reply_text("❌ Cesaret görevi eklenemedi.")

__HELP__ = """
**🎲 Doğruluk & Cesaret Komutları**

/t → Rastgele doğruluk sorusu gönderir  
/c → Rastgele cesaret görevi gönderir  

📌 **Ekleme Komutları (Bot Sahibi İçin)**  
/te <soru> → Doğruluk sorusu ekler  
/ce <görev> → Cesaret görevi ekler  
"""

__MODULE__ = "🎲 Doğruluk & Cesaret"
