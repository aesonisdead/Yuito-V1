import time, random
from libs import BaseCommand, MessageClass


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "broadcast",
                "aliases": ["bc"],
                "category": "dev",
                "description": {
                    "content": "Broadcast a message to all groups (with safe delay).",
                    "usage": "<message>",
                },
                "exp": 0,
                "devOnly": True,
            },
        )

    def exec(self, M: MessageClass, contex):
        if not contex.text:
            return self.client.reply_message(
                "*⚠️ Please provide a message to broadcast.*", M
            )

        text = contex.text.strip()
        sent = 0
        failed = 0

        try:
            all_chats = self.client.get_joined_groups()
            total = len(all_chats)

            self.client.reply_message(
                f"📢 Starting broadcast to *{total}* groups...\n"
                f"⏳ This will take some time (2–3 sec delay each).",
                M,
            )

            for chat in all_chats:
                try:
                    self.client.send_message(chat.JID, f"📢 *Broadcast:*\n{text}")
                    sent += 1
                    time.sleep(random.uniform(2.0, 3.5))  # safe delay
                except Exception as e:
                    failed += 1
                    self.client.log.error(f"[BroadcastError] {chat.JID} → {e}")
                    time.sleep(1.5)

            self.client.reply_message(
                f"✅ Broadcast finished.\n"
                f"📨 Sent: *{sent}*\n"
                f"❌ Failed: *{failed}*",
                M,
            )

        except Exception as e:
            self.client.reply_message("❌ Broadcast failed completely.", M)
            self.client.log.error(f"[BroadcastFatalError] {e}")

