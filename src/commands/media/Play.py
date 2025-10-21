from libs import BaseCommand, MessageClass
import yt_dlp
import os


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "play",
                "category": "media",
                "description": {
                    "content": "Search and download audio by query from YouTube.",
                    "usage": "<search>",
                },
                "exp": 3,
            },
        )

    def exec(self, M: MessageClass, contex):
        if not contex.text:
            return self.client.reply_message(
                "❌ Please provide a song name or *search query*.", M
            )

        query = contex.text.strip()
        self.client.reply_message(f"🔍 *Searching for:* {query}...", M)

        try:
            os.makedirs("downloads", exist_ok=True)
            random_filename = self.client.utils.random_alpha_string(10)
            temp_outtmpl = os.path.join("downloads", random_filename + ".%(ext)s")

            # --- Optimized yt-dlp options ---
            ydl_opts = {
                "format": "bestaudio[ext=m4a]/bestaudio/best",
                "noplaylist": True,
                "quiet": True,
                "default_search": "ytsearch1",
                "outtmpl": temp_outtmpl,
                "geo_bypass": True,
                "http_headers": {
                    "User-Agent": "com.google.android.youtube/19.17.34 (Linux; U; Android 11) gzip",
                    "Accept-Language": "en-US,en;q=0.9",
                },
                "concurrent_fragment_downloads": 10,
                "http_chunk_size": 1048576,  # 1MB per chunk
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(query, download=True)

            file_path = os.path.join("downloads", f"{random_filename}.mp3")

            if not os.path.exists(file_path):
                return self.client.reply_message(
                    "⚠️ Downloaded file not found. Please try again.", M
                )

            # 100 MB file size check
            if os.path.getsize(file_path) > 100 * 1024 * 1024:
                os.remove(file_path)
                return self.client.reply_message(
                    "⚠️ File size exceeds the 100MB limit.", M
                )

            # Send the audio file
            self.client.send_audio(M.gcjid, file=file_path, quoted=M)
            os.remove(file_path)

        except Exception as e:
            self.client.reply_message(
                "⚠️ Something went wrong while fetching the audio.", M
            )
            self.client.log.error(f"[PlayCommandError] {e}")
