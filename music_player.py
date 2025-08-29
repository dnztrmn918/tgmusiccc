#!/usr/bin/env python3
"""
🎵 Gelişmiş Müzik Oynatıcı Modülü
✨ Özellikler:
- Çoklu platform desteği (YouTube, Spotify, SoundCloud)
- Yüksek kaliteli ses akışı
- Playlist yönetimi
- Otomatik kuyruk sistemi
- Ses kalitesi ayarları
"""

import asyncio
import logging
import os
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

import yt_dlp
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import aiohttp
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped, AudioParameters, VideoPiped, VideoParameters

logger = logging.getLogger(__name__)

@dataclass
class Track:
    """Şarkı bilgilerini tutan sınıf"""
    title: str
    artist: str
    duration: int
    url: str
    thumbnail: str
    source: str
    webpage_url: str
    audio_url: Optional[str] = None
    video_url: Optional[str] = None

class AdvancedMusicPlayer:
    def __init__(self, calls: PyTgCalls):
        self.calls = calls
        self.queues: Dict[int, List[Track]] = {}
        self.current_tracks: Dict[int, Track] = {}
        self.playlists: Dict[int, List[Track]] = {}
        self.is_playing: Dict[int, bool] = {}
        self.volume: Dict[int, int] = {}
        
        # Platform ayarları
        self.spotify_client = None
        self.setup_spotify()
        
        # yt-dlp ayarları
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'extractaudio': True,
            'audioformat': 'mp3',
            'outtmpl': '%(title)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        
    def setup_spotify(self):
        """Spotify API'sini ayarlar"""
        try:
            client_id = os.getenv("SPOTIFY_CLIENT_ID")
            client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
            
            if client_id and client_secret:
                self.spotify_client = spotipy.Spotify(
                    client_credentials_manager=SpotifyClientCredentials(
                        client_id=client_id,
                        client_secret=client_secret
                    )
                )
                logger.info("✅ Spotify API başarıyla ayarlandı")
        except Exception as e:
            logger.warning(f"⚠️ Spotify API ayarlanamadı: {e}")
    
    async def search_track(self, query: str, platform: str = "auto") -> Optional[Track]:
        """Şarkı arar ve Track objesi döner"""
        try:
            if platform == "spotify" and self.spotify_client:
                return await self.search_spotify(query)
            elif platform == "soundcloud":
                return await self.search_soundcloud(query)
            else:
                return await self.search_youtube(query)
        except Exception as e:
            logger.error(f"Search error: {e}")
            return None
    
    async def search_youtube(self, query: str) -> Optional[Track]:
        """YouTube'da şarkı arar"""
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                # YouTube arama
                if not query.startswith(('http://', 'https://')):
                    query = f"ytsearch:{query}"
                
                info = ydl.extract_info(query, download=False)
                
                if 'entries' in info and info['entries']:
                    entry = info['entries'][0]
                else:
                    entry = info
                
                return Track(
                    title=entry.get('title', 'Unknown'),
                    artist=entry.get('uploader', 'Unknown'),
                    duration=entry.get('duration', 0),
                    url=entry.get('url', ''),
                    thumbnail=entry.get('thumbnail', ''),
                    source='youtube',
                    webpage_url=entry.get('webpage_url', ''),
                    audio_url=entry.get('url', '')
                )
        except Exception as e:
            logger.error(f"YouTube search error: {e}")
            return None
    
    async def search_spotify(self, query: str) -> Optional[Track]:
        """Spotify'da şarkı arar"""
        try:
            if not self.spotify_client:
                return None
                
            results = self.spotify_client.search(q=query, type='track', limit=1)
            
            if results['tracks']['items']:
                track = results['tracks']['items'][0]
                
                # YouTube'da arama yaparak ses URL'sini al
                search_query = f"{track['name']} {track['artists'][0]['name']}"
                youtube_track = await self.search_youtube(search_query)
                
                if youtube_track:
                    return Track(
                        title=track['name'],
                        artist=track['artists'][0]['name'],
                        duration=track['duration_ms'] // 1000,
                        url=youtube_track.audio_url,
                        thumbnail=track['album']['images'][0]['url'] if track['album']['images'] else '',
                        source='spotify',
                        webpage_url=track['external_urls']['spotify'],
                        audio_url=youtube_track.audio_url
                    )
        except Exception as e:
            logger.error(f"Spotify search error: {e}")
            return None
    
    async def search_soundcloud(self, query: str) -> Optional[Track]:
        """SoundCloud'da şarkı arar"""
        try:
            # SoundCloud için özel yt-dlp ayarları
            sc_opts = self.ydl_opts.copy()
            sc_opts['extractaudio'] = False
            
            with yt_dlp.YoutubeDL(sc_opts) as ydl:
                if not query.startswith(('http://', 'https://')):
                    query = f"scsearch:{query}"
                
                info = ydl.extract_info(query, download=False)
                
                if 'entries' in info and info['entries']:
                    entry = info['entries'][0]
                else:
                    entry = info
                
                return Track(
                    title=entry.get('title', 'Unknown'),
                    artist=entry.get('uploader', 'Unknown'),
                    duration=entry.get('duration', 0),
                    url=entry.get('url', ''),
                    thumbnail=entry.get('thumbnail', ''),
                    source='soundcloud',
                    webpage_url=entry.get('webpage_url', ''),
                    audio_url=entry.get('url', '')
                )
        except Exception as e:
            logger.error(f"SoundCloud search error: {e}")
            return None
    
    async def add_to_queue(self, chat_id: int, track: Track) -> bool:
        """Şarkıyı kuyruğa ekler"""
        try:
            if chat_id not in self.queues:
                self.queues[chat_id] = []
            
            self.queues[chat_id].append(track)
            return True
        except Exception as e:
            logger.error(f"Add to queue error: {e}")
            return False
    
    async def play_track(self, chat_id: int, track: Track) -> bool:
        """Şarkıyı çalar"""
        try:
            self.current_tracks[chat_id] = track
            self.is_playing[chat_id] = True
            
            # Ses kalitesi ayarları
            audio_params = AudioParameters(
                bitrate=48000,
                channels=2,
                sample_rate=48000
            )
            
            await self.calls.join_group_call(
                chat_id,
                AudioPiped(
                    track.audio_url or track.url,
                    audio_params
                )
            )
            
            return True
        except Exception as e:
            logger.error(f"Play track error: {e}")
            self.is_playing[chat_id] = False
            return False
    
    async def play_next(self, chat_id: int) -> bool:
        """Sıradaki şarkıyı çalar"""
        try:
            if chat_id not in self.queues or not self.queues[chat_id]:
                await self.stop_playback(chat_id)
                return False
            
            track = self.queues[chat_id].pop(0)
            return await self.play_track(chat_id, track)
        except Exception as e:
            logger.error(f"Play next error: {e}")
            return False
    
    async def pause_playback(self, chat_id: int) -> bool:
        """Çalmayı duraklatır"""
        try:
            if chat_id in self.is_playing and self.is_playing[chat_id]:
                await self.calls.pause_stream(chat_id)
                return True
            return False
        except Exception as e:
            logger.error(f"Pause error: {e}")
            return False
    
    async def resume_playback(self, chat_id: int) -> bool:
        """Çalmayı devam ettirir"""
        try:
            if chat_id in self.is_playing and not self.is_playing[chat_id]:
                await self.calls.resume_stream(chat_id)
                self.is_playing[chat_id] = True
                return True
            return False
        except Exception as e:
            logger.error(f"Resume error: {e}")
            return False
    
    async def stop_playback(self, chat_id: int) -> bool:
        """Çalmayı durdurur"""
        try:
            await self.calls.leave_group_call(chat_id)
            
            if chat_id in self.current_tracks:
                del self.current_tracks[chat_id]
            if chat_id in self.is_playing:
                self.is_playing[chat_id] = False
            if chat_id in self.queues:
                self.queues[chat_id].clear()
                
            return True
        except Exception as e:
            logger.error(f"Stop error: {e}")
            return False
    
    async def skip_track(self, chat_id: int) -> bool:
        """Şarkıyı atlar"""
        try:
            await self.calls.leave_group_call(chat_id)
            return await self.play_next(chat_id)
        except Exception as e:
            logger.error(f"Skip error: {e}")
            return False
    
    def get_queue(self, chat_id: int) -> List[Track]:
        """Kuyruğu döner"""
        return self.queues.get(chat_id, [])
    
    def get_current_track(self, chat_id: int) -> Optional[Track]:
        """Şu anda çalan şarkıyı döner"""
        return self.current_tracks.get(chat_id)
    
    def is_playing_track(self, chat_id: int) -> bool:
        """Şarkı çalıp çalmadığını kontrol eder"""
        return self.is_playing.get(chat_id, False)
    
    def get_queue_length(self, chat_id: int) -> int:
        """Kuyruk uzunluğunu döner"""
        return len(self.queues.get(chat_id, []))
    
    async def create_playlist(self, chat_id: int, name: str, tracks: List[Track]) -> bool:
        """Playlist oluşturur"""
        try:
            if chat_id not in self.playlists:
                self.playlists[chat_id] = []
            
            # Playlist objesi oluştur
            playlist = {
                'name': name,
                'tracks': tracks,
                'created_at': datetime.now(),
                'total_duration': sum(track.duration for track in tracks)
            }
            
            self.playlists[chat_id].append(playlist)
            return True
        except Exception as e:
            logger.error(f"Create playlist error: {e}")
            return False
    
    async def load_playlist(self, chat_id: int, playlist_name: str) -> bool:
        """Playlist'i yükler"""
        try:
            if chat_id not in self.playlists:
                return False
            
            for playlist in self.playlists[chat_id]:
                if playlist['name'].lower() == playlist_name.lower():
                    # Playlist'i kuyruğa ekle
                    for track in playlist['tracks']:
                        await self.add_to_queue(chat_id, track)
                    return True
            
            return False
        except Exception as e:
            logger.error(f"Load playlist error: {e}")
            return False
    
    def format_duration(self, seconds: int) -> str:
        """Süreyi formatlar"""
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes}:{seconds:02d}"
    
    def get_track_info_text(self, track: Track) -> str:
        """Şarkı bilgilerini metin olarak döner"""
        return (
            f"🎵 **{track.title}**\n"
            f"👤 **Sanatçı:** {track.artist}\n"
            f"⏱️ **Süre:** {self.format_duration(track.duration)}\n"
            f"📺 **Kaynak:** {track.source.title()}"
        )
    
    def get_queue_text(self, chat_id: int, limit: int = 10) -> str:
        """Kuyruk metnini döner"""
        queue = self.get_queue(chat_id)
        
        if not queue:
            return "📭 Kuyruk boş!"
        
        text = "📋 **Müzik Kuyruğu:**\n\n"
        
        for i, track in enumerate(queue[:limit], 1):
            text += f"{i}. **{track.title}** - {track.artist}\n"
        
        if len(queue) > limit:
            text += f"\n... ve {len(queue) - limit} şarkı daha"
        
        return text