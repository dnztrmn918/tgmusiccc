import asyncio
import re
from time import time
from pyrogram import filters, types, enums
from ShrutiMusic import app

user_last_message_time = {}
user_command_count = {}
SPAM_THRESHOLD = 2
SPAM_WINDOW_SECONDS = 5

async def userstatus(user_id):
    try:
        user = await app.get_users(user_id)
        status = user.status
        if status == enums.UserStatus.RECENTLY:
            return "ʏᴀᴋɪɴʟᴀʀᴅᴀ ᴀᴋᴛɪғ"
        elif status == enums.UserStatus.LAST_WEEK:
            return "ɢᴇᴄ̧ᴇɴ ʜᴀғᴛᴀ ᴀᴋᴛɪғ"
        elif status == enums.UserStatus.LONG_AGO:
            return "ᴜᴢᴜɴ ᴢᴀᴍᴀɴ ᴏ̈ɴᴄᴇ"
        elif status == enums.UserStatus.OFFLINE:
            return "ᴄ̧ɪᴠʀɪᴍᴅɪşɪ"
        elif status == enums.UserStatus.ONLINE:
            return "şᴜ ᴀɴ ᴄ̧ɪᴠʀɪᴍɪᴄ̧ɪ 🟢"
        else:
            return "ʙɪʟɪɴᴍɪʏᴏʀ"
    except:
        return "ʙɪʟɪɴᴍɪʏᴏʀ"

INFO_CAPTION = """
<b>👤 ᴋᴜʟʟᴀɴɪᴄɪ ʙɪʟɢɪʟᴇʀɪ</b>

<b>🆔 ɪᴅ:</b> <code>{}</code>
<b>👨‍💻 ɪ̇sɪᴍ:</b> {}
<b>🏷 ᴜsᴇʀɴᴀᴍᴇ:</b> {}
<b>🔗 ᴍᴇɴᴛɪᴏɴ:</b> {}
<b>📡 ᴅᴄ ɪᴅ:</b> {}
<b>💎 ᴘʀᴇᴍɪᴜᴍ:</b> {}
<b>💬 ʙɪᴏ:</b> {}
<b>👥 ᴏʀᴛᴀᴋ ɢʀᴜᴘʟᴀʀ:</b> {}
<b>📶 ᴅᴜʀᴜᴍ:</b> {}

•── ⋅ ⋅ ⋅ ───────── ⋅ • ⋅ ──•
🛠 <b>sᴏʀᴜɴ ᴠᴀʀsᴀ ᴄ̧ᴏ̈ᴢᴜ̈ᴍ ɢʀᴜʙᴜɴᴀ ᴜʟᴀşɪɴ.</b>
"""

@app.on_message(filters.command(["info", "userinfo", "bilgi"], prefixes=["/", "!", "."]))
async def userinfo(_, message):
    user_id = message.from_user.id
    current_time = time()

    # Spam Kontrolü
    last_message_time = user_last_message_time.get(user_id, 0)
    if current_time - last_message_time < SPAM_WINDOW_SECONDS:
        user_command_count[user_id] = user_command_count.get(user_id, 0) + 1
        if user_command_count[user_id] > SPAM_THRESHOLD:
            warn = await message.reply_text(f"⚠️ {message.from_user.mention}, **sᴘᴀᴍ ʏᴀᴘᴍᴀʏɪɴ. ʙɪʀᴀᴢ ʙᴇᴋʟᴇʏɪɴ.**")
            await asyncio.sleep(3)
            return await warn.delete()
    else:
        user_command_count[user_id] = 1
        user_last_message_time[user_id] = current_time

    # Hedef Kullanıcı Belirleme
    if message.reply_to_message:
        target = message.reply_to_message.from_user
    elif len(message.command) > 1:
        try:
            target = await app.get_users(message.text.split(None, 1)[1])
        except Exception as e:
            return await message.reply_text(f"⚠️ **ʜᴀᴛᴀ:** `ᴋᴜʟʟᴀɴɪᴄɪ ʙᴜʟᴜɴᴀᴍᴀᴅɪ`")
    else:
        target = message.from_user

    try:
        user_info = await app.get_chat(target.id)
        status = await userstatus(target.id)

        user_id = target.id
        name = f"{user_info.first_name or ''} {user_info.last_name or ''}".strip() or "ɪ̇sɪᴍsɪᴢ"
        username = f"@{user_info.username}" if user_info.username else "ʏᴏᴋ"
        mention = target.mention
        dc_id = getattr(target, "dc_id", "ʙɪʟɪɴᴍɪʏᴏʀ")
        premium = "✅ ᴇᴠᴇᴛ" if getattr(target, "is_premium", False) else "❌ ʜᴀʏɪʀ"

        # Bio Filtreleme
        bio_raw = user_info.bio or ""
        if not bio_raw:
            bio = "ʙɪᴏ ʏᴏᴋ"
        elif re.search(r"(t\.me|https?://|@)", bio_raw, re.IGNORECASE):
            bio = "🔒 **ɢɪᴢʟᴇɴᴅɪ** (ʟɪɴᴋ/ᴇᴛɪᴋᴇᴛ ɪᴄ̧ᴇʀɪʏᴏʀ)"
        else:
            bio = bio_raw

        try:
            mutual_chats = await app.get_common_chats(target.id)
            mutual_count = len(mutual_chats)
        except:
            mutual_count = "ᴇʀɪşɪʟᴇᴍᴇᴅɪ"

        caption = INFO_CAPTION.format(
            user_id, name, username, mention, dc_id, premium, bio, mutual_count, status
        )

        btn = [[types.InlineKeyboardButton("🌐 ᴘʀᴏғɪʟɪ ɢᴏ̈ʀ", url=f"https://t.me/{target.username}" if target.username else "https://t.me/")] ]

        await message.reply_text(
            caption,
            reply_markup=types.InlineKeyboardMarkup(btn),
            disable_web_page_preview=True,
        )

    except Exception as e:
        await message.reply_text(f"❌ **ʙɪʀ ʜᴀᴛᴀ ᴏʟᴜşᴛᴜ:** `{e}`")

__MODULE__ = "ʙɪʟɢɪ"
__HELP__ = """
● `/info` - ᴋᴇɴᴅɪ ʙɪʟɢɪʟᴇʀɪɴɪᴢɪ ɢᴏ̈sᴛᴇʀɪʀ.
● `/info [ʏᴀɴɪᴛ]` - ʏᴀɴɪᴛʟᴀɴᴀɴ ᴋɪşɪɴɪɴ ʙɪʟɢɪʟᴇʀɪɴɪ ᴠᴇʀɪʀ.
● `/info [ᴜsᴇʀɴᴀᴍᴇ/ɪᴅ]` - ʙᴇʟɪʀᴛɪʟᴇɴ ᴋɪşɪɴɪɴ ʙɪʟɢɪʟᴇʀɪɴɪ ᴠᴇʀɪʀ.
"""
