import asyncio

from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
from pyrogram.errors import FloodWait

from ShrutiMusic import app
from ShrutiMusic.misc import SUDOERS  # MongoDB'den gelen set
from ShrutiMusic.utils.database import (
    get_active_chats,
    get_authuser_names,
    get_client,
    get_served_chats,
    get_served_users,
)
from ShrutiMusic.utils.decorators.language import language
from ShrutiMusic.utils.formatters import alpha_to_int
from config import adminlist

# Pyrogram 2.x uyumu için: set → list
SUDOERS_LIST = list(SUDOERS)

IS_BROADCASTING = False


@app.on_message((filters.command(["broadcast", "yayınla"])) & filters.user(SUDOERS_LIST))
@language
async def broadcast_message(client, message, _):
    global IS_BROADCASTING

    if "-wfchat" in message.text or "-wfuser" in message.text:
        if not message.reply_to_message or not (message.reply_to_message.photo or message.reply_to_message.text):
            return await message.reply_text("Lütfen yayınlamak istediğiniz metin veya fotoğrafa yanıt verin.")

        if message.reply_to_message.photo:
            content_type = 'photo'
            file_id = message.reply_to_message.photo.file_id
        else:
            content_type = 'text'
            text_content = message.reply_to_message.text
            
        caption = message.reply_to_message.caption
        reply_markup = getattr(message.reply_to_message, 'reply_markup', None)

        IS_BROADCASTING = True
        await message.reply_text("Yayın işlemi başlatıldı, lütfen bekleyin...")

        if "-wfchat" in message.text:
            sent_chats = 0
            chats = [int(chat["chat_id"]) for chat in await get_served_chats()]
            for i in chats:
                try:
                    if content_type == 'photo':
                        await app.send_photo(chat_id=i, photo=file_id, caption=caption, reply_markup=reply_markup)
                    else:
                        await app.send_message(chat_id=i, text=text_content, reply_markup=reply_markup)
                    sent_chats += 1
                    await asyncio.sleep(0.2)
                except FloodWait as fw:
                    await asyncio.sleep(fw.value)
                except:
                    continue
            await message.reply_text(f"Sohbetlere yayın tamamlandı! Toplam {sent_chats} sohbet.")

        if "-wfuser" in message.text:
            sent_users = 0
            users = [int(user["user_id"]) for user in await get_served_users()]
            for i in users:
                try:
                    if content_type == 'photo':
                        await app.send_photo(chat_id=i, photo=file_id, caption=caption, reply_markup=reply_markup)
                    else:
                        await app.send_message(chat_id=i, text=text_content, reply_markup=reply_markup)
                    sent_users += 1
                    await asyncio.sleep(0.2)
                except FloodWait as fw:
                    await asyncio.sleep(fw.value)
                except:
                    continue
            await message.reply_text(f"Kullanıcılara yayın tamamlandı! Toplam {sent_users} kullanıcı.")

        IS_BROADCASTING = False
        return

    if message.reply_to_message:
        x = message.reply_to_message.id
        y = message.chat.id
        reply_markup = getattr(message.reply_to_message, 'reply_markup', None)
    else:
        if len(message.command) < 2:
            return await message.reply_text("Lütfen yayınlamak istediğiniz mesajı yazın.")
        query = message.text.split(None, 1)[1]
        for flag in ["-pin", "-nobot", "-pinloud", "-assistant", "-user"]:
            query = query.replace(flag, "")
        if query.strip() == "":
            return await message.reply_text("Boş mesaj ile yayın yapamazsınız.")

    IS_BROADCASTING = True
    await message.reply_text("Yayın işlemi başlatıldı, lütfen bekleyin...")

    if "-nobot" not in message.text:
        sent = 0
        pin = 0
        chats = [int(chat["chat_id"]) for chat in await get_served_chats()]
        for i in chats:
            try:
                m = (
                    await app.copy_message(chat_id=i, from_chat_id=y, message_id=x, reply_markup=reply_markup)
                    if message.reply_to_message
                    else await app.send_message(i, text=query)
                )
                if "-pin" in message.text:
                    try:
                        await m.pin(disable_notification=True)
                        pin += 1
                    except:
                        pass
                elif "-pinloud" in message.text:
                    try:
                        await m.pin(disable_notification=False)
                        pin += 1
                    except:
                        pass
                sent += 1
                await asyncio.sleep(0.2)
            except FloodWait as fw:
                if fw.value > 200:
                    continue
                await asyncio.sleep(fw.value)
            except:
                continue
        try:
            await message.reply_text(f"Yayın tamamlandı! Toplam gönderilen sohbet: {sent}, sabitlenen mesaj: {pin}")
        except:
            pass

    if "-user" in message.text:
        susr = 0
        served_users = [int(user["user_id"]) for user in await get_served_users()]
        for i in served_users:
            try:
                m = (
                    await app.copy_message(chat_id=i, from_chat_id=y, message_id=x, reply_markup=reply_markup)
                    if message.reply_to_message
                    else await app.send_message(i, text=query)
                )
                susr += 1
                await asyncio.sleep(0.2)
            except FloodWait as fw:
                if fw.value > 200:
                    continue
                await asyncio.sleep(fw.value)
            except:
                pass
        try:
            await message.reply_text(f"Kullanıcılara yayın tamamlandı! Toplam gönderilen kullanıcı: {susr}")
        except:
            pass

    if "-assistant" in message.text:
        aw = await message.reply_text("Asistanlar üzerinden yayın yapılıyor, lütfen bekleyin...")
        text = "Asistanlar üzerinden gönderilen mesajlar:\n"
        from ShrutiMusic.core.userbot import assistants

        for num in assistants:
            sent = 0
            client = await get_client(num)
            async for dialog in client.get_dialogs():
                try:
                    if message.reply_to_message:
                        await client.forward_messages(dialog.chat.id, y, x)
                    else:
                        await client.send_message(dialog.chat.id, text=query)
                    sent += 1
                    await asyncio.sleep(3)
                except FloodWait as fw:
                    if fw.value > 200:
                        continue
                    await asyncio.sleep(fw.value)
                except:
                    continue
            text += f"Asistan {num} - Gönderilen mesaj sayısı: {sent}\n"
        try:
            await aw.edit_text(text)
        except:
            pass

    IS_BROADCASTING = False


async def auto_clean():
    while not await asyncio.sleep(10):
        try:
            served_chats = await get_active_chats()
            for chat_id in served_chats:
                if chat_id not in adminlist:
                    adminlist[chat_id] = []
                    async for user in app.get_chat_members(
                        chat_id, filter=ChatMembersFilter.ADMINISTRATORS
                    ):
                        if user.privileges.can_manage_video_chats:
                            adminlist[chat_id].append(user.user.id)
                    authusers = await get_authuser_names(chat_id)
                    for user in authusers:
                        user_id = await alpha_to_int(user)
                        adminlist[chat_id].append(user_id)
        except:
            continue


asyncio.create_task(auto_clean())
