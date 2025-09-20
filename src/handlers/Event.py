from libs import Void
from neonize.events import (
    GroupInfoEv,
    JoinedGroupEv,
    CallOfferEv,
)


class Event:
    def __init__(self, client: Void):
        self.__client = client

    def on_call(self, event: CallOfferEv):
        user_id = event.basicCallMeta.callCreator.User
        jid = self.__client.build_jid(user_id)

        self.__client.db.update_user_ban(user_id, True, "Called the bot!")
        self.__client.send_message(
            jid,
            "🚫 You have been *blocked* for calling the bot.\nPlease refrain from calling bots in the future.",
        )
        self.__client.update_blocklist(jid, self.__client.BlocklistAction.BLOCK)

    def on_joined(self, event: JoinedGroupEv):
        self.__client.send_message(
            event.GroupInfo.JID,
            f"Thanks for adding me in {event.GroupInfo.GroupName.Name}!!\nUse {self.__client.config.prefix}help to see the commands",
        )

    def on_groupevent(self, event: GroupInfoEv):
    group = self.__client.db.get_group_by_number(event.JID.User)
      if not group.events:
        return

    jid = str(event.JID)

      try:
          if len(event.Leave) > 0:
            user = str(event.Leave[0].User)
            phone = user.replace("@c.us", "")
            self.__client.send_message(
                jid,
                f"👋 @{phone} left the chat.",
                mentions=[user]
            )

          elif len(event.Join) > 0:
            user = str(event.Join[0].User)
            phone = user.replace("@c.us", "")
            self.__client.send_message(
                jid,
                f"👤 @{phone} joined the chat.",
                mentions=[user]
            )

          elif len(event.Promote) > 0:
            user = str(event.Promote[0].User)
            promoter = str(event.Sender.User)
            phone = user.replace("@c.us", "")
            promoter_phone = promoter.replace("@c.us", "")
            self.__client.send_message(
                jid,
                f"⬆️ @{phone} was *promoted* by @{promoter_phone}.",
                mentions=[user, promoter]
            )

          elif len(event.Demote) > 0:
            user = str(event.Demote[0].User)
            demoter = str(event.Sender.User)
            phone = user.replace("@c.us", "")
            demoter_phone = demoter.replace("@c.us", "")
            self.__client.send_message(
                jid,
                f"⬇️ @{phone} was *demoted* by @{demoter_phone}.",
                mentions=[user, demoter]
            )

          elif len(event.Announce) > 0:
            status = "enabled" if event.Announce.IsAnnounce else "disabled"
            sender = str(event.Sender.User)
            sender_phone = sender.replace("@c.us", "")
            self.__client.send_message(
                jid,
                f"📢 Announcement mode was *{status}* by @{sender_phone}.",
                mentions=[sender]
            )

    except Exception as e:
        self.__client.log.error(f"[GroupUpdateError] {e}")
