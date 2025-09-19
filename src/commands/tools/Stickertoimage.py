from libs import BaseCommand, MessageClass
import pprint

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "toimgdebug",
                "category": "tools",
                "description": {"content": "Debug sticker message attributes"},
                "exp": 0
            },
        )

    def exec(self, M: MessageClass, _):
        try:
            sticker_msg = None
            if hasattr(M.Message, "stickerMessage"):
                sticker_msg = M.Message.stickerMessage
            elif M.quoted and hasattr(M.quoted, "stickerMessage"):
                sticker_msg = M.quoted.stickerMessage

            if not sticker_msg:
                self.client.reply_message("⚠️ Please reply to a sticker to debug it.", M)
                return

            # Collect attributes
            attrs = dir(sticker_msg)
            try:
                as_dict = sticker_msg.__dict__
            except:
                as_dict = str(sticker_msg)

            debug_text = "🔎 Sticker Debug:\n\n"
            debug_text += f"Attributes: {attrs}\n\n"
            debug_text += f"Dict/Content:\n{pprint.pformat(as_dict, indent=2, width=80)}"

            # Send back in chunks if too long
            if len(debug_text) > 4000:  # WhatsApp message limit
                parts = [debug_text[i:i+4000] for i in range(0, len(debug_text), 4000)]
                for p in parts:
                    self.client.reply_message(p, M)
            else:
                self.client.reply_message(debug_text, M)

        except Exception as e:
            self.client.reply_message(f"❌ DebugError: {e}", M)
            self.client.log.error(f"[StickerDebugError] {e}")
