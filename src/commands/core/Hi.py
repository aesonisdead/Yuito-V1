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

        jid = str(M.sender.jid)  # full WhatsApp ID (e.g., 212605158422@c.us)
        phone = M.sender.number  # clean phone number without @c.us

        self.client.send_message(
            M.chat_id,  # reply in the same chat
            f"🎯 Hey *@{phone}*! Your current EXP is: *{exp}*.",
            mentions=[jid],
        )
