import os

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client, handler,
            {
                "command": "leave",
                "category": "dev",
                "aliases": [],
                "description": {"content": "Leave current group", "usage": "none"},
                "exp": 0,
                "devOnly": True,
                "group": True,
            }
        )

    def exec(self, M: MessageClass, contex):
        os.system(f"node bot-commands.js leave")
        self.client.reply_message("✅ Leave command sent to Node.js bot.", M)
