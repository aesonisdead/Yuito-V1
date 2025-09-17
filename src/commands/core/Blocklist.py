from libs import BaseCommand, MessageClass


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "blocklist",
                "category": "core",
                "description": {
                    "content": "Displays all users blocked by the bot."
                },
                "aliases": ["blist", "blocked"],
                "exp": 0,
            },
        )
        # ✅ Add your dev numbers here (without @s.whatsapp.net)
        self.dev_numbers = ["212605158422"]

    def exec(self, M: MessageClass, _):
        # ✅ Dev-only check
        if M.sender.number not in self.dev_numbers:
            return self.client.reply_message(
                "⛔ This command is restricted to bot developers only.", M
            )

        try:
            blocklist_response = self.client.get_blocklist()

            if (
                not hasattr(blocklist_response, "JIDs")
                or len(blocklist_response.JIDs) == 0
            ):
                return self.client.reply_message(
                    "✅ No users are currently blocked.", M
                )

            lines = []
            for i, jid in enumerate(blocklist_response.JIDs, start=1):
                if hasattr(jid, "User") and jid.User:
                    lines.append(f"{i}. wa.me/{jid.User}")

            if not lines:
                return self.client.reply_message(
                    "✅ No users are currently blocked.", M
                )

            message = f"🚫 *Blocked Users ({len(lines)})*\n\n" + "\n".join(
                lines
            )

            self.client.reply_message(message, M)

        except Exception as e:
            self.client.reply_message("⚠️ Failed to retrieve blocklist.", M)
            self.client.log.error(f"[blocklist] Error: {e}")
