# Copyright (c) 2025 Nand Yaduwanshi <NoxxOP>
# Location: Supaul, Bihar
#
# Tüm hakları saklıdır.
#
# Bu kod Nand Yaduwanshi'nin fikri mülkiyetidir.
# Açık izin olmadan bu kodu kopyalamak, değiştirmek, yeniden dağıtmak
# veya ticari / kişisel projelerde kullanmak yasaktır.
#
# İzin Verilen:
# - Kişisel öğrenme amacıyla forklamak
# - Pull request ile geliştirme önerileri sunmak
#
# Yasak:
# - Bu kodu kendi kodunuzmuş gibi göstermek
# - İzin veya kaynak belirtmeden yeniden yüklemek
# - Ticari amaçla kullanmak
#
# İzinler için iletişim:
# E-posta: badboy809075@gmail.com

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.enums import ParseMode
from ShrutiMusic import app
import config

TEXT = f"""
🔒 **{app.mention} için Gizlilik Politikası!**

Gizliliğiniz bizim için önemlidir. Verilerinizi nasıl topladığımız, kullandığımız ve koruduğumuz hakkında daha fazla bilgi edinmek için lütfen Gizlilik Politikamızı inceleyin: [Gizlilik Politikası]({config.PRIVACY_LINK}).

Herhangi bir sorunuz veya endişeniz varsa, lütfen [destek ekibimizle](https://t.me/ShrutiBotSupport) iletişime geçin.
"""

@app.on_message(filters.command("privacy"))
async def privacy(client, message: Message):
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Gizlilik Politikasını Görüntüle", url=config.SUPPORT_GROUP
                )
            ]
        ]
    )
    await message.reply_text(
        TEXT, 
        reply_markup=keyboard, 
        parse_mode=ParseMode.MARKDOWN, 
        disable_web_page_preview=True
    )

# ©️ Telif Hakkı Saklıdır - @NoxxOP  Nand Yaduwanshi

# ===========================================
# ©️ 2025 Nand Yaduwanshi (aka @NoxxOP)
# 🔗 GitHub : https://github.com/NoxxOP/ShrutiMusic
# 📢 Telegram Kanalı : https://t.me/ShrutiBots
# ===========================================
