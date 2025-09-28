from libs import BaseCommand, MessageClass

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "leave",
                "category": "dev",
                "aliases": [],
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
            group_id = getattr(M, "chat", None) or getattr(M, "chat_id", None)
            if not group_id:
                return self.client.reply_message("❌ Could not detect this group.", M)

            self.client.groupLeave(group_id)  # actual method to leave
            self.client.reply_message("👋 Successfully left the group.", M)
        except Exception as e:
            self.client.reply_message(f"❌ Failed to leave the group: {str(e)}", M)
