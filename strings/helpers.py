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


HELP_1 = """<b><u>👮‍♂️ YÖNETİCİ KOMUTLARI :</b></u>

Komutları kanal için kullanmak istiyorsanız başına <b>c</b> ekleyin.

/play /oynat : Müzik veya video oynatır.
/pause /duraklat : Geçerli yayını duraklatır.
/resume /devam : Duraklatılan yayını devam ettirir.
/skip /geç : Geçerli yayını atlar, sıradaki parçayı çalar.
/end /stop /bitir /durdur : Kuyruğu temizler ve yayını sonlandırır.
/player /panel : Etkileşimli oynatma paneli gösterir.
/queue /list /liste : Kuyruktaki parçaların listesini gösterir.
"""

HELP_2 = """
<b><u>👤 YETKİLİ KULLANICILAR (AUTH USERS) :</b></u>

Yetkili kullanıcılar, sohbette yönetici olmadan botun yönetici komutlarını kullanabilirler.

/auth [kullanıcı_adı veya kullanıcı_id] : Bir kullanıcıyı botun yetkili listesine ekler.
/unauth [kullanıcı_adı veya kullanıcı_id] : Kullanıcıyı yetkili listesinden kaldırır.
/authusers : Grubun yetkili kullanıcılarını listeler.
"""

HELP_3 = """
<u><b>ʏᴀʏɪɴʟᴀ ᴏ̈ᴢᴇʟʟɪɢ̆ɪ</b></u> [sᴀᴅᴇᴄᴇ sᴜᴅᴏ ᴋᴜʟʟᴀɴɪᴄɪʟᴀʀɪ ɪᴄ̧ɪɴ] :

/broadcast [ᴍᴇsᴀᴊ ᴠᴇʏᴀ ʙɪʀ ᴍᴇsᴀᴊᴀ ᴄᴇᴠᴀᴘ] : ʙᴏᴛᴜɴ ʜɪᴢᴍᴇᴛ ᴠᴇʀᴅɪɢ̆ɪ sᴏʜʙᴇᴛʟᴇʀᴇ ᴍᴇsᴀᴊ ʏᴀʏɪɴʟᴀʀ.

<u>ʏᴀʏɪɴʟᴀ ᴍᴏᴅʟᴀʀɪ :</u>
<b>-pin</b> : ʏᴀʏɪɴʟᴀɴᴀɴ ᴍᴇsᴀᴊʟᴀʀɪɴɪᴢɪ sᴏʜʙᴇᴛʟᴇʀᴅᴇ sᴀʙɪᴛʟᴇʀ.
<b>-pinloud</b> : ʏᴀʏɪɴʟᴀɴᴀɴ ᴍᴇsᴀᴊɪ sᴀʙɪᴛʟᴇʀ ᴠᴇ ᴜʏᴇʟᴇʀᴇ ʙɪʟᴅɪʀɪᴍ ɢᴏ̈ɴᴅᴇʀɪʀ.
<b>-user</b> : ʙᴏᴛᴜɴᴜᴢᴜ ʙᴀşʟᴀᴛᴀɴ ᴋᴜʟʟᴀɴɪᴄɪʟᴀʀᴀ ᴍᴇsᴀᴊ ʏᴀʏɪɴʟᴀʀ.
<b>-assistant</b> : ʙᴏᴛᴜɴ ᴀsɪsᴛᴀɴ ʜᴇsᴀʙɪɴᴅᴀɴ ᴍᴇsᴀᴊ ʏᴀʏɪɴʟᴀʀ.
<b>-nobot</b> : ʙᴏᴛᴜɴ ᴍᴇsᴀᴊ ʏᴀʏɪɴʟᴀᴍᴀsɪɴɪ ᴢᴏʀʟᴀ ᴇɴɢᴇʟʟᴇʀ.

<b>ᴏ̈ʀɴᴇᴋ:</b> <code>/broadcast -user -assistant -pin ʏᴀʏɪɴ ᴅᴇɴᴇᴍᴇsɪ</code>
"""

HELP_4 = """<u><b>ᴄʜᴀᴛ ᴋᴀʀᴀ ʟɪsᴛᴇ ᴏ̈ᴢᴇʟʟɪɢ̆ɪ :</b></u> [sᴀᴅᴇᴄᴇ sᴜᴅᴏ ᴋᴜʟʟᴀɴɪᴄɪʟᴀʀɪ ɪᴄ̧ɪɴ]

ɢᴇʀᴇᴋsɪᴢ sᴏʜʙᴇᴛʟᴇʀɪ ᴋɪᴍᴇᴛʟɪ ʙᴏᴛᴜᴍᴜᴢᴅᴀɴ ᴜᴢᴀᴋ ᴛᴜᴛᴜɴ.

/blacklistchat [sᴏʜʙᴇᴛ ɪᴅ] : ʙɪʀ sᴏʜʙᴇᴛɪ ʙᴏᴛᴜ ᴋᴜʟʟᴀɴᴀᴍᴀᴢ ʜᴀʟᴇ ɢᴇᴛɪʀɪʀ.
/whitelistchat [sᴏʜʙᴇᴛ ɪᴅ] : ᴋᴀʀᴀ ʟɪsᴛᴇʏᴇ ᴀʟɪɴᴍɪş sᴏʜʙᴇᴛɪ ʙᴇʏᴀᴢ ʟɪsᴛᴇʏᴇ ᴇᴋʟᴇʀ.
/blacklistedchat : ᴋᴀʀᴀ ʟɪsᴛᴇʏᴇ ᴀʟɪɴᴀɴ sᴏʜʙᴇᴛʟᴇʀɪɴ ʟɪsᴛᴇsɪɴɪ ɢᴏ̈sᴛᴇʀɪʀ.
"""

HELP_5 = """
<u><b>ᴋᴜʟʟᴀɴɪᴄɪʟᴀʀɪ ᴇɴɢᴇʟʟᴇ:</b></u> [sᴀᴅᴇᴄᴇ sᴜᴅᴏ ᴋᴜʟʟᴀɴɪᴄɪʟᴀʀɪ ɪᴄ̧ɪɴ]

ᴋᴀʀᴀ ʟɪsᴛᴇʏᴇ ᴀʟɪɴᴀɴ ᴋᴜʟʟᴀɴɪᴄɪʏɪ ʏᴏᴋ sᴀʏᴀʀ ᴠᴇ ʙᴏᴛ ᴋᴏᴍᴜᴛʟᴀʀɪɴɪ ᴋᴜʟʟᴀɴᴀᴍᴀᴢ.

/block [ᴋᴜʟʟᴀɴɪᴄɪ ᴀᴅɪ ᴠᴇʏᴀ ʙɪʀ ᴋᴜʟʟᴀɴɪᴄɪʏᴀ ʏᴀɴɪᴛ] : ᴋᴜʟʟᴀɴɪᴄɪʏɪ ʙᴏᴛᴜᴍᴜᴢᴅᴀɴ ᴇɴɢᴇʟʟᴇʀ.
/unblock [ᴋᴜʟʟᴀɴɪᴄɪ ᴀᴅɪ ᴠᴇʏᴀ ʙɪʀ ᴋᴜʟʟᴀɴɪᴄɪʏᴀ ʏᴀɴɪᴛ] : ᴇɴɢᴇʟʟɪ ᴋᴜʟʟᴀɴɪᴄɪɴɪɴ ᴇɴɢᴇʟɪɴɪ ᴋᴀʟᴅɪʀɪʀ.
/blockedusers : ᴇɴɢᴇʟʟɪ ᴋᴜʟʟᴀɴɪᴄɪʟᴀʀɪɴ ʟɪsᴛᴇsɪɴɪ ɢᴏ̈sᴛᴇʀɪʀ.
"""
HELP_6 = """
<u><b>ᴋᴀɴᴀʟ ᴏʏɴᴀᴛᴍᴀ ᴋᴏᴍᴜᴛʟᴀʀɪ:</b></u>

ᴋᴀɴᴀʟᴅᴀ sᴇs/vɪᴅᴇᴏ ʏᴀʏıɴʟᴀʏᴀʙɪʟɪʀsɪɴɪᴢ.

/cplay : ɪsᴛᴇɴᴇɴ sᴇs ᴘᴀʀᴄ̧ᴀsıɴı ᴋᴀɴᴀʟıɴ sᴇsʟɪ sᴏʜʙᴇᴛɪɴᴅᴇ ʏᴀʏıɴʟᴀᴍᴀʏᴀ ʙᴀşʟᴀʀ.
/cvplay : ɪsᴛᴇɴᴇɴ ᴠɪᴅᴇᴏ ᴘᴀʀᴄ̧ᴀsıɴı ᴋᴀɴᴀʟıɴ sᴇsʟɪ sᴏʜʙᴇᴛɪɴᴅᴇ ʏᴀʏıɴʟᴀᴍᴀʏᴀ ʙᴀşʟᴀʀ.
/cplayforce veya /cvplayforce : ᴅᴇᴠᴀᴍ ᴇᴅᴇɴ ʏᴀʏıɴı ᴅᴜʀᴅᴜʀᴜʀ ᴠᴇ ɪsᴛᴇɴᴇɴ ᴘᴀʀᴄ̧ᴀʏı ʏᴀʏıɴʟᴀᴍᴀʏᴀ ʙᴀşʟᴀʀ.

/channelplay [ᴋᴀɴᴀʟ ᴋᴜʟʟᴀɴıᴄı ᴀᴅı ᴠᴇʏᴀ ɪᴅ] ᴠᴇʏᴀ [ᴋᴀᴘᴀᴛ] : ʙɪʀ ᴋᴀɴᴀʟı ʙɪʀ ɢʀᴜʙᴀ ʙᴀɢ̆ʟᴀʀ ᴠᴇ ɢʀᴜᴘᴛᴀ ɢᴏ̈ɴᴅᴇʀɪʟᴇɴ ᴋᴏᴍᴜᴛʟᴀʀ ᴀʀᴀᴄ̧ıʟıɢ̆ıʏʟᴀ ᴘᴀʀᴄ̧ᴀʟᴀʀı ʏᴀʏıɴʟᴀᴍᴀʏᴀ ʙᴀşʟᴀʀ.
"""

HELP_7 = """
<u><b>ɢʟᴏʙᴀʟ ʏᴀsᴀᴋʟᴀᴍᴀ ᴏ̈ᴢᴇʟʟɪɢ̆ɪ</b></u> [sᴀᴅᴇᴄᴇ sᴜᴅᴏ ᴋᴜʟʟᴀɴıᴄıʟᴀʀ ɪᴄ̧ɪɴ] :

/gban [ᴋᴜʟʟᴀɴıᴄı ᴀᴅı ᴠᴇʏᴀ ʙɪʀ ᴋᴜʟʟᴀɴıᴄıʏᴀ ʏᴀɴıᴛ] : ᴋᴜʟʟᴀɴıᴄıʏı ᴛᴜ̈ᴍ sᴜɴᴜʟᴀɴ ᴅɪʟᴇʀᴅᴇɴ ɢʟᴏʙᴀʟ ᴏʟᴀʀᴀᴋ ʏᴀsᴀᴋʟᴀʀ ᴠᴇ ʙᴏᴛᴜ ᴋᴜʟʟᴀɴᴍᴀsıɴı ᴇɴɢᴇʟʟᴇʀ.
/ungban [ᴋᴜʟʟᴀɴıᴄı ᴀᴅı ᴠᴇʏᴀ ʙɪʀ ᴋᴜʟʟᴀɴıᴄıʏᴀ ʏᴀɴıᴛ] : ɢʟᴏʙᴀʟ ʏᴀsᴀᴋʟᴀᴍᴀʏı ᴋᴀʟᴅıʀıʀ.
/gbannedusers : ɢʟᴏʙᴀʟ ᴏʟᴀʀᴀᴋ ʏᴀsᴀᴋʟᴀɴᴀɴ ᴋᴜʟʟᴀɴıᴄıʟᴀʀıɴ ʟɪsᴛᴇsɪɴɪ ɢᴏ̈sᴛᴇʀɪʀ.
"""

HELP_8 = """
<b><u>ᴅᴏ̈ɴɢᴜ̈ʟᴜ̈ ᴏʏɴᴀᴛᴍᴀ :</b></u>

<b>ᴍᴇᴠᴄᴜᴛ ʏᴀʏıɴı ᴅᴏ̈ɴɢᴜ̈ ɪᴄ̧ᴇʀɪsɪɴᴅᴇ ᴛᴇᴋʀᴀʀʟᴀʏᴀʀᴀᴋ ᴏʏɴᴀᴛıʀ</b>

/loop [aç/kapat] : ᴍᴇᴠᴄᴜᴛ ʏᴀʏıɴ ɪᴄ̧ɪɴ ᴅᴏ̈ɴɢᴜ̈ʏᴜ̈ ᴀᴄ̧ᴀʀ ᴠᴇʏᴀ ᴋᴀᴘᴀᴛıʀ.
/loop [1, 2, 3, ...] : ᴠᴇʀɪʟᴇɴ sᴀʏı ᴋᴀᴅᴀʀ ᴅᴏ̈ɴɢᴜ̈ʟᴜ̈ ᴏʏɴᴀᴛᴍᴀʏı ᴀᴄ̧ᴀʀ.
"""
HELP_9 = """
<u><b>ʙᴀᴋıᴍ ᴍᴏᴅᴜ</b></u> [sᴀᴅᴇᴄᴇ sᴜᴅᴏ ᴋᴜʟʟᴀɴıᴄıʟᴀʀ ɪᴄ̧ɪɴ] :

/logs : ʙᴏᴛ ɢᴜ̈ɴʟᴜ̈ᴋʟᴇʀɪɴɪ ɢᴏ̈ʀᴛ.

/logger [aç/kapat] : ʙᴏᴛᴜɴ ᴜ̈ᴢᴇʀɪɴᴅᴇ ᴏʟᴀɴ ᴛᴜ̈ᴍ ᴘʀᴏsᴇsʟᴇʀɪ ɢᴜ̈ɴʟᴜ̈ᴋʟᴇᴍᴇsɪɴɪ ᴀᴄ̧ᴀʀ ᴠᴇʏᴀ ᴋᴀᴘᴀᴛıʀ.

/maintenance [aç/kapat] : ʙᴏᴛᴜɴ ʙᴀᴋıᴍ ᴍᴏᴅᴜɴᴜ ᴀᴄ̧ᴀʀ ᴠᴇʏᴀ ᴋᴀᴘᴀᴛıʀ.
"""

HELP_10 = """
<b><u>ᴘɪɴɢ & ɪsᴛᴀᴛɪsᴛɪᴋ :</b></u>

/start : ᴍᴜ̈ᴢɪᴋ ʙᴏᴛᴜɴᴜ ʙᴀşʟᴀᴛıʀ.
/help : ᴋᴏᴍᴜᴛʟᴀʀıɴ ᴀᴄ̧ıᴋʟᴀᴍᴀʟᴀʀı ɪʟᴇ ʏᴀʀᴅıᴍ ᴍᴇɴᴜ̈sᴜ̈ɴᴜ ɢᴏ̈sᴛᴇʀɪʀ.

/ping : ʙᴏᴛᴜɴ ᴘɪɴɢ ᴠᴇ sɪsᴛᴇᴍ ɪsᴛᴀᴛɪsᴛɪᴋʟᴇʀɪɴɪ ɢᴏ̈sᴛᴇʀɪʀ.

/stats : ʙᴏᴛᴜɴ ɢᴇɴᴇʟ ɪsᴛᴀᴛɪsᴛɪᴋʟᴇʀɪɴɪ ɢᴏ̈sᴛᴇʀɪʀ.
"""

HELP_11 = """
<u><b>ᴏʏɴᴀᴛᴍᴀ ᴋᴏᴍᴜᴛʟᴀʀɪ :</b></u>

<b>v :</b> ᴠɪᴅᴇᴏ ᴏʏɴᴀᴛᴍᴀ.
<b>zorla :</b> ᴍᴇᴠᴄᴜᴛ ᴏʏɴᴀᴛᴍᴀʏɪ ᴅᴜʀᴅᴜʀᴜᴘ ʏᴇɴɪ ɪçᴇʀɪğɪ ʙᴀşʟᴀᴛᴍᴀ.

/play veya /oynat veya /vplay : ɪsᴛᴇɴɪʟᴇɴ şᴀʀᴋɪʏɪ veya ᴠɪᴅᴇᴏʏᴜ sᴇsʟɪ sᴏʜʙᴇᴛᴛᴇ ᴏʏɴᴀᴛᴍᴀʏᴀ ʙᴀşʟᴀᴛɪʀ.

/playforce veya /vplayforce : ᴅᴇᴠᴀᴍ ᴇᴅᴇɴ ᴏʏɴᴀᴛᴍᴀʏɪ ᴅᴜʀᴅᴜʀᴜʀ ᴠᴇ ɪsᴛᴇɴɪʟᴇɴ şᴀʀᴋɪʏɪ veya ᴠɪᴅᴇᴏʏᴜ ᴏʏɴᴀᴛᴍᴀʏᴀ ʙᴀşʟᴀᴛɪʀ.
"""

HELP_12 = """
<b><u>ᴋᴜʏʀᴜᴋ ᴋᴀʀɪşᴛɪʀᴍᴀ :</b></u>

/shuffle : ᴏʏɴᴀᴛᴍᴀ ᴋᴜʏʀᴜğᴜɴᴅᴀᴋɪ şᴀʀᴋɪʟᴀʀɪ ᴋᴀʀɪşᴛɪʀɪʀ.
/queue : ᴍᴇᴠᴄᴜᴛ ᴏʏɴᴀᴛᴍᴀ ᴋᴜʏʀᴜğᴜɴᴜ ɢöʀᴛᴇʀ.
"""

HELP_13 = """
<b><u>ᴀɴɪɴᴅᴀɴ ᴏʏɴᴀᴛᴍᴀ :</b></u>

/seek [sᴀɴɪʏᴇ] : ᴍᴇᴠᴄᴜᴛ ᴏʏɴᴀᴛᴍᴀʏɪ ᴠᴇʀɪʟᴇɴ sᴀɴɪʏᴇʏᴇ ᴀʟɪʀ.
/seekback [sᴀɴɪʏᴇ] : ᴍᴇᴠᴄᴜᴛ ᴏʏɴᴀᴛᴍᴀʏɪ ᴠᴇʀɪʟᴇɴ sᴀɴɪʏᴇ ɢᴇʀɪʏᴇ sᴀʀᴀʀ.
"""

HELP_14 = """
<b><u>şᴀʀᴋı ɪɴᴅɪʀᴍᴇ</b></u>

/song [şᴀʀᴋı ɪsᴍɪ/ʏᴛ ʟɪɴᴋɪ] : ʏᴏᴜᴛᴜʙᴇ'ᴅᴀɴ ɪsᴛᴇᴅɪğɪɴɪᴢ şᴀʀᴋıʏı MP3 ᴠᴇʏᴀ MP4 ғᴏʀᴍᴀᴛıɴᴅᴀ ɪɴᴅɪʀɪʀ.
"""

HELP_15 = """
<b><u>Oynatma Hızı Komutları:</u></b>

Devam eden yayının oynatma hızını kontrol edebilirsiniz. [Yalnızca yöneticiler]

/speed veya /playback : Grupta ses oynatma hızını ayarlamak için kullanılır.
/cspeed veya /cplayback : Kanallarda ses oynatma hızını ayarlamak için kullanılır.
"""

HELP_16 = """
<b><u>Gizlilik Politikası:</u></b>

/privacy : Tubidy Bot'un gizlilik politikasını görüntüler.
"""

HELP_17 = """
<b><u>Oyun Komutları:</u></b>

/dice : Zar atar.
/ludo : Ludo oyunu oynar.
/dart : Dart atar.
/basket veya /basketball : Basketbol oynar.
/football : Futbol oynar.
/slot veya /jackpot : Jackpot oynar.
/bowling : Bowling oynar.
"""

HELP_18 = """
<b><u>Yönetici Komutları:</u></b>

/ban - Bir kullanıcıyı yasaklar.
/banall - Tüm kullanıcıları yasaklar.
/sban - Kullanıcının grupta gönderdiği tüm mesajları siler ve yasaklar.
/tban - Bir kullanıcıyı belirli süreliğine yasaklar.
/unban - Yasaklı bir kullanıcıyı serbest bırakır.
/warn - Bir kullanıcıya uyarı verir.
/swarn - Kullanıcının tüm mesajlarını siler ve uyarı verir.
/rmwarns - Bir kullanıcının tüm uyarılarını kaldırır.
/warns - Bir kullanıcının mevcut uyarılarını gösterir.
/kick - Bir kullanıcıyı gruptan atar.
/skick - Yanıt verilen mesajı siler ve göndereni gruptan atar.
/purge - Mesajları temizler.
/purge [n] - Yanıtlanan mesajdan itibaren "n" kadar mesajı temizler.
/del - Yanıtlanan mesajı siler.
/promote - Bir üyeyi yönetici yapar.
/fullpromote - Bir üyeyi tüm yetkilerle yönetici yapar.
/demote - Bir yöneticinin yetkilerini alır.
/pin - Bir mesajı sabitler.
/unpin - Sabitlenmiş bir mesajı kaldırır.
/unpinall - Tüm sabitlenmiş mesajları kaldırır.
/mute - Bir kullanıcıyı susturur.
/tmute - Bir kullanıcıyı belirli süreliğine susturur.
/unmute - Susturulmuş bir kullanıcıyı serbest bırakır.
/zombies - Silinmiş hesapları yasaklar.
/report veya @admins veya @admin - Bir mesajı yöneticilere bildirir.
"""

HELP_19 = """
<b><u>📷 Görsel Bağlantı Oluşturucu:</u></b>

/tgm - Herhangi bir resme, videoya veya GIF’e yanıt vererek bağlantı oluşturur.
"""

HELP_20 = """
<b><u>🏷️ Etiketleme Komutları:</u></b>

/tagall [mesajınız veya bir mesaja yanıt] - Gruptaki tüm üyeleri etiketler.
/admins [mesajınız veya bir mesaja yanıt] - Gruptaki tüm yöneticileri etiketler.
"""

HELP_21 = """
<b><u>📥 Video İndirme:</u></b>

/vid - Instagram, Twitter ve diğer platformlardan video indirir.
"""

HELP_22 = """
🔊 <b>Metinden Konuşmaya (TTS)</b> 🎤

• /tts <metin> - Yazdığınız metni sesli olarak okur.
<b>Örnek:</b>
/tts Merhaba, nasılsınız? 🙏

<b>Not:</b> Komuttan sonra mutlaka bir metin yazmalısınız.
"""

HELP_23 = """
🔗 <b>Davet Bağlantısı Komutları</b> 💫

• /givelink - Mevcut sohbetin davet bağlantısını alır.
• /link <grup_id> - Belirtilen grup için davet bağlantısı oluşturur.
"""

HELP_24 = """
🔒 <b>Zorunlu Kanal Aboneliği</b> 🎯

• /fsub <kanal kullanıcı adı veya ID> - Bu grup için zorunlu kanal aboneliği ayarlar.
• /fsub off - Zorunlu kanal aboneliğini kapatır.
"""

HELP_25 = """
🧟 <b>Silinmiş Hesaplar</b> 💀

• /zombies - Gruptaki silinmiş hesapları tespit eder ve yasaklar.
"""

HELP_26 = """
👤 <b>Kullanıcı Bilgisi</b> 📊

• /info <kullanıcı_id> - Bir kullanıcı hakkında detaylı bilgi alır.
• /userinfo <kullanıcı_id> - /info komutunun kısayolu.
"""

HELP_27 = """
📁 <b>GitHub Depo İndirici</b> 🐙

• /downloadrepo <repo_url> - Belirtilen GitHub deposunu indirir ve zip dosyası olarak gönderir.
"""

HELP_28 = """
🎲 <b>Doğruluk mu Cesaret mi?</b> 🎯

• /truth - Rastgele bir doğruluk sorusu getirir.
• /dare - Rastgele bir cesaret görevi verir.
"""

HELP_29 = """
🍃 <b>MongoDB Bağlantı Kontrolü</b> 🔍

• /mongochk <mongo_url> - MongoDB bağlantısını test eder.
"""

HELP_30 = """
🔤 <b>Yazı Tipi Dönüştürücü</b> ✨

• /font <metin> - Yazınızı farklı yazı tipleriyle dönüştürür.
"""

HELP_31 = """ 📜 <b>ŞİİR & SÖZ KOMUTLARI</b> ✍️

/siir - Rastgele şiir gönderir  
/soz - Rastgele söz gönderir  

🔐 <b>Sadece bot sahibi kullanabilir:</b>  
/siirekle &lt;şiir&gt; - Yeni şiir ekler  
/sozekle &lt;söz&gt; - Yeni söz ekler  

Örnek:  
<code>/siirekle Geceye şiir gibi düştün.</code>  
<code>/sozekle Yalnızlık paylaşılmaz.</code>
"""

# 🤖 BOT LIST
HELP_32 = """ 🤖 <b>BOT LIST</b> 🎯

• /bots - Get a list of bots in the group 📋 """

# 📝 MARKDOWN HELP
HELP_33 = """ 📝 <b>MARKDOWN HELP</b> 📖

• /markdownhelp - Help about using Markdown formatting in messages 🔧 """

HELP_34 = """ 🏷️ <b>ÖZEL TAG YARDIMI</b> 🌟

<b>Günaydın:</b> 🌅
• /gtag - Günaydın mesajlarını başlat ☀️

<b>İyi Akşamlar:</b> 🌞
• /itag - İyi akşamlar mesajlarını başlat 🌤️

<b>İyi Geceler:</b> 🌙
• /stag - İyi geceler mesajlarını başlat 🌜

<b>Kurt Oyunu:</b> 🐺
• /ktag - Kurt oyunu çağırmalarını başlat ⚔️

<b>Yardımcı Komutlar:</b> ⚙️
• /cancel - Aktif tüm mesajları durdur 🚫
• /taghelp - Bu yardım mesajını göster 📖

<b>Not:</b> Aynı anda bir sohbet için sadece bir mesajlaşma oturumu çalışabilir 📌
"""

HELP_35 = """ 👋 <b>KULLANICI KARŞILAMA MESAJI</b> 🎉

• /welcome on - Yeni üyeler için karşılama mesajını aç ✅
• /welcome off - Karşılama mesajını kapat ❌ """


# ©️ Copyright Reserved - @NoxxOP  Nand Yaduwanshi

# ===========================================
# ©️ 2025 Nand Yaduwanshi (aka @NoxxOP)
# 🔗 GitHub : https://github.com/NoxxOP/ShrutiMusic
# 📢 Telegram Channel : https://t.me/ShrutiBots
# ===========================================
