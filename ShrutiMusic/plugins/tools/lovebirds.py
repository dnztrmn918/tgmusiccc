import random
import asyncio
from pyrogram import filters
from ShrutiMusic import app
from ShrutiMusic.core.mongo import mongodb

lovebirds_db = mongodb.lovebirds
users_collection = lovebirds_db.users
gifts_collection = lovebirds_db.gifts

# Hediye Listesi
GIFTS = {
    "🌹": {"name": "Gül", "cost": 10, "emoji": "🌹"},
    "🍫": {"name": "Çikolata", "cost": 20, "emoji": "🍫"},
    "🧸": {"name": "Ayıcık", "cost": 30, "emoji": "🧸"},
    "💍": {"name": "Yüzük", "cost": 50, "emoji": "💍"},
    "❤️": {"name": "Kalp", "cost": 5, "emoji": "❤️"},
    "💎": {"name": "Elmas", "cost": 100, "emoji": "💎"},
    "🏰": {"name": "Şato", "cost": 150, "emoji": "🏰"},
    "🍓": {"name": "Çilek", "cost": 12, "emoji": "🍓"}
}

async def get_user_data(user_id):
    user_data = await users_collection.find_one({"user_id": user_id})
    if not user_data:
        new_user = {
            "user_id": user_id,
            "coins": 50,
            "total_gifts_received": 0,
            "total_gifts_sent": 0,
        }
        await users_collection.insert_one(new_user)
        return new_user
    return user_data

@app.on_message(filters.command(["balance", "bal", "cuzdan"], prefixes=["/", "!", "."]))
async def balance(_, message):
    if not message.from_user:
        return
    uid = message.from_user.id
    username = message.from_user.first_name
    user_data = await get_user_data(uid)
    gifts_received = await gifts_collection.count_documents({"receiver_id": uid})
    
    balance_text = f"""
💰 <b>{username} | ʜᴇsᴀᴘ ʙɪʟɢɪʟᴇʀɪ</b>

💸 <b>ʙᴀᴋɪʏᴇ:</b> {user_data['coins']} ᴄᴏɪɴs
🎁 <b>ᴀʟɪɴᴀɴ:</b> {gifts_received}
📤 <b>ɢᴏ̈ɴᴅᴇʀɪʟᴇɴ:</b> {user_data.get('total_gifts_sent', 0)}

•── ⋅ ⋅ ⋅ ───────── ⋅ • ⋅ ──•
💡 <b>ɪ̇ᴘᴜᴄᴜ:</b> ɢʀᴜᴘᴛᴀ ᴍᴇsᴀᴊ ʏᴀᴢᴀʀᴀᴋ ᴄᴏɪɴ ᴋᴀᴢᴀɴᴀʙɪʟɪʀsɪɴ!
"""
    await message.reply_text(balance_text)

@app.on_message(filters.command("gifts", prefixes=["/", "!", "."]))
async def gift_list(_, message):
    text = "🎁 <b>ᴍᴇᴠᴄᴜᴛ ʜᴇᴅɪʏᴇʟᴇʀ:</b>\n\n"
    for emoji, info in GIFTS.items():
        text += f"{emoji} <b>{info['name']}</b> - {info['cost']} ᴄᴏɪɴs\n"
    text += "\n📝 <b>ᴋᴜʟʟᴀɴɪᴍ:</b> `/sendgift @username 🌹`"
    await message.reply_text(text)

@app.on_message(filters.command("sendgift", prefixes=["/", "!", "."]))
async def send_gift(_, message):
    parts = message.text.split(" ")
    if len(parts) < 3:
        return await message.reply_text("❌ <b>ᴋᴜʟʟᴀɴɪᴍ:</b> `/sendgift @username ᴇᴍᴏᴊɪ`")
    
    target_username = parts[1].replace("@", "")
    gift_emoji = parts[2]
    sender_id = message.from_user.id
    
    if gift_emoji not in GIFTS:
        return await message.reply_text("❌ <b>ɢᴇᴄ̧ᴇʀsɪᴢ ʜᴇᴅɪʏᴇ!</b>")
    
    gift_info = GIFTS[gift_emoji]
    sender_data = await get_user_data(sender_id)
    
    if sender_data["coins"] < gift_info["cost"]:
        return await message.reply_text(f"😢 <b>ʙᴀᴋɪʏᴇ ʏᴇᴛᴇʀsɪᴢ!</b>\nᴍᴀʟɪʏᴇᴛ: {gift_info['cost']} ᴄᴏɪɴs")

    await users_collection.update_one({"user_id": sender_id}, {"$inc": {"coins": -gift_info['cost'], "total_gifts_sent": 1}})
    await gifts_collection.insert_one({
        "sender_id": sender_id,
        "receiver_username": target_username,
        "gift_emoji": gift_emoji,
        "claimed": False
    })
    await message.reply_text(f"🎉 <b>{message.from_user.first_name}</b>, @{target_username} ᴋᴜʟʟᴀɴɪᴄɪsɪɴᴀ {gift_emoji} <b>{gift_info['name']}</b> ɢᴏ̈ɴᴅᴇʀᴅɪ!")

@app.on_message(filters.group & ~filters.bot, group=10)
async def earn_coins(_, message):
    if not message.from_user:
        return
    if random.random() < 0.20:
        reward = random.randint(1, 3)
        await users_collection.update_one(
            {"user_id": message.from_user.id},
            {"$inc": {"coins": reward}},
            upsert=True
        )
        
