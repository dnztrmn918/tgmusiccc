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

from pyrogram import enums, filters
from pyrogram.errors import FloodWait

from ShrutiMusic import app


@app.on_message(filters.command("bots") & filters.group)
async def bots(client, message):

    try:
        botList = []
        async for bot in app.get_chat_members(
            message.chat.id, filter=enums.ChatMembersFilter.BOTS
        ):
            botList.append(bot.user)
        lenBotList = len(botList)
        text3 = f"**ʙᴏᴛ ʟɪsᴛᴇsɪ - {message.chat.title}**\n\n🤖 ʙᴏᴛʟᴀʀ\n"
        while len(botList) > 1:
            bot = botList.pop(0)
            text3 += f"├ @{bot.username}\n"
        else:
            bot = botList.pop(0)
            text3 += f"└ @{bot.username}\n\n"
            text3 += f"**ᴛᴏᴘʟᴀᴍ ʙᴏᴛ ꜱᴀʏıꜱı**: {lenBotList}**"
            await app.send_message(message.chat.id, text3)
    except FloodWait as e:
        await asyncio.sleep(e.value)


__MODULE__ = "Bᴏᴛs"
__HELP__ = """
**ʙᴏᴛs**

• /bots - ❖ ʙᴏᴛ ʟɪsᴛᴇsɪ • ɢʀᴜᴘᴛᴀᴋɪ ʙᴏᴛʟᴀʀɪ ʟɪsᴛᴇʟᴇʀ
"""


# ©️ Copyright Reserved - @NoxxOP  Nand Yaduwanshi

# ===========================================
# ©️ 2025 Nand Yaduwanshi (aka @NoxxOP)
# 🔗 GitHub : https://github.com/NoxxOP/ShrutiMusic
# 📢 Telegram Channel : https://t.me/ShrutiBots
# ===========================================


# ❤️ Love From ShrutiBots 
