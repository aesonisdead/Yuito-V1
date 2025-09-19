from libs import BaseCommand, MessageClass
from PIL import Image
import os
import time

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "stickertoimage",   # main command
                "aliases": ["toimg"],          # alias(es)
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
            # get sticker from message or quoted
            sticker_msg = None
            if hasattr(M.Message, "stickerMessage"):
                sticker_msg = M.Message.stickerMessage
            elif M.quoted and hasattr(M.quoted, "stickerMessage"):
                sticker_msg = M.quoted.stickerMessage

            if not sticker_msg:
                self.client.reply_message("⚠️ Please reply to a sticker to convert it.", M)
                return

            # fetch bytes from directPath or fileSHA256
            sticker_bytes = None
            if getattr(sticker_msg, "directPath", None):
                sticker_bytes = self.client.get_bytes_from_name_or_url(sticker_msg.directPath)
            elif getattr(sticker_msg, "fileSHA256", None):
                sticker_bytes = self.client.get_bytes_from_name_or_url(sticker_msg.fileSHA256)

            if not sticker_bytes:
                self.client.reply_message("❌ Sticker data missing or invalid.", M)
                return

            # save temp WEBP
            sticker_path = os.path.join(self.temp_dir, f"sticker_{int(time.time())}.webp")
            image_path = os.path.join(self.temp_dir, f"converted_{int(time.time())}.png")
            with open(sticker_path, "wb") as f:
                f.write(sticker_bytes)

            # convert WEBP → PNG
            image = Image.open(sticker_path).convert("RGBA")
            image.save(image_path, format="PNG")

            # send PNG back
            with open(image_path, "rb") as f:
                self.client.send_image(M, f.read(), caption="✅ Sticker converted to image")

            # cleanup
            try:
                os.remove(sticker_path)
                os.remove(image_path)
            except Exception as cleanup_err:
                self.client.log.warning(f"[ToImgCleanup] {cleanup_err}")

        except Exception as e:
            self.client.reply_message(f"❌ ToImgError: {e}", M)
            self.client.log.error(f"[ToImgError] {e}")
