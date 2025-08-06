import os
from unidecode import unidecode
from PIL import ImageDraw, Image, ImageFont, ImageChops
from pyrogram import *
from pyrogram.types import *
from logging import getLogger
from ShrutiMusic import LOGGER
from pyrogram.types import Message
from ShrutiMusic.misc import SUDOERS
from ShrutiMusic import app
from ShrutiMusic.utils.database import *
from ShrutiMusic.utils.database import db

# Veritabanı bağlantısı
try:
    wlcm = db.welcome
except:
    from ShrutiMusic.utils.database import welcome as wlcm

LOGGER = getLogger(__name__)

class temp:
    ME = None
    CURRENT = 2
    CANCEL = False
    MELCOW = {}
    U_NAME = None
    B_NAME = None

# Profil fotoğrafını daire şeklinde kırpma
def circle(pfp, size=(450, 450)):
    pfp = pfp.resize(size, Image.LANCZOS).convert("RGBA")
    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new("L", bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.LANCZOS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp

# Karşılama görselini oluşturma
def welcomepic(pic, user, chat, id, uname):
    background = Image.open("ShrutiMusic/assets/welcome.png")
    pfp = Image.open(pic).convert("RGBA")
    pfp = circle(pfp)
    pfp = pfp.resize((450, 450)) 
    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype('ShrutiMusic/assets/font.ttf', size=45)
    font2 = ImageFont.truetype('ShrutiMusic/assets/font.ttf', size=90)
    draw.text((65, 250), f'İSİM : {unidecode(user)}', fill="white", font=font)
    draw.text((65, 340), f'ID : {id}', fill="white", font=font)
    draw.text((65, 430), f"KULLANICI ADI : {uname}", fill="white", font=font)
    pfp_position = (767, 133)  
    background.paste(pfp, pfp_position, pfp)  
    background.save(f"downloads/welcome#{id}.png")
    return f"downloads/welcome#{id}.png"

# ✅ /welcome komutu (aç/kapat)
@app.on_message(filters.command("welcome") & ~filters.private)
async def auto_state(_, message):
    usage = "**❖ Kullanım:** /welcome [on|off]"
    if len(message.command) == 1:
        return await message.reply_text(usage)

    chat_id = message.chat.id
    user = await app.get_chat_member(message.chat.id, message.from_user.id)

    if user.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
        A = await wlcm.find_one({"chat_id": chat_id})
        state = message.text.split(None, 1)[1].strip().lower()

        if state == "on":
            if A and not A.get("disabled", False):
                return await message.reply_text("🔹 Karşılama mesajı zaten açık.")
            await wlcm.update_one({"chat_id": chat_id}, {"$set": {"disabled": False}}, upsert=True)
            await message.reply_text(f"✅ {message.chat.title} grubunda özel karşılama açıldı.")

        elif state == "off":
            if A and A.get("disabled", False):
                return await message.reply_text("🔸 Karşılama mesajı zaten kapalı.")
            await wlcm.update_one({"chat_id": chat_id}, {"$set": {"disabled": True}}, upsert=True)
            await message.reply_text(f"🛑 {message.chat.title} grubunda özel karşılama kapatıldı.")

        else:
            await message.reply_text(usage)
    else:
        await message.reply("❗ Bu komutu sadece yöneticiler kullanabilir.")

# ✅ Yeni kullanıcı geldiğinde karşılama mesajı gönder
@app.on_chat_member_updated(filters.group, group=-3)
async def greet_group(_, member: ChatMemberUpdated):
    chat_id = member.chat.id
    A = await wlcm.find_one({"chat_id": chat_id})

    if not A or not A.get("disabled", True):  # Başlangıçta 'disabled: True' yani KAPALI olarak ayarlı
        if (
            not member.new_chat_member
            or member.new_chat_member.status in {"banned", "left", "restricted"}
            or member.old_chat_member
        ):
            return

        user = member.new_chat_member.user if member.new_chat_member else member.from_user
        try:
            pic = await app.download_media(
                user.photo.big_file_id, file_name=f"pp{user.id}.png"
            )
        except AttributeError:
            pic = "ShrutiMusic/assets/upic.png"

        if (temp.MELCOW).get(f"welcome-{member.chat.id}") is not None:
            try:
                await temp.MELCOW[f"welcome-{member.chat.id}"].delete()
            except Exception as e:
                LOGGER.error(e)

        try:
            welcomeimg = welcomepic(
                pic, user.first_name, member.chat.title, user.id, user.username
            )
            temp.MELCOW[f"welcome-{member.chat.id}"] = await app.send_photo(
                member.chat.id,
                photo=welcomeimg,
                caption=f"""
🌸✨ ──────────────── ✨🌸

🎉 <b>GRUBA HOŞGELDİN</b> 🎉

👤 <b>İsim:</b> {user.mention}
🔗 <b>Kullanıcı Adı:</b> @{user.username if user.username else "Yok"}
🆔 <b>Kullanıcı ID:</b> <code>{user.id}</code>
🏠 <b>Grup:</b> {member.chat.title}

🎶 <b>Umarız burada keyifli vakit geçirirsin!</b>
🎧 <b>Müzik keyfini çıkar!</b>

<blockquote><b>💖 Destekleyen:</b> <a href="https://t.me/{app.username}?start=help">Müzik Botları</a></blockquote>

🌸✨ ──────────────── ✨🌸
""",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🎵 Müzik/Şiir Kanalımız", url="https://t.me/TubidyMusic")]
                ]),
            )

        except Exception as e:
            LOGGER.error(e)

        try:
            os.remove(f"downloads/welcome#{user.id}.png")
            os.remove(f"downloads/pp{user.id}.png")
        except Exception:
            pass

# ©️ 2025 Nand Yaduwanshi (aka @NoxxOP)
# 🔗 GitHub : https://github.com/NoxxOP/ShrutiMusic
# 📢 Telegram Kanalı : https://t.me/ShrutiBots
