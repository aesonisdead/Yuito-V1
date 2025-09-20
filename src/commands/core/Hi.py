from libs import BaseCommand, MessageClass

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "hi",
                "category": "core",
                "description": {"content": "Say hello to the bot"},
                "exp": 1,
            },
        )

    def exec(self, M: MessageClass, _):
        # Get user info
        user_number = M.sender.number
        user_jid = M.sender.jid  # full WhatsApp ID
        exp = getattr(M.sender, "exp", 0) or 0

        # Build the message text
        text = f"🎯 Hey *@{user_number}*! Your current EXP is: *{exp}*."

        # Send message and tag user
        self.client.send_message(
            M.gcjid if M.chat == "group" else user_jid,
            text,
            mentions=[user_jid]  # this tags the user in the message
        )
