import os

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client, handler,
            {
                "command": "join",
                "category": "dev",
                "aliases": [],
                "description": {"content": "Join a group via link", "usage": "<group_link>"},
                "exp": 0,
                "devOnly": True,
            }
        )

    def exec(self, M: MessageClass, contex):
        link = contex.text.strip()
        if not link:
            return self.client.reply_message("⚠️ Please provide a group invite link.", M)

        # Call the Node.js helper
        os.system(f"node bot-commands.js join {link}")
        self.client.reply_message("✅ Join command sent to Node.js bot.", M)
