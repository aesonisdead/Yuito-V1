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

        chat_jid = M.gcjid  # use gcjid instead of chat_id

        self.client.send_message(
            chat_jid,
            f"🎯 Hey *@{M.sender.number}*! Your current EXP is: *{exp}*.",
            mentions=[M.sender.jid],
        )
