# ©️ 2025 Nand Yaduwanshi (aka @NoxxOP)
# Türkçeleştirme ve Düzenleme: Gemini

import io
from gtts import gTTS
from pyrogram import filters
from ShrutiMusic import app

@app.on_message(filters.command(["tts", "seslendir"]))
async def text_to_speech(client, message):
    if len(message.command) < 2:
        return await message.reply_text(
            "❌ **ʟᴜ̈ᴛғᴇɴ sᴇsᴇ ᴅᴏ̈ɴᴜ̈şᴛᴜ̈ʀᴜ̈ʟᴇᴄᴇᴋ ʙɪʀ ᴍᴇᴛɪɴ ʏᴀᴢɪɴ.**\n\nᴏ̈ʀɴᴇᴋ: `/tts Merhaba nasılsın?`"
        )

    # İşlem başladığını belirten küçük bir emoji
    m = await message.reply_text("⏳ **sᴇs ᴅᴏsʏᴀsɪ ʜᴀᴢɪʀʟᴀɴɪʏᴏʀ...**")

    try:
        text = message.text.split(None, 1)[1]
        # Dil 'tr' (Türkçe) olarak güncellendi
        tts = gTTS(text, lang="tr")
        audio_data = io.BytesIO()
        tts.write_to_fp(audio_data)
        audio_data.seek(0)

        audio_file = io.BytesIO(audio_data.read())
        audio_file.name = "dnz_ses.mp3"
        
        await message.reply_audio(
            audio_file, 
            caption=f"✨ **ᴍᴇᴛɪɴ ʙᴀşᴀʀɪʏʟᴀ sᴇsᴇ ᴄ̧ᴇᴠɪʀɪʟᴅɪ!**\n\n🎙️ **sᴇsʟᴇɴᴅɪʀɪʟᴇɴ:** `{text[:50]}...`"
        )
        await m.delete()

    except Exception as e:
        await m.edit(f"❌ **ʙɪʀ ʜᴀᴛᴀ ᴏʟᴜşᴛᴜ:** `{e}`")

__HELP__ = """
🎙️ **ᴛᴛs (ᴍᴇᴛɴɪ sᴇsᴇ ᴄ̧ᴇᴠɪ̇ʀᴍᴇ) ᴋᴏᴍᴜᴛʟᴀʀɪ**

ᴍᴇᴛɪɴʟᴇʀɪ ᴛᴜ̈ʀᴋᴄ̧ᴇ sᴇs ᴅᴏsʏᴀsɪɴᴀ ᴅᴏ̈ɴᴜ̈şᴛᴜ̈ʀᴍᴇᴋ ɪᴄ̧ɪɴ ᴋᴜʟʟᴀɴɪʟɪʀ.

● `/tts <ᴍᴇᴛɪɴ>` - ʏᴀᴢᴅɪɢ̆ɪɴɪᴢ ᴍᴇᴛɴɪ sᴇsᴇ ᴄ̧ᴇᴠɪʀɪᴘ ɢᴏ̈ɴᴅᴇʀɪʀ.
● `/seslendir <ᴍᴇᴛɪɴ>` - ᴀʏɴɪ ɪ̇şʟᴇᴍɪ ʏᴀᴘᴀʀ.

**ᴏ̈ʀɴᴇᴋ:**
- `/tts Selam grup, müzik keyfiniz bol olsun!`

⚠️ **ɴᴏᴛ:** ᴄ̧ᴏ̈ᴢᴜ̈ᴍ ɢʀᴜʙᴜ ᴅᴇsᴛᴇɢ̆ɪ ɪ̇ʟᴇ ʜᴇʀ ᴢᴀᴍᴀɴ ᴀᴋᴛɪғ!
"""

__MODULE__ = "ᴛᴛs"
