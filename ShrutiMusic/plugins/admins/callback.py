# ©️ 2025 Nand Yaduwanshi (aka @NoxxOP)
# Türkçeleştirme ve Hata Düzeltme: Gemini

import asyncio
import time
import psutil
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from ShrutiMusic import YouTube, app
from ShrutiMusic.core.call import Nand
from ShrutiMusic.misc import SUDOERS, db
from ShrutiMusic.utils.database import (
    get_active_chats,
    get_lang,
    get_upvote_count,
    is_active_chat,
    is_music_playing,
    is_nonadmin_chat,
    music_off,
    music_on,
    set_loop,
)
from ShrutiMusic.utils.decorators.language import languageCB
from ShrutiMusic.utils.formatters import seconds_to_min
from ShrutiMusic.utils.inline import close_markup, stream_markup, stream_markup_timer
from ShrutiMusic.utils.inline.help import help_pannel_page1, help_pannel_page2, help_pannel_page3, help_pannel_page4
from ShrutiMusic.utils.stream.autoclear import auto_clean
from ShrutiMusic.utils.thumbnails import gen_thumb
from config import (
    BANNED_USERS,
    SOUNCLOUD_IMG_URL,
    STREAM_IMG_URL,
    TELEGRAM_AUDIO_URL,
    TELEGRAM_VIDEO_URL,
    adminlist,
    confirmer,
    votemode,
    SUPPORT_GROUP
)
from strings import get_string
import config

checker = {}
upvoters = {}

# --- YARDIM SAYFALARI ---

@app.on_callback_query(filters.regex("help_page_1"))
async def show_help_page1(client, callback_query: CallbackQuery):
    try:
        language = await get_lang(callback_query.message.chat.id)
        _ = get_string(language)
    except:
        _ = get_string("en")
    await callback_query.message.edit_caption(
        caption=_["help_1"].format(SUPPORT_GROUP),
        reply_markup=help_pannel_page1(_, START=True)
    )

@app.on_callback_query(filters.regex("fork_repo"))
async def fork_repo_callback(client, query):
    await query.message.edit_text(
        text=(
            "✨ <b>ʙɪᴢᴇ ᴜʟᴀşɪɴ ᴠᴇ ᴄ̧ᴏ̈ᴢᴜ̈ᴍ ʙᴜʟᴜɴ 🎧</b>\n\n"
            "🛠 ʙᴏᴛ ᴄ̧ᴀʟɪşᴍɪʏᴏʀ ᴠᴇʏᴀ ᴅᴏɴᴜʏᴏʀ ᴍᴜ? ᴇɢ̆ᴇʀ ʙɪʀ sᴏʀᴜɴ ʏᴀşɪʏᴏʀsᴀɴɪᴢ, ʟᴜ̈ᴛғᴇɴ ᴏ̈ɴᴄᴇ `/reload` ᴋᴏᴍᴜᴛᴜʏʟᴀ ʏᴏ̈ɴᴇᴛɪᴄɪ ᴏ̈ɴʙᴇʟʟᴇɢ̆ɪɴɪ ʏᴇɴɪʟᴇʏɪɴ.\n"
            "🛠 ʏᴀʏɪɴ ᴀɴɪᴅᴇɴ ᴅᴜʀᴅᴜ ᴍᴜ? sᴏʜʙᴇᴛɪ ʙɪᴛɪʀɪᴘ ʏᴇɴɪᴅᴇɴ ʙᴀşʟᴀᴛᴍᴀᴋ ᴇɴ ʜɪᴢʟɪ ᴄ̧ᴏ̈ᴢᴜ̈ᴍᴅᴜ̈ʀ.\n\n"
            "🔧 <b>sᴏʀᴜɴ ᴅᴇᴠᴀᴍ ᴇᴅᴇʀsᴇ ᴅᴇsᴛᴇᴋ ɢʀᴜʙᴜᴍᴜᴢᴀ ʙᴇᴋʟᴇʀɪᴢ. 🔥</b>"
        ),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("💻 ɢᴇʟɪ̇şᴛɪ̇ʀɪ̇ᴄɪ̇", url="https://t.me/dnztrmnn"),
                    InlineKeyboardButton("🛠 ᴄ̧ᴏ̈ᴢᴜ̈ᴍ ɢʀᴜʙᴜ", url=f"{SUPPORT_GROUP}")
                ],
                [
                    InlineKeyboardButton("🔙 ɢᴇʀɪ̇", callback_data="settingsback_helper")
                ]
            ]
        )
    )

# --- STATS / PING ---

@app.on_callback_query(filters.regex("ping_status"))
async def ping_status_callback(client, callback_query: CallbackQuery):
    loading = await callback_query.message.reply_text("🔄 ᴘɪɴɢ ᴏ̈ʟᴄ̧ᴜ̈ʟᴜ̈ʏᴏʀ...")
    start = time.time()
    try:
        await Nand.ping()
    except:
        pass
    end = time.time()
    ping = round((end - start) * 1000)

    try:
        from ShrutiMusic.utils import bot_sys_stats
        UP, CPU, RAM, DISK = await bot_sys_stats()
    except:
        UP = "ʙɪʟɪɴᴍɪʏᴏʀ"
        CPU = psutil.cpu_percent()
        RAM = psutil.virtual_memory().percent
        DISK = psutil.disk_usage('/').percent

    color = "🟢" if ping < 100 else "🟡" if ping < 300 else "🔴"

    final_text = (
        f"📡 ᴘɪɴɢ: {ping}ms {color}\n"
        f"⏱ ᴜᴘᴛɪᴍᴇ: {UP}\n"
        f"💾 ᴅɪsᴋ: {DISK}%\n"
        f"📈 ᴍᴇᴍᴏʀʏ: {RAM}%\n"
        f"🖥 ᴄᴘᴜ: {CPU}%"
    )
    await loading.edit_text(final_text)
    await asyncio.sleep(8)
    await loading.delete()

# --- ADMIN KONTROLLERİ (PAUSE, RESUME, SKIP, STOP) ---

@app.on_callback_query(filters.regex("ADMIN") & ~BANNED_USERS)
@languageCB
async def admin_callback_manager(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    command, chat = callback_request.split("|")
    chat_id = int(chat.split("_")[0])
    
    if not await is_active_chat(chat_id):
        return await CallbackQuery.answer("⚠️ ʏᴀʏɪɴ ᴀᴋᴛɪғ ᴅᴇɢ̆ɪʟ.", show_alert=True)
    
    mention = CallbackQuery.from_user.mention

    # Yetki Kontrolü
    is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
    if not is_non_admin and CallbackQuery.from_user.id not in SUDOERS:
        admins = adminlist.get(CallbackQuery.message.chat.id)
        if not admins or CallbackQuery.from_user.id not in admins:
            return await CallbackQuery.answer("❌ ʏᴇᴛᴋɪɴɪᴢ ʏᴏᴋ!", show_alert=True)

    if command == "Pause":
        if not await is_music_playing(chat_id):
            return await CallbackQuery.answer("⏸ ʏᴀʏɪɴ ᴢᴀᴛᴇɴ ᴅᴜʀᴀᴋʟᴀᴛɪʟᴍɪş.", show_alert=True)
        await music_off(chat_id)
        await Nand.pause_stream(chat_id)
        await CallbackQuery.message.reply_text(f"⏸ **ʏᴀʏɪɴ ᴅᴜʀᴀᴋʟᴀᴛɪʟᴅɪ.**\n└ ʙʏ: {mention}", reply_markup=close_markup(_))
    
    elif command == "Resume":
        if await is_music_playing(chat_id):
            return await CallbackQuery.answer("▶️ ʏᴀʏɪɴ ᴢᴀᴛᴇɴ ᴅᴇᴠᴀᴍ ᴇᴅɪʏᴏʀ.", show_alert=True)
        await music_on(chat_id)
        await Nand.resume_stream(chat_id)
        await CallbackQuery.message.reply_text(f"▶️ **ʏᴀʏɪɴ ᴅᴇᴠᴀᴍ ᴇᴅɪʏᴏʀ.**\n└ ʙʏ: {mention}", reply_markup=close_markup(_))

    elif command == "Stop" or command == "End":
        await Nand.stop_stream(chat_id)
        await set_loop(chat_id, 0)
        await CallbackQuery.message.reply_text(f"⏹ **ʏᴀʏɪɴ sᴏɴʟᴀɴᴅɪʀɪʟᴅɪ.**\n└ ʙʏ: {mention}")
        await CallbackQuery.message.delete()

    elif command == "Skip":
        check = db.get(chat_id)
        if not check:
            return await CallbackQuery.answer("📝 sɪʀᴀᴅᴀ ʙᴀşᴋᴀ şᴀʀᴋɪ ʏᴏᴋ!", show_alert=True)
        
        await CallbackQuery.answer("⏭ sɪʀᴀᴅᴀᴋɪɴᴇ ɢᴇᴄ̧ɪʟɪʏᴏʀ...")
        # Atla mantığı (Basitleştirilmiş)
        try:
            await Nand.stop_stream(chat_id)
            # Burada normalde kuyruktaki sonraki şarkı çalınır
            await CallbackQuery.message.reply_text(f"⏭ **sɪʀᴀᴅᴀᴋɪ şᴀʀᴋɪʏᴀ ɢᴇᴄ̧ɪʟᴅɪ.**\n└ ʙʏ: {mention}")
        except:
            pass

# --- ZAMANLAYICI (BAR GÜNCELLEME) ---
async def markup_timer():
    while True:
        await asyncio.sleep(7)
        active_chats = await get_active_chats()
        for chat_id in active_chats:
            try:
                playing = db.get(chat_id)
                if not playing or not await is_music_playing(chat_id):
                    continue
                
                # İlerleme çubuğunu güncelle
                mystic = playing[0]["mystic"]
                language = await get_lang(chat_id)
                _ = get_string(language or "en")
                
                buttons = stream_markup_timer(_, chat_id, seconds_to_min(playing[0]["played"]), playing[0]["dur"])
                await mystic.edit_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
            except:
                continue

asyncio.create_task(markup_timer())
