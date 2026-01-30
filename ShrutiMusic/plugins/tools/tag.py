# ©️ 2025 Nand Yaduwanshi (aka @NoxxOP)
# Modified by Gemini for dnztrmnn
# All rights reserved.

import asyncio
from pyrogram import filters
from pyrogram.enums import ChatMembersFilter, ParseMode
from pyrogram.errors import FloodWait
import re

from ShrutiMusic import app

SPAM_CHATS = []

def clean_text(text):
    """Markdown karakterlerini temizler"""
    if not text:
        return ""
    return re.sub(r'([_*\[\]()~`>#+-=|{}.!])', r'\\1', text)

async def is_admin(chat_id, user_id):
    try:
        admin_ids = [
            admin.user.id
            async for admin in app.get_chat_members(
                chat_id, filter=ChatMembersFilter.ADMINISTRATORS
            )
        ]
        return user_id in admin_ids
    except:
        return False

@app.on_message(
    filters.command(["tag", "all", "tagall", "allmention"], prefixes=["/", "@"])
)
async def tag_all_users(_, message):
    chat_id = message.chat.id
    
    # Yönetici kontrolü
    admin = await is_admin(chat_id, message.from_user.id)
    if not admin:
        return await message.reply_text("⛔ **ʙᴜ ᴋᴏᴍᴜᴛᴜ sᴀᴅᴇᴄᴇ ʏᴏ̈ɴᴇᴛɪᴄɪʟᴇʀ ᴋᴜʟʟᴀɴᴀʙɪʟɪʀ.**")

    # Zaten çalışıyor mu kontrolü
    if chat_id in SPAM_CHATS:  
        return await message.reply_text("⚠️ **ᴇᴛɪ̇ᴋᴇᴛʟᴇᴍᴇ ɪ̇şʟᴇᴍɪ̇ ᴢᴀᴛᴇɴ ᴅᴇᴠᴀᴍ ᴇᴅɪ̇ʏᴏʀ.**\n\nᴅᴜʀᴅᴜʀᴍᴀᴋ ɪ̇ᴄ̧ɪ̇ɴ: `/cancel`")  
    
    # Mesaj içeriği kontrolü
    replied = message.reply_to_message  
    if len(message.command) < 2 and not replied:  
        return await message.reply_text("💬 **ʟᴜ̈ᴛғᴇɴ ᴇᴛɪ̇ᴋᴇᴛ ʏᴀɴɪɴᴀ ʙɪ̇ʀ ᴍᴇsᴀᴊ ʏᴀᴢɪɴ.**\n\nᴏ̈ʀɴᴇᴋ: `/tag Herkes kurda`")  
    
    # Etiket mesajını hazırla
    tag_msg = clean_text(message.text.split(None, 1)[1]) if not replied else ""
    
    try:  
        SPAM_CHATS.append(chat_id)
        members = []
        async for m in app.get_chat_members(chat_id):
            if not m.user.is_bot and not m.user.is_deleted:
                members.append(m)
        
        total_members = len(members)
        tagged_count = 0

        for member in members:
            if chat_id not in SPAM_CHATS: # İptal edildiyse durdur
                break
            
            # Kullanıcıyı isminden etiketle + yanına senin mesajını ekle
            mention = f"[{member.user.first_name}](tg://user?id={member.user.id})"
            full_text = f"{mention} {tag_msg}"
            
            try:
                if replied:
                    await replied.reply_text(full_text, parse_mode=ParseMode.MARKDOWN)
                else:
                    await app.send_message(chat_id, full_text, parse_mode=ParseMode.MARKDOWN)
                
                tagged_count += 1
                await asyncio.sleep(2.5) # Spam filtresine takılmamak için bekleme süresi
                
            except FloodWait as e:
                await asyncio.sleep(e.value + 2)
            except Exception:
                continue

        # İşlem bitiş özeti
        if chat_id in SPAM_CHATS:
            summary = f"✅ **ᴇᴛɪ̇ᴋᴇᴛʟᴇᴍᴇ ᴛᴀᴍᴀᴍʟᴀɴᴅɪ!**\n\n📊 **ᴛᴏᴘʟᴀᴍ:** {total_members}\n✨ **ᴇᴛɪ̇ᴋᴇᴛʟᴇɴᴇɴ:** {tagged_count}"
            await app.send_message(chat_id, summary)

    except Exception as e:  
        await app.send_message(chat_id, f"❌ **ʜᴀᴛᴀ:** {str(e)}")  
    finally:  
        if chat_id in SPAM_CHATS:
            SPAM_CHATS.remove(chat_id)

@app.on_message(filters.command(["cancel", "stopmention"], prefixes=["/", "@"]))
async def cancel_tag(_, message):
    chat_id = message.chat.id
    admin = await is_admin(chat_id, message.from_user.id)
    if not admin:
        return await message.reply_text("⛔ **ʏᴇᴛᴋɪɴɪᴢ ʏᴏᴋ.**")

    if chat_id in SPAM_CHATS:  
        SPAM_CHATS.remove(chat_id)
        return await message.reply_text("🛑 **ᴇᴛɪ̇ᴋᴇᴛʟᴇᴍᴇ ᴅᴜʀᴅᴜʀᴜʟᴅɪ.**")  
    else:  
        return await message.reply_text("❓ **ᴄ̧ᴀʟɪşᴀɴ ʙɪ̇ʀ ɪ̇şʟᴇᴍ ʏᴏᴋ.**")

# Modül bilgileri
MODULE = "ᴛᴀɢᴀʟʟ"
HELP = """
✨ **ᴇᴛɪ̇ᴋᴇᴛ ᴍᴏᴅᴜ̈ʟᴜ̈**

● `/tag [ᴍᴇsᴀᴊ]` - ᴜ̈ʏᴇʟᴇʀɪ ᴛᴇᴋᴇʀ ᴛᴇᴋᴇʀ ɪ̇sɪᴍʟᴇʀɪʏʟᴇ ᴠᴇ ᴍᴇsᴀᴊɪɴɪᴢʟᴀ ᴇᴛɪᴋᴇᴛʟᴇʀ.
● `/cancel` - ɪ̇şʟᴇᴍɪ ᴅᴜʀᴅᴜʀᴜʀ.

⚠️ **ɴᴏᴛ:** ʜᴇʀ ᴇᴛɪᴋᴇᴛ ᴀʀᴀsɪɴᴅᴀ 2.5 sᴀɴɪʏᴇ ʙᴇᴋʟᴇʀ (ʙᴏᴛᴜɴ ᴇɴɢᴇʟ ʏᴇᴍᴇᴍᴇsɪ ɪᴄ̧ɪɴ).
"""
