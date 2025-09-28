from libs import BaseCommand, MessageClass


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "leave",
                "category": "dev",
                "aliases": ["l"],
                "description": {
                    "content": "Make the bot leave the current group (devs only).",
                    "usage": "none",
                },
                "exp": 0,
                "devOnly": True,
                "group": True,
            },
        )

    def exec(self, M: MessageClass, contex):
        try:
            self.client.leave_group(M.chat_id)  # replace with your actual method
            self.client.reply_message("👋 Successfully left the group.", M)
        except Exception as e:
            self.client.reply_message(f"❌ Failed to leave the group: {str(e)}", M)
