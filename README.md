# 🎵 Nova Music Bot

<p align="center">
  <img src="https://img.shields.io/badge/Nova%20Music%20Bot-blue?style=for-the-badge&logo=telegram&logoColor=white" alt="Nova Music Bot">
</p>

<p align="center">
  <b>Gelişmiş Telegram Müzik Botu - Yüksek Kaliteli Ses Akışı ve Gelişmiş Özellikler</b>
</p>

## ✨ Özellikler

- 🎧 **Yüksek Kaliteli Müzik Oynatma** - YouTube, Spotify, SoundCloud desteği
- 📥 **Video ve Ses İndirme** - Farklı kalite seçenekleri
- 📢 **Gelişmiş Broadcast Sistemi** - Kullanıcı ve grup yönetimi
- 🎵 **Playlist Yönetimi** - Özel playlist oluşturma ve yönetimi
- 🔧 **Gelişmiş Yönetim Paneli** - Detaylı istatistikler ve moderasyon
- 🌍 **Çoklu Dil Desteği** - Türkçe ve İngilizce
- 🎚️ **Ses Kalitesi Ayarları** - Yüksek bitrate ve stereo ses

## 🚀 Komutlar

### 🎧 Müzik Oynatma
| Komut | Açıklama |
|-------|----------|
| `/oynat <şarkı>` | Şarkı çalar |
| `/durdur` | Müziği duraklatır |
| `/devam` | Müziği devam ettirir |
| `/bitir` | Müziği durdurur |
| `/atla` | Şarkıyı atlar |
| `/liste` | Kuyruğu gösterir |

### 📥 İndirme
| Komut | Açıklama |
|-------|----------|
| `/indir <url>` | Video indirir |

### 📢 Yönetim
| Komut | Açıklama |
|-------|----------|
| `/yayınla` | Toplu mesaj gönderir |
| `/yayınla -u` | Sadece kullanıcılara gönderir |
| `/yayınla -g` | Sadece gruplara gönderir |
| `/istatistik` | Bot istatistiklerini gösterir |

## 🛠️ Kurulum

### Gereksinimler
- Python 3.8+
- FFmpeg
- MongoDB
- Telegram Bot Token

### Adım 1: Repoyu Klonlayın
```bash
git clone https://github.com/your-username/nova-music-bot.git
cd nova-music-bot
```

### Adım 2: Gerekli Paketleri Yükleyin
```bash
pip install -r requirements.txt
```

### Adım 3: FFmpeg Kurulumu
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install ffmpeg

# CentOS/RHEL
sudo yum install ffmpeg

# macOS
brew install ffmpeg
```

### Adım 4: Environment Variables
```bash
cp .env.example .env
```

`.env` dosyasını düzenleyin:
```env
API_ID=your_api_id_here
API_HASH=your_api_hash_here
BOT_TOKEN=your_bot_token_here
OWNER_ID=your_telegram_user_id_here
SUDO_USERS=user_id1,user_id2,user_id3
STRING_SESSION=your_session_string_here
MONGO_URI=mongodb://localhost:27017
```

### Adım 5: Session String Oluşturma
PyTgCalls için userbot session string'i gereklidir:

```bash
python generate_session.py
```

Bu script:
1. Telegram hesabınızla giriş yapmanızı ister
2. Session string oluşturur
3. `.env` dosyasına eklemeniz için gösterir

### Adım 6: Botu Çalıştırın
```bash
python start.py
```

## 📊 Bot İstatistikleri

- 👥 **Toplam Kullanıcı:** Dinamik sayı
- 💬 **Toplam Sohbet:** Dinamik sayı
- 🎵 **Toplam Şarkı:** Dinamik sayı
- 🎧 **Aktif Sohbet:** Dinamik sayı
- 📋 **Toplam Kuyruk:** Dinamik sayı

## 🔧 Gelişmiş Özellikler

### 🎚️ Ses Kalitesi
- **Bitrate:** 48kbps (yüksek kalite)
- **Channels:** Stereo (2 kanal)
- **Sample Rate:** 48kHz

### 📱 Kullanıcı Arayüzü
- Inline butonlar
- Medya mesajları
- İlerleme çubuğu
- Ses kontrolü

### 🔄 Otomatik Özellikler
- Akıllı kuyruk sistemi
- Otomatik devam
- Döngü modu
- Karıştırma

## 🌐 Desteklenen Platformlar

- ✅ **YouTube** - Tam destek
- ✅ **Spotify** - API entegrasyonu
- ✅ **SoundCloud** - Tam destek
- ✅ **Yerel Dosyalar** - Telegram dosyaları

## 📞 Destek

- 👤 **Yapımcı:** [@dnztrmnn](https://t.me/dnztrmnn)
- 💬 **Sohbet Grubu:** [@sohbetgo_tr](https://t.me/sohbetgo_tr)
- 📢 **Resmi Kanal:** Yakında açılacak

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 🤝 Katkıda Bulunma

1. Bu repoyu fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## ⚠️ Önemli Notlar

- Bot sadece sesli sohbetlerde çalışır
- Yönetici yetkileri gereklidir
- Rate limiting'e dikkat edin
- MongoDB bağlantısı zorunludur

---

<p align="center">
  <b>🎵 Nova Music Bot ile müzik keyfini yaşayın! 🎵</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Made%20with%20%E2%9D%A4%EF%B8%8F%20by-dnztrmnn-red?style=for-the-badge" alt="Made with love">
</p>
