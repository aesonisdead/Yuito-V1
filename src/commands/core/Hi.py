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
        user = self.client.db.get_user_by_number(M.sender.number)
        exp = getattr(user, "exp", 0)

        # ✅ Correct WhatsApp mention format
        # If M.sender.number = 212605158422
        # Then jid = "212605158422@c.us"
        jid = f"{M.sender.number}@c.us"

        self.client.reply_message(
            f"🎯 Hey *@{jid}*! Your current EXP is: *{exp}*.", M
    )
