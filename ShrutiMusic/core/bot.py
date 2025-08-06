# Telif Hakkı (c) 2025 Nand Yaduwanshi <NoxxOP>
# Konum: Supaul, Bihar
#
# Tüm hakları saklıdır.
#
# Bu kod Nand Yaduwanshi'nin fikri mülkiyetidir.
# Açık izin olmadan bu kodu kopyalamak, değiştirmek, yeniden dağıtmak
# veya ticari / kişisel projelerde kullanmak yasaktır.
#
# İzin verilenler:
# - Kendi öğreniminiz için forklayabilirsiniz
# - Pull request ile geliştirme gönderebilirsiniz
#
# İzin verilmeyenler:
# - Kodu kendinize aitmiş gibi göstermek
# - İzin veya kredi vermeden yeniden yüklemek
# - Satmak veya ticari amaçla kullanmak
#
# İzin almak için iletişim:
# E-posta: badboy809075@gmail.com

import uvloop

uvloop.install()

import pyrogram
from pyrogram import Client
from pyrogram.enums import ChatMemberStatus, ParseMode
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

import config

from ..logging import LOGGER


class Aviax(Client):
    def __init__(self):
        LOGGER(__name__).info("Bot başlatılıyor...")
        super().__init__(
            name="ShrutiMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            parse_mode=ParseMode.HTML,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()
        get_me = await self.get_me()
        self.username = get_me.username
        self.id = get_me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.mention = self.me.mention

        # Davet butonu oluştur
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="📌 Beni Grubuna Ekle",
                        url=f"https://t.me/{self.username}?startgroup=true",
                    )
                ]
            ]
        )

        # Log grubuna mesaj gönder
        if config.LOG_GROUP_ID:
            try:
                await self.send_photo(
                    config.LOG_GROUP_ID,
                    photo=config.START_IMG_URL,
                    caption=(
                        f"╔════❰ 𝗛𝗢𝗦𝗚𝗘𝗟𝗗𝗜𝗡 ❱════❍⊱❁۪۪\n"
                        f"║\n"
                        f"║┣⪼ 🎉 Bot başlatıldı!\n"
                        f"║\n"
                        f"║┣⪼ 🤖 Ad: {self.name}\n"
                        f"║┣⪼ 🆔 ID: `{self.id}`\n"
                        f"║┣⪼ 📌 Kullanıcı Adı: @{self.username}\n"
                        f"║\n"
                        f"║💖 Kullandığınız için teşekkürler!\n"
                        f"╚════════════════❍⊱❁"
                    ),
                    reply_markup=button,
                )
            except pyrogram.errors.ChatWriteForbidden as e:
                LOGGER(__name__).error(f"Bot log grubuna yazamıyor: {e}")
                try:
                    await self.send_message(
                        config.LOG_GROUP_ID,
                        (
                            f"╔═══❰ 𝗛𝗢𝗦𝗚𝗘𝗟𝗗𝗜𝗡 ❱═══❍⊱❁۪۪\n"
                            f"║\n"
                            f"║┣⪼ 🎉 Bot başlatıldı!\n"
                            f"║\n"
                            f"║🤖 Ad: {self.name}\n"
                            f"║🆔 ID: `{self.id}`\n"
                            f"║📌 Kullanıcı Adı: @{self.username}\n"
                            f"║\n"
                            f"║💖 Kullandığınız için teşekkürler!\n"
                            f"╚══════════════❍⊱❁"
                        ),
                        reply_markup=button,
                    )
                except Exception as e:
                    LOGGER(__name__).error(f"Log grubuna mesaj gönderilemedi: {e}")
            except Exception as e:
                LOGGER(__name__).error(f"Log grubuna gönderimde beklenmeyen hata: {e}")
        else:
            LOGGER(__name__).warning("LOG_GROUP_ID ayarlanmamış, log mesajı gönderilmeyecek.")

        # Bot log grubunda admin mi kontrol et
        if config.LOG_GROUP_ID:
            try:
                chat_member_info = await self.get_chat_member(
                    config.LOG_GROUP_ID, self.id
                )
                if chat_member_info.status != ChatMemberStatus.ADMINISTRATOR:
                    LOGGER(__name__).error("Lütfen botu log grubunda yönetici yapın.")
            except Exception as e:
                LOGGER(__name__).error(f"Bot durum kontrolünde hata: {e}")

        LOGGER(__name__).info(f"Müzik Botu {self.name} olarak başlatıldı.")

    async def stop(self):
        await super().stop()
        LOGGER(__name__).info("Bot durduruldu.")


# ©️ Telif Hakkı Saklıdır - @NoxxOP  Nand Yaduwanshi
# ===========================================
# ©️ 2025 Nand Yaduwanshi (aka @NoxxOP)
# 🔗 GitHub : https://github.com/NoxxOP/ShrutiMusic
# 📢 Telegram Kanalı : https://t.me/ShrutiBots
# ===========================================
