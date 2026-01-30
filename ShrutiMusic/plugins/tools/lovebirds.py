import random
from pyrogram import filters
from ShrutiMusic import app
from ShrutiMusic.core.mongo import mongodb
from config import MONGO_DB_URI

lovebirds_db = mongodb.lovebirds
users_collection = lovebirds_db.users
gifts_collection = lovebirds_db.gifts

# Hediye Listesi - Türkçeleştirildi
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

async def get_user_data(user_id):
    try:
        user_data = await users_collection.find_one({"user_id": user_id})
        if not user_data:
            new_user = {
                "user_id": user_id,
                "coins": 50,
                "total_gifts_received": 0,
                "total_gifts_sent": 0,
                "created_at": "2026"
            }
            await users_collection.insert_one(new_user)
            return new_user
        return user_data
    except:
        return {"user_id": user_id, "coins": 0, "total_gifts_received": 0, "total_gifts_sent": 0}

async def update_user_coins(user_id, amount):
    try:
        await users_collection.update_one(
            {"user_id": user_id},
            {"$inc": {"coins": amount}},
            upsert=True
        )
    except:
        pass

async def get_user_gifts(user_id, gift_type="received"):
    try:
        if gift_type == "received":
            gifts = await gifts_collection.find({"receiver_id": user_id}).to_list(length=None)
        else:
            gifts = await gifts_collection.find({"sender_id": user_id}).to_list(length=None)
        return gifts
    except:
        return []

def get_user_info(message):
    try:
        if not message.from_user:
            return None, None
        user_id = message.from_user.id
        username = message.from_user.username or message.from_user.first_name
        return user_id, username
    except:
        return None, None

@app.on_message(filters.command(["balance", "bal", "cuzdan"], prefixes=["/", "!", "."]))
async def balance(_, message):
    try:
        uid, username = get_user_info(message)
        if not uid: return
        user_data = await get_user_data(uid)
        coins = user_data["coins"]
        gifts_received = await gifts_collection.count_documents({"receiver_id": uid})
        gifts_sent = await gifts_collection.count_documents({"sender_id": uid})
        
        balance_text = f"""
💰 <b>{username} | ʜᴇsᴀᴘ ʙɪʟɢɪʟᴇʀɪ</b>

💸 <b>ʙᴀᴋɪʏᴇ:</b> {coins} ᴄᴏɪɴs
🎁 <b>ᴀʟɪɴᴀɴ:</b> {gifts_received}
📤 <b>ɢᴏ̈ɴᴅᴇʀɪʟᴇɴ:</b> {gifts_sent}

•── ⋅ ⋅ ⋅ ───────── ⋅ • ⋅ ──•
💡 <b>ɪ̇ᴘᴜᴄᴜ:</b> ɢʀᴜᴘᴛᴀ ᴍᴇsᴀᴊ ʏᴀᴢᴀʀᴀᴋ ᴄᴏɪɴ ᴋᴀᴢᴀɴᴀʙɪʟɪʀsɪɴ!
"""
        await message.reply_text(balance_text)
    except:
        pass

@app.on_message(filters.command("gifts", prefixes=["/", "!", "."]))
async def gift_list(_, message):
    try:
        text = "🎁 <b>ᴍᴇᴠᴄᴜᴛ ʜᴇᴅɪʏᴇʟᴇʀ:</b>\n\n"
        sorted_gifts = sorted(GIFTS.items(), key=lambda x: x[1]["cost"])
        for emoji, gift_info in sorted_gifts:
            text += f"{emoji} <b>{gift_info['name']}</b> - {gift_info['cost']} ᴄᴏɪɴs\n"
        
        text += "\n📝 <b>ᴋᴜʟʟᴀɴɪᴍ:</b> `/sendgift @username ᴇᴍᴏᴊɪ`"
        text += "\n💡 <b>ᴏ̈ʀɴᴇᴋ:</b> `/sendgift @deniz 🌹`"
        await message.reply_text(text)
    except:
        pass

@app.on_message(filters.command("sendgift", prefixes=["/", "!", "."]))
async def send_gift(_, message):
    try:
        parts = message.text.split(" ")
        if len(parts) < 3:
            return await message.reply_text("❌ <b>ᴋᴜʟʟᴀɴɪᴍ:</b> `/sendgift @username ᴇᴍᴏᴊɪ`")
        
        target = parts[1].replace("@", "")
        gift_emoji = parts[2]
        sender_id, sender_name = get_user_info(message)
        if not sender_id: return
        
        sender_data = await get_user_data(sender_id)
        if gift_emoji not in GIFTS:
            return await message.reply_text("❌ <b>ɢᴇᴄ̧ᴇʀsɪᴢ ʜᴇᴅɪʏᴇ!</b> `/gifts` ʏᴀᴢᴀʀᴀᴋ ʟɪsᴛᴇʏᴇ ʙᴀᴋɪɴ.")
        
        gift_info = GIFTS[gift_emoji]
        cost = gift_info["cost"]
        
        if sender_data["coins"] < cost:
            return await message.reply_text(f"😢 <b>ʏᴇᴛᴇʀsɪᴢ ʙᴀᴋɪʏᴇ!</b>\n💰 ɢᴇʀᴇᴋʟɪ: {cost} ᴄᴏɪɴs\n📉 sɪᴢᴅᴇᴋɪ: {sender_data['coins']}")
        
        await users_collection.update_one({"user_id": sender_id}, {"$inc": {"coins": -cost, "total_gifts_sent": 1}})
        
        gift_record = {
            "sender_id": sender_id, "sender_name": sender_name, "receiver_name": target,
            "receiver_id": None, "gift_name": gift_info["name"], "gift_emoji": gift_emoji,
            "cost": cost, "timestamp": "2026", "claimed": False
        }
        await gifts_collection.insert_one(gift_record)
        
        success_msg = f"""
🎉 <b>ʜᴇᴅɪʏᴇ ʙᴀşᴀʀɪʏʟᴀ ɢᴏ̈ɴᴅᴇʀɪʟᴅɪ!</b>

{gift_emoji} <b>{sender_name}</b>, <b>@{target}</b> ᴋᴜʟʟᴀɴɪᴄɪsɪɴᴀ <b>{gift_info['name']}</b> ɢᴏ̈ɴᴅᴇʀᴅɪ!

💝 <b>ʜᴇᴅɪʏᴇ ᴅᴇᴛᴀʏʟᴀʀɪ:</b>
• <b>ʜᴇᴅɪʏᴇ:</b> {gift_emoji} {gift_info['name']}
• <b>ᴍᴀʟɪʏᴇᴛ:</b> {cost} ᴄᴏɪɴs
• <b>ᴋɪᴍᴅᴇɴ:</b> {sender_name}

💰 <b>ᴋᴀʟᴀɴ ʙᴀᴋɪʏᴇɴɪᴢ:</b> {sender_data['coins'] - cost}
"""
        await message.reply_text(success_msg)
    except:
        pass

async def claim_pending_gifts(user_id, username):
    try:
        pending_gifts = await gifts_collection.find({"receiver_name": username, "claimed": False}).to_list(length=None)
        if pending_gifts:
            total_bonus, gift_count = 0, len(pending_gifts)
            for gift in pending_gifts:
                await gifts_collection.update_one({"_id": gift["_id"]}, {"$set": {"receiver_id": user_id, "claimed": True}})
                total_bonus += 5
            await users_collection.update_one({"user_id": user_id}, {"$inc": {"coins": total_bonus, "total_gifts_received": gift_count}})
            return gift_count, total_bonus
        return 0, 0
    except:
        return 0, 0

@app.on_message(filters.
