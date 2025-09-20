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

        # Use M.sender.jid for correct mentions
        self.client.send_message(
            M.chat_id,
            f"🎯 Hey *@{M.sender.number}*! Your current EXP is: *{exp}*.",
            mentions=[M.sender.jid],
        )
