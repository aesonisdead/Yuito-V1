from libs import Void
from utils import DynamicConfig
from neonize.events import MessageEv


class MessageClass:
    def __init__(self, client: Void, message: MessageEv):
        self.__client = client
        self.__M = message

        self.Info = message.Info
        self.Message = message.Message
        self.content = client.extract_text(self.Message)
        self.gcjid = self.Info.MessageSource.Chat
        self.chat = "group" if self.Info.MessageSource.IsGroup else "dm"

        sender_number = self.Info.MessageSource.Sender.User
        self.sender = DynamicConfig(
            {
                "number": sender_number,
                "username": client.contact.get_contact(
                    client.build_jid(sender_number)
                ).PushName,
            }
        )

        self.urls = []
        self.numbers = []
        self.quoted = None
        self.quoted_user = None
        self.mentioned = []

        if self.Message.HasField("extendedTextMessage"):
            ctx_info = self.Message.extendedTextMessage.contextInfo

            if ctx_info.HasField("quotedMessage"):
                self.quoted = ctx_info.quotedMessage

                if ctx_info.HasField("participant"):
                    quoted_number = ctx_info.participant.split("@")[0]
                    self.quoted_user = DynamicConfig(
                        {
                            "number": quoted_number,
                            "username": client.contact.get_contact(
                                client.build_jid(quoted_number)
                            ).PushName,
                        }
                    )

            for jid in ctx_info.mentionedJID:
                number = jid.split("@")[0]
                self.mentioned.append(
                    DynamicConfig(
                        {
                            "number": number,
                            "username": client.contact.get_contact(
                                client.build_jid(number)
                            ).PushName,
                        }
                    )
                )

    def build(self):
        self.urls = self.__client.utils.get_urls(self.content)
        self.numbers = self.__client.utils.extract_numbers(self.content)

        if self.chat == "group":
            self.group = self.__client.get_group_info(self.gcjid)
            self.isAdminMessage = (
                self.sender.number
                in self.__client.filter_admin_users(self.group.Participants)
            )

        return self

    def raw(self):
        return self.__M
