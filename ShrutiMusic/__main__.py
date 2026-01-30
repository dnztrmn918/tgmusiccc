# Copyright (c) 2025 Nand Yaduwanshi <NoxxOP>
# Location: Supaul, Bihar
#
# All rights reserved.
#
# This code is the intellectual property of Nand Yaduwanshi.
# You are not allowed to copy, modify, redistribute, or use this
# code for commercial or personal projects without explicit permission.
#
# Allowed:
# - Forking for personal learning
# - Submitting improvements via pull requests
#
# Not Allowed:
# - Claiming this code as your own
# - Re-uploading without credit or permission
# - Selling or using commercially
#
# Contact for permissions:
# Email: badboy809075@gmail.com


import asyncio
import importlib
from pyrogram import idle
from pyrogram.types import BotCommand
from pytgcalls.exceptions import NoActiveGroupCall
import config
from ShrutiMusic import LOGGER, app, userbot
from ShrutiMusic.core.call import Nand
from ShrutiMusic.misc import sudo
from ShrutiMusic.plugins import ALL_MODULES
from ShrutiMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS

COMMANDS = [
    BotCommand("start", "❖ ʙᴏᴛᴜ ʙᴀşʟᴀᴛ • ʙᴏᴛᴜ çᴀʟışᴛıʀᴍᴀᴋ İçɪɴ"),
    BotCommand("help", "❖ ʏᴀʀᴅıᴍ ᴍᴇɴüꜱü • ᴛüᴍ ᴋᴏᴍᴜᴛʟᴀʀ ᴠᴇ ʏöɴᴇᴛɪᴍ"),
    BotCommand("ping", "❖ ʙᴏᴛ ɢᴇᴄɪᴋᴍᴇꜱɪ • ᴘɪɴɢ ᴠᴇ ꜱɪꜱᴛᴇᴍ İꜱᴛᴀᴛɪꜱᴛɪᴋʟᴇʀɪ"),
    BotCommand("play", "❖ ꜱᴇꜱʟɪᴅᴇ ᴏʏɴᴀᴛ • ꜱᴇꜱʟɪ ꜱᴏʜʙᴇᴛᴛᴇ ᴍüᴢɪᴋ çᴀʟᴍᴀᴋ İçɪɴ"),
    BotCommand("vplay", "❖ ꜱᴇꜱʟɪᴅᴇ ᴠɪᴅᴇᴏ • ꜱᴇꜱʟɪ ꜱᴏʜʙᴇᴛᴛᴇ ᴠɪᴅᴇᴏ ᴏʏɴᴀᴛᴍᴀᴋ İçɪɴ"),
    BotCommand("playrtmps", "❖ ᴄᴀɴʟı ʏᴀʏıɴ • ᴄᴀɴʟı ᴠɪᴅᴇᴏ İçᴇʀɪğɪɴɪ ʏᴀʏıɴʟᴀ"),
    BotCommand("playforce", "❖ ᴢᴏʀʟᴀ ᴏʏɴᴀᴛ • ᴍᴇᴠᴄᴜᴛ ꜱᴇꜱɪ ᴅᴜʀᴅᴜʀᴜᴘ ᴢᴏʀʟᴀ çᴀʟ"),
    BotCommand("vplayforce", "❖ ᴢᴏʀʟᴀ ᴠɪᴅᴇᴏ • ᴍᴇᴠᴄᴜᴛ ᴠɪᴅᴇᴏʏᴜ ᴅᴜʀᴅᴜʀᴜᴘ ᴢᴏʀʟᴀ çᴀʟ"),
    BotCommand("pause", "❖ ʏᴀʏıɴı ᴅᴜʀᴀᴋʟᴀᴛ • ᴍᴇᴠᴄᴜᴛ ᴀᴋışı ᴅᴜʀᴅᴜʀ"),
    BotCommand("resume", "❖ ʏᴀʏıɴᴀ ᴅᴇᴠᴀᴍ ᴇᴛ • ᴅᴜʀᴀᴋʟᴀᴛıʟᴀɴ ᴀᴋışı ʙᴀşʟᴀᴛ"),
    BotCommand("skip", "❖ ᴘᴀʀçᴀʏı ᴀᴛʟᴀ • ꜱıʀᴀᴅᴀᴋɪ ᴘᴀʀçᴀʏᴀ ɢᴇç"),
    BotCommand("end", "❖ ʏᴀʏıɴı ʙɪᴛɪʀ • ᴍᴇᴠᴄᴜᴛ ᴀᴋışı ᴛᴀᴍᴀᴍᴇɴ ᴅᴜʀᴅᴜʀ"),
    BotCommand("stop", "❖ ʏᴀʏıɴı ᴅᴜʀᴅᴜʀ • ᴍᴇᴠᴄᴜᴛ ᴀᴋışı ᴋᴇꜱ"),
    BotCommand("queue", "❖ ꜱıʀᴀʏı ɢöꜱᴛᴇʀ • çᴀʟᴍᴀ ʟɪꜱᴛᴇꜱɪɴɪ ɢöʀüɴᴛüʟᴇ"),
    BotCommand("auth", "❖ ʏᴇᴛᴋɪ ᴇᴋʟᴇ • ᴋᴜʟʟᴀɴıᴄıʏı ʏᴇᴛᴋɪʟɪ ʟɪꜱᴛᴇꜱɪɴᴇ ᴇᴋʟᴇ"),
    BotCommand("unauth", "❖ ʏᴇᴛᴋɪ ᴋᴀʟᴅıʀ • ᴋᴜʟʟᴀɴıᴄıʏı ʏᴇᴛᴋɪʟɪ ʟɪꜱᴛᴇꜱɪɴᴅᴇɴ çıᴋᴀʀ"),
    BotCommand("authusers", "❖ ʏᴇᴛᴋɪʟɪ ʟɪꜱᴛᴇꜱɪ • ᴛüᴍ ʏᴇᴛᴋɪʟɪ ᴋᴜʟʟᴀɴıᴄıʟᴀʀı ɢöꜱᴛᴇʀ"),
    BotCommand("cplay", "❖ ᴋᴀɴᴀʟᴅᴀ ᴏʏɴᴀᴛ • ᴋᴀɴᴀʟᴅᴀ ꜱᴇꜱ çᴀʟᴍᴀᴋ İçɪɴ"),
    BotCommand("cvplay", "❖ ᴋᴀɴᴀʟᴅᴀ ᴠɪᴅᴇᴏ • ᴋᴀɴᴀʟᴅᴀ ᴠɪᴅᴇᴏ ᴏʏɴᴀᴛᴍᴀᴋ İçɪɴ"),
    BotCommand("cplayforce", "❖ ᴋᴀɴᴀʟᴅᴀ ᴢᴏʀʟᴀ ᴏʏɴᴀᴛ • ᴋᴀɴᴀʟᴅᴀ ᴢᴏʀʟᴀ ꜱᴇꜱ çᴀʟᴍᴀᴋ İçɪɴ"),
    BotCommand("cvplayforce", "❖ ᴋᴀɴᴀʟᴅᴀ ᴢᴏʀʟᴀ ᴠɪᴅᴇᴏ • ᴋᴀɴᴀʟᴅᴀ ᴢᴏʀʟᴀ ᴠɪᴅᴇᴏ çᴀʟᴍᴀᴋ İçɪɴ"),
    BotCommand("channelplay", "❖ ᴋᴀɴᴀʟᴀ ʙᴀğʟᴀɴ • ɢʀᴜʙᴜ ʙɪʀ ᴋᴀɴᴀʟᴀ ʙᴀğʟᴀ"),
    BotCommand("loop", "❖ ᴅöɴɢü ᴍᴏᴅᴜ • ᴅöɴɢüʏü ᴀç ᴠᴇʏᴀ ᴋᴀᴘᴀᴛ"),
    BotCommand("stats", "❖ ʙᴏᴛ İꜱᴛᴀᴛɪꜱᴛɪᴋʟᴇʀɪ • ʙᴏᴛ ᴠᴇʀɪʟᴇʀɪɴɪ ɢöꜱᴛᴇʀ"),
    BotCommand("shuffle", "❖ ꜱıʀᴀʏı ᴋᴀʀışᴛıʀ • ʟɪꜱᴛᴇ ꜱıʀᴀꜱıɴı ʀᴀꜱᴛɢᴇʟᴇ ʏᴀᴘ"),
    BotCommand("seek", "❖ İʟᴇʀɪ ꜱᴀʀ • ʙᴇʟɪʀʟɪ ʙɪʀ ꜱᴀɴɪʏᴇʏᴇ ɢɪᴛ"),
    BotCommand("seekback", "❖ ɢᴇʀɪ ꜱᴀʀ • öɴᴄᴇᴋɪ ʙɪʀ ꜱᴀɴɪʏᴇʏᴇ ᴅöɴ"),
    BotCommand("song", "❖ şᴀʀᴋı İɴᴅɪʀ • ᴍᴘ3 ᴠᴇʏᴀ ᴍᴘ4 ᴅᴏꜱʏᴀꜱı ᴀʟ"),
    BotCommand("speed", "❖ ʜıᴢı ᴀʏᴀʀʟᴀ • ɢʀᴜᴘ ᴏʏɴᴀᴛᴍᴀ ʜıᴢıɴı ᴅᴇğɪşᴛɪʀ"),
    BotCommand("cspeed", "❖ ᴋᴀɴᴀʟ ʜıᴢı • ᴋᴀɴᴀʟ ᴏʏɴᴀᴛᴍᴀ ʜıᴢıɴı ᴀʏᴀʀʟᴀ"),
    BotCommand("tagall", "❖ ʜᴇʀᴋᴇꜱɪ ᴇᴛɪᴋᴇᴛʟᴇ • ɢʀᴜᴘᴛᴀᴋɪ ʜᴇʀᴋᴇꜱᴇ ꜱᴇꜱʟᴇɴ"),
]

async def setup_bot_commands():
    try:
        await app.set_bot_commands(COMMANDS)
        LOGGER("ShrutiMusic").info("Bot commands set successfully!")
        
    except Exception as e:
        LOGGER("ShrutiMusic").error(f"Failed to set bot commands: {str(e)}")

async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        exit()

    await sudo()

    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass

    await app.start()
    
    await setup_bot_commands()

    for all_module in ALL_MODULES:
        importlib.import_module("ShrutiMusic.plugins" + all_module)

    LOGGER("ShrutiMusic.plugins").info("Successfully Imported Modules...")

    await userbot.start()
    await Nand.start()

    try:
        await Nand.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("ShrutiMusic").error(
            "Please turn on the videochat of your log group\channel.\n\nStopping Bot..."
        )
        exit()
    except:
        pass

    await Nand.decorators()

    LOGGER("ShrutiMusic").info(
        "\x53\x68\x72\x75\x74\x69\x20\x4d\x75\x73\x69\x63\x20\x53\x74\x61\x72\x74\x65\x64\x20\x53\x75\x63\x63\x65\x73\x73\x66\x75\x6c\x6c\x79\x2e\x0a\x0a\x44\x6f\x6e\x27\x74\x20\x66\x6f\x72\x67\x65\x74\x20\x74\x6f\x20\x76\x69\x73\x69\x74\x20\x40\x53\x68\x72\x75\x74\x69\x42\x6f\x74\x73"
    )

    await idle()

    await app.stop()
    await userbot.stop()
    LOGGER("ShrutiMusic").info("Stopping Shruti Music Bot...🥺")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())


# ©️ Copyright Reserved - @NoxxOP  Nand Yaduwanshi

# ===========================================
# ©️ 2025 Nand Yaduwanshi (aka @NoxxOP)
# 🔗 GitHub : https://github.com/NoxxOP/ShrutiMusic
# 📢 Telegram Channel : https://t.me/ShrutiBots
# ===========================================


# ❤️ Love From ShrutiBots
