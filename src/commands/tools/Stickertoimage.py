from libs import BaseCommand, MessageClass
from PIL import Image
import os
import io
import base64
import time

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "toimg",
                "category": "tools",
                "description": {"content": "Convert a sticker to an image"},
                "exp": 1
            },
        )
        self.temp_dir = "./temp"
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

    def exec(self, M: MessageClass, _):
        try:
            # Check sticker in current message or quoted
            sticker_msg = None
            if hasattr(M.Message, "stickerMessage"):
                sticker_msg = M.Message.stickerMessage
            elif M.quoted and hasattr(M.quoted, "stickerMessage"):
                sticker_msg = M.quoted.stickerMessage

            if not sticker_msg:
                self.client.reply_message("⚠️ Please reply to a sticker to convert it.", M)
                return

            # Try to get bytes from pngThumbnail (base64)
            sticker_bytes = None
            if hasattr(sticker_msg, "pngThumbnail") and sticker_msg.pngThumbnail:
                sticker_bytes = base64.b64decode(sticker_msg.pngThumbnail)
            else:
                self.client.reply_message("❌ Sticker data missing or invalid.", M)
                return

            # Save temp WEBP
            sticker_path = os.path.join(self.temp_dir, f"sticker_{int(time.time())}.webp")
            image_path = os.path.join(self.temp_dir, f"converted_{int(time.time())}.png")
            with open(sticker_path, "wb") as f:
                f.write(sticker_bytes)

            # Convert WEBP → PNG
            image = Image.open(sticker_path).convert("RGBA")
            image.save(image_path, format="PNG")

            # Send converted image
            with open(image_path, "rb") as f:
                self.client.send_image(M, f.read(), caption="✅ Sticker converted to image")

            # Cleanup temp files
            try:
                os.remove(sticker_path)
                os.remove(image_path)
            except Exception as cleanup_err:
                self.client.log.warning(f"[ToImgCleanup] {cleanup_err}")

        except Exception as e:
            self.client.reply_message(f"❌ ToImgError: {e}", M)
            self.client.log.error(f"[ToImgError] {e}")
