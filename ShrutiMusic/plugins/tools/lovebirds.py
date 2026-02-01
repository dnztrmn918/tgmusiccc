import random
import asyncio
from pyrogram import filters
from pyrogram.types import Message
from ShrutiMusic import app
from ShrutiMusic.core.mongo import mongodb
from config import MONGO_DB_URI

# --- VERİTABANI BAĞLANTILARI ---
lovebirds_db = mongodb.lovebirds
users_collection = lovebirds_db.users
gifts_collection = lovebirds_db.gifts

# --- HEDİYE TANIMLAMALARI ---
GIFTS = {
    "🌹": {"name": "Gül", "cost": 10, "emoji": "🌹"},
    "🍫": {"name": "Çikolata", "cost": 20, "emoji": "🍫"},
    "🧸": {"name": "Ayıcık", "cost": 30, "emoji": "🧸"},
    "💍": {"name": "Yüzük", "cost": 50, "emoji": "💍"},
    "❤️": {"name": "Kalp", "cost": 5, "emoji": "❤️"},
    "🌺": {"name": "Çiçek Buketi", "cost": 25, "emoji": "🌺"},
    "💎": {"name": "Elmas", "cost": 100, "emoji": "💎"},
    "🎀": {"name": "Hediye Kutusu", "cost": 40, "emoji": "🎀"},
    "🌙": {"name": "Ay", "cost": 35, "emoji": "🌙"},
    "⭐": {"name": "Yıldız", "cost": 15, "emoji": "⭐"},
    "🦋": {"name": "Kelebek", "cost": 18, "emoji": "🦋"},
    "🕊️": {"name": "Güvercin", "cost": 22, "emoji": "🕊️"},
    "🏰": {"name": "Şato", "cost": 80, "emoji": "🏰"},
    "🎂": {"name": "Pasta", "cost": 28, "emoji": "🎂"},
    "🍓": {"name": "Çilek", "cost": 12, "emoji": "🍓"}
}

# --- FONKSİYONLAR ---

async def get_user_data(user_id):
    """Kullanıcı verilerini getirir veya yeni kayıt oluşturur."""
    try:
        user_data = await users_collection.find_one({"user_id": user_id})
        if not user_data:
            new_user = {
                "user_id": user_id,
                "coins": 50,
                "total_gifts_received": 0,
                "total_gifts_sent": 0,
                "last_chat_name": "Bilinmiyor",
                "created_at": "2026"
            }
            await users_collection.insert_one(new_user)
            return new_user
        return user_data
    except Exception as e:
        print(f"Hata: get_user_data - {e}")
        return {"user_id": user_id, "coins": 0}

async def update_user_coins(user_id, amount, chat_name=None):
    """Kullanıcı bakiyesini ve bulunduğu son grubu günceller."""
    try:
        update_query = {"$inc": {"coins": amount}}
        if chat_name:
            update_query["$set"] = {"last_chat_name": chat_name}
        await users_collection.update_one({"user_id": user_id}, update_query, upsert=True)
    except Exception as e:
        print(f"Hata: update_user_coins - {e}")

def get_user_info(message):
    """Mesajdan kullanıcı ID ve isim bilgisini ayıklar."""
    try:
        if not message.from_user:
            return None, None
        return message.from_user.id, message.from_user.first_name
    except:
        return None, None

# --- KOMUTLAR ---

@app.on_message(filters.command(["cuzdan", "bal", "balance"], prefixes=["/", "!", "."]))
async def balance(_, message: Message):
    uid, username = get_user_info(message)
    if not uid: return
    user_data = await get_user_data(uid)
    received = await gifts_collection.count_documents({"receiver_id": uid})
    sent = await gifts_collection.count_documents({"sender_id": uid})
    
    text = (f"💰 <b>{username} Profili</b>\n\n"
            f"💸 <b>Bakiye:</b> <code>{user_data['coins']}</code> coin\n"
            f"🎁 <b>Alınan:</b> {received}\n"
            f"📤 <b>Gönderilen:</b> {sent}\n\n"
            f"💡 <i>Grupta aktif olarak coin kazanabilirsin!</i>")
    await message.reply_text(text)

@app.on_message(filters.command(["hediyeler", "gifts"], prefixes=["/", "!", "."]))
async def gift_list(_, message: Message):
    text = "🎁 <b>Hediye Mağazası</b>\n\n"
    for emoj, info in sorted(GIFTS.items(), key=lambda x: x[1]["cost"]):
        text += f"{emoj} {info['name']} — <b>{info['cost']}</b> coin\n"
    text += "\n📝 <i>Örnek: /hediyegonder @kullanici 🌹</i>"
    await message.reply_text(text)

@app.on_message(filters.command(["hediyegonder", "sendgift"], prefixes=["/", "!", "."]))
async def send_gift(_, message: Message):
    parts = message.text.split()
    if len(parts) < 3:
        return await message.reply_text("❌ <b>Hatalı kullanım!</b>\nFormat: <code>/hediyegonder @etiket Emoji</code>")
    
    target = parts[1].replace("@", "")
    gift_emoji = parts[2]
    sid, sname = get_user_info(message)
    
    if gift_emoji not in GIFTS:
        return await message.reply_text("❌ Bu hediye mağazada yok!")
    
    cost = GIFTS[gift_emoji]["cost"]
    sdata = await get_user_data(sid)
    
    if sdata["coins"] < cost:
        return await message.reply_text(f"😢 Bakiyen yetersiz! {cost} coin gerekli.")
    
    await update_user_coins(sid, -cost)
    await gifts_collection.insert_one({
        "sender_id": sid, "sender_name": sname, 
        "receiver_name": target, "gift_emoji": gift_emoji, "claimed": False
    })
    await message.reply_text(f"🎉 <b>{sname}</b>, <b>@{target}</b> kullanıcısına {gift_emoji} gönderdi!")

@app.on_message(filters.command(["hikaye", "story"], prefixes=["/", "!", "."]))
async def love_story(_, message: Message):
    parts = message.text.split(None, 2)
    if len(parts) < 3: return
    n1, n2 = parts[1], parts[2]
    
    # --- GENİŞ HİKAYE HAVUZU ---
    sts = [
        f"Bir zamanlar <b>{n1}</b> ve <b>{n2}</b> ☕ bir kahve dükkanında tanıştılar. Gözleri buluştuğunda zaman durdu...",
        f"<b>{n1}</b> kütüphanede 📚 kitap ararken <b>{n2}</b> ona yardım etti. O an yeni bir sayfa açıldı.",
        f"Yağmurlu bir günde 🌧️ <b>{n1}</b> şemsiyesini <b>{n2}</b> ile paylaştı. Kalpleri ısınmaya başladı.",
        f"<b>{n1}</b> ve <b>{n2}</b> bir konserde 🎵 aynı nakarata eşlik ettiler. Ruhları bir oldu.",
        f"Yıldızların altında ✨ <b>{n1}</b> bir dilek tuttu, o sırada <b>{n2}</b> yanına geldi. Dileği gerçek olmuştu.",
        f"Deniz kenarında 🌊 <b>{n1}</b> bir şişe buldu, içinde <b>{n2}</b>'den gelen asırlık bir aşk mektubu vardı.",
        f"<b>{n1}</b> ve <b>{n2}</b> karlı bir günde ❄️ kartopu oynarken birbirlerinin gülüşüne aşık oldular.",
        f"Eski bir trende 🚂 <b>{n1}</b> ve <b>{n2}</b> yan yana oturdular. Yolculuk hiç bitmesin istediler.",
        f"<b>{n1}</b> çiçekçide 🌸 <b>{n2}</b> için en güzel gülü seçerken aslında kalbini veriyordu.",
        f"Karanlık bir sokakta 🕯️ <b>{n1}</b>'in yolunu <b>{n2}</b> aydınlattı. Artık beraber yürüyorlar."
    ]
    await message.reply_text(f"💕 <b>Aşk Masalı</b>\n\n{random.choice(sts)}\n\n✨ <i>Aşk tesadüfleri sever...</i>")
    uid, _ = get_user_info(message)
    if uid: await update_user_coins(uid, 5, message.chat.title)

@app.on_message(filters.command(["zenginler", "top"], prefixes=["/", "!", "."]))
async def leaderboard(_, message: Message):
    try:
        top_list = await users_collection.find().sort("coins", -1).limit(10).to_list(10)
        if not top_list: return
        
        res = "🏆 <b>En Zengin 10 Kullanıcı</b>\n\n"
        medals = ["🥇", "🥈", "🥉", "🏅", "🏅", "🏅", "🏅", "🏅", "🏅", "🏅"]
        
        for i, u in enumerate(top_list):
            uid = u['user_id']
            grp = u.get("last_chat_name", "Bilinmiyor")
            try:
                user_obj = await app.get_users(uid)
                uname = user_obj.first_name if user_obj.first_name else "Gizli"
            except:
                uname = f"Kullanıcı {uid}"
            
            res += f"{medals[i]} <a href='tg://user?id={uid}'>{uname}</a> — <i>{grp}</i> — <b>{u['coins']}</b> coin\n"
        
        await message.reply_text(res, disable_web_page_preview=True)
    except Exception as e:
        print(f"Leaderboard hatası: {e}")

@app.on_message(filters.text & ~filters.regex(r"^[/!.\-]"))
async def message_handler(_, message: Message):
    uid, uname = get_user_info(message)
    if not uid: return
    # Bekleyen hediyeleri kontrol et
    pending = await gifts_collection.find({"receiver_name": uname, "claimed": False}).to_list(None)
    if pending:
        for g in pending:
            await gifts_collection.update_one({"_id": g["_id"]}, {"$set": {"receiver_id": uid, "claimed": True}})
            await update_user_coins(uid, 5) # Hediye başı bonus
        await message.reply_text(f"🎁 <b>{uname}</b>, bekleyen hediyelerin teslim edildi! +Bonus coin.")
    
    # Rastgele coin şansı
    if random.randint(1, 100) <= 20:
        await update_user_coins(uid, 1, message.chat.title)

# --- DOSYA SONU ---
