from libs import BaseCommand, MessageClass

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "join",
                "category": "dev",
                "aliases": ["j"],
                "description": {
                    "content": "Join a WhatsApp group via invite link (devs only).",
                    "usage": "<group_link>",
                },
                "exp": 0,
                "devOnly": True,
            },
        )

    def exec(self, M: MessageClass, contex):
        link = contex.text.strip()
        if not link:
            return self.client.reply_message("⚠️ Please provide a group invite link.", M)

        # Extract the invite code from the link
        try:
            invite_code = link.split("/")[-1]
            self.client.groupAcceptInvite(invite_code)  # actual method to join
            self.client.reply_message(f"✅ Successfully joined the group.", M)
        except Exception as e:
            self.client.reply_message(f"❌ Failed to join the group: {str(e)}", M)
