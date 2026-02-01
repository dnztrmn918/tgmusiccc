import random
from pyrogram import filters
from ShrutiMusic import app
from ShrutiMusic.core.mongo import mongodb
from config import MONGO_DB_URI

lovebirds_db = mongodb.lovebirds
users_collection = lovebirds_db.users
gifts_collection = lovebirds_db.gifts

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

@app.on_message(filters.command(["cuzdan", "bal", "balance"], prefixes=["/", "!", "."]))
async def balance(_, message):
    try:
        uid, username = get_user_info(message)
        if not uid:
            return
        
        user_data = await get_user_data(uid)
        
        coins = user_data["coins"]
        gifts_received = await gifts_collection.count_documents({"receiver_id": uid})
        gifts_sent = await gifts_collection.count_documents({"sender_id": uid})
        
        balance_text = f"""
💰 <b>{username} Hesabı</b>
💸 <b>Bakiye:</b> {coins} coin
🎁 <b>Alınan Hediyeler:</b> {gifts_received}
📤 <b>Gönderilen Hediyeler:</b> {gifts_sent}

💡 <b>İpucu:</b> Coin kazanmak için grupta mesaj gönderin!
        """
        await message.reply_text(balance_text)
    except:
        pass

@app.on_message(filters.command(["hediyeler", "gifts"], prefixes=["/", "!", "."]))
async def gift_list(_, message):
    try:
        text = "🎁 <b>Mevcut Hediyeler:</b>\n\n"
        sorted_gifts = sorted(GIFTS.items(), key=lambda x: x[1]["cost"])
        
        for emoji, gift_info in sorted_gifts:
            text += f"{emoji} <b>{gift_info['name']}</b> - {gift_info['cost']} coin\n"
        
        text += "\n📝 <b>Kullanım:</b> /hediyegonder @kullaniciadi Emoji"
        text += "\n💡 <b>Örnek:</b> /hediyegonder @dnztrmnn 🌹"
        
        await message.reply_text(text)
    except:
        pass

@app.on_message(filters.command(["hediyegonder", "sendgift"], prefixes=["/", "!", "."]))
async def send_gift(_, message):
    try:
        parts = message.text.split(" ")
        if len(parts) < 3:
            return await message.reply_text("❌ <b>Kullanım:</b> /hediyegonder @kullaniciadi Emoji\n💡 <b>Örnek:</b> /hediyegonder @dnztrmnn 🌹")
        
        target = parts[1].replace("@", "")
        gift_emoji = parts[2]
        
        sender_id, sender_name = get_user_info(message)
        if not sender_id:
            return
        
        sender_data = await get_user_data(sender_id)
        
        if gift_emoji not in GIFTS:
            return await message.reply_text("❌ <b>Geçersiz hediye!</b> Mevcut hediyeleri görmek için /hediyeler yazın.")
        
        gift_info = GIFTS[gift_emoji]
        cost = gift_info["cost"]
        
        if sender_data["coins"] < cost:
            return await message.reply_text(f"😢 <b>Yetersiz bakiye!</b>\n💰 {cost} coine ihtiyacınız var ama sizde {sender_data['coins']} coin var.")
        
        await users_collection.update_one(
            {"user_id": sender_id},
            {"$inc": {"coins": -cost, "total_gifts_sent": 1}}
        )
        
        gift_record = {
            "sender_id": sender_id,
            "sender_name": sender_name,
            "receiver_name": target,
            "receiver_id": None,
            "gift_name": gift_info["name"],
            "gift_emoji": gift_emoji,
            "cost": cost,
            "timestamp": "2026",
            "claimed": False
        }
        
        await gifts_collection.insert_one(gift_record)
        updated_sender = await get_user_data(sender_id)
        
        success_msg = f"""
🎉 <b>Hediye Başarıyla Gönderildi!</b>

{gift_emoji} <b>{sender_name}</b>, <b>@{target}</b> kullanıcısına <b>{gift_info['name']}</b> gönderdi!

💝 <b>Hediye Detayları:</b>
• <b>Hediye:</b> {gift_emoji} {gift_info['name']}
• <b>Ücret:</b> {cost} coin
• <b>Gönderen:</b> {sender_name}
• <b>Alıcı:</b> @{target}

💰 <b>{sender_name} kalan bakiyesi:</b> {updated_sender['coins']}

💕 <i>Aşk her yerde!</i>
        """
        
        await message.reply_text(success_msg)
    except:
        pass

async def claim_pending_gifts(user_id, username):
    try:
        pending_gifts = await gifts_collection.find({
            "receiver_name": username,
            "claimed": False
        }).to_list(length=None)
        
        if pending_gifts:
            total_bonus = 0
            gift_count = len(pending_gifts)
            
            for gift in pending_gifts:
                await gifts_collection.update_one(
                    {"_id": gift["_id"]},
                    {
                        "$set": {
                            "receiver_id": user_id,
                            "claimed": True
                        }
                    }
                )
                total_bonus += 5
            
            await users_collection.update_one(
                {"user_id": user_id},
                {"$inc": {"coins": total_bonus, "total_gifts_received": gift_count}}
            )
            
            return gift_count, total_bonus
        
        return 0, 0
    except:
        return 0, 0

@app.on_message(filters.command(["hikaye", "story"], prefixes=["/", "!", "."]))
async def love_story(_, message):
    try:
        parts = message.text.split(" ", 2)
        if len(parts) < 3:
            return await message.reply_text("❌ <b>Kullanım:</b> /hikaye İsim1 İsim2\n💡 <b>Örnek:</b> /hikaye Deniz Merve")
        
        name1, name2 = parts[1], parts[2]
        
        stories = [
            f"Bir zamanlar <b>{name1}</b>, bir kahve dükkanında <b>{name2}</b> ile tanıştı ☕. Gözleri buharlı fincanların üzerinde buluştu ve kader aşk hikayelerini yazmaya başladı ❤️✨",
            f"Kalabalık bir kütüphanede 📚, <b>{name1}</b> ve <b>{name2}</b> aynı kitaba uzandılar. Parmakları birbirine değdi ve sihir gibi kıvılcımlar uçuştu 💫💕",
            f"<b>{name1}</b> yağmurda yürürken 🌧️, <b>{name2}</b> bir şemsiye uzattı ☂️. O ortak sığınak altında, aşk yağmur sonrası çiçekler gibi açtı 🌸",
            f"Bir konserde 🎵, <b>{name1}</b> ve <b>{name2}</b> kendilerini aynı şarkıyı söylerken buldular. Sesleri ve kalpleri tam bir uyum içindeydi 🎶❤️",
            f"<b>{name1}</b> yabancı bir şehirde kaybolmuşken 🏙️, <b>{name2}</b> yol gösterdi. Birlikte yürüdüler ve sadece yolu değil, birbirlerini de buldular 💝",
            f"Güzel bir bahçede 🌺, <b>{name1}</b> güllere hayran kalmışken <b>{name2}</b> bir rüya gibi belirdi. Birlikte bahçeyi daha da güzelleştirdiler 🌹✨",
            f"<b>{name1}</b> kitaplarını düşürdü 📖, <b>{name2}</b> toplamasına yardım etti. O basit anda, aynı aşk hikayesini okuduklarını fark ettiler 💘",
            f"Gün batımında kumsalda 🌅, <b>{name1}</b> ve <b>{name2}</b> kumdan kaleler yaptılar 🏰. Kalpleri ise çok daha güçlü bir şey inşa etti: sonsuz aşk 💞",
            f"<b>{name1}</b> parkta kuşları beslerken 🐦, <b>{name2}</b> daha fazla ekmek kırıntısıyla ona katıldı. Birlikte neşe ve kahkaha dolu bir senfoni yarattılar 🎭💕",
            f"Bir elektrik kesintisi sırasında 🕯️, <b>{name1}</b> ve <b>{name2}</b> mum ışığında hikayeler paylaştılar. O karanlıkta, en parlak ışıklarını buldular - birbirlerini ✨❤️"
        ]
        
        story = random.choice(stories)
        
        endings = [
            "\n\n💕 <i>Ve sonsuza dek mutlu yaşadılar...</i>",
            "\n\n❤️ <i>Gerçek aşk her zaman bir yolunu bulur...</i>",
            "\n\n💞 <i>Bazı insanlar tüm hayatlarını birbirlerinde buldukları şeyi arayarak geçirir...</i>",
            "\n\n✨ <i>Kaos dolu bir dünyada, birbirlerinde huzuru buldular...</i>",
            "\n\n💝 <i>Aşk mükemmel kişiyi bulmak değil, senin için mükemmel olanı bulmaktır...</i>"
        ]
        
        story += random.choice(endings)
        
        romantic_header = random.choice([
            "💕 <b>Aşk Hikayesi</b> 💕",
            "❤️ <b>Bir Aşk Masalı</b> ❤️", 
            "💞 <b>Romantik Hikaye</b> 💞",
            "✨ <b>Aşk Günlükleri</b> ✨",
            "🌹 <b>Romantik Masal</b> 🌹"
        ])
        
        final_story = f"{romantic_header}\n\n{story}"
        await message.reply_text(final_story)
        
        uid, _ = get_user_info(message)
        if uid:
            await update_user_coins(uid, 5)
    except:
        pass

@app.on_message(filters.command(["hediyelerim", "mygifts", "received"], prefixes=["/", "!", "."]))
async def my_gifts(_, message):
    try:
        uid, username = get_user_info(message)
        if not uid:
            return
        
        await get_user_data(uid)
        
        gifts_received = await gifts_collection.find({"receiver_id": uid}).to_list(length=10)
        
        if not gifts_received:
            await message.reply_text(f"📭 <b>{username}</b>, henüz hiç hediye almadınız!\n💡 Birinden size hediye göndermesini isteyebilirsiniz: /hediyegonder")
            return
        
        gifts_text = f"🎁 <b>{username} Tarafından Alınan Hediyeler:</b>\n\n"
        
        for i, gift in enumerate(gifts_received, 1):
            gifts_text += f"{i}. {gift['gift_emoji']} <b>{gift['gift_name']}</b> - Gönderen: <b>{gift['sender_name']}</b>\n"
        
        total_gifts = await gifts_collection.count_documents({"receiver_id": uid})
        gifts_text += f"\n💝 <b>Toplam alınan hediye:</b> {total_gifts}"
        
        await message.reply_text(gifts_text)
    except:
        pass

@app.on_message(filters.command(["zenginler", "top", "leaderboard"], prefixes=["/", "!", "."]))
async def leaderboard(_, message):
    try:
        top_users = await users_collection.find().sort("coins", -1).limit(10).to_list(length=10)
        
        if not top_users:
            await message.reply_text("📊 Sıralamada kullanıcı bulunamadı!")
            return
        
        leaderboard_text = "🏆 <b>En Zengin 10 Kullanıcı</b>\n\n"
        medals = ["🥇", "🥈", "🥉", "🏅", "🏅", "🏅", "🏅", "🏅", "🏅", "🏅"]
        
        for i, user in enumerate(top_users):
            medal = medals[i]
            user_id = user['user_id']
            try:
                # İsmi çekip tıklanabilir (mention) yapıyoruz
                get_user = await app.get_users(user_id)
                user_name = f"<a href='tg://user?id={user_id}'>{get_user.first_name}</a>"
            except:
                user_name = f"Kullanıcı <code>{user_id}</code>"
                
            leaderboard_text += f"{medal} {user_name} - {user['coins']} coin\n"
        
        await message.reply_text(leaderboard_text, disable_web_page_preview=True)
    except:
        pass

@app.on_message(filters.text & ~filters.regex(r"^[/!.\-]"))
async def give_coins_and_claim_gifts(_, message):
    try:
        uid, username = get_user_info(message)
        if not uid:
            return
        
        await get_user_data(uid)
        
        gift_count, bonus_coins = await claim_pending_gifts(uid, username)
        
        if gift_count > 0:
            claim_msg = f"""
🎁 <b>Hediyeler Alındı!</b>

<b>{username}</b>, bekleyen <b>{gift_count}</b> hediyeni aldın!
💰 <b>Kazanılan bonus:</b> {bonus_coins} coin

Aldığın hediyeleri görmek için /hediyelerim yazabilirsin! 💝
            """
            await message.reply_text(claim_msg)
        
        if random.randint(1, 100) <= 20:
            await update_user_coins(uid, 1)
    except:
        pass
