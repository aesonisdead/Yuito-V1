from libs import Void
from neonize.events import GroupInfoEv, JoinedGroupEv, CallOfferEv

class Event:
    def __init__(self, client: Void):
        self.__client = client

    # --- Existing handlers ---
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

        jid = event.JID
        try:
            if len(event.Leave) > 0:
                user = event.Leave[0].User
                self.__client.send_message(jid, f"👋 @{user} left the chat.")
            elif len(event.Join) > 0:
                user = event.Join[0].User
                self.__client.send_message(jid, f"👤 @{user} joined the chat.")
            elif len(event.Promote) > 0:
                user = event.Promote[0].User
                promoter = event.Sender.User
                self.__client.send_message(
                    jid, f"⬆️ @{user} was *promoted* by @{promoter}."
                )
            elif len(event.Demote) > 0:
                user = event.Demote[0].User
                demoter = event.Sender.User
                self.__client.send_message(
                    jid, f"⬇️ @{user} was *demoted* by @{demoter}."
                )
            elif len(event.Announce) > 0:
                status = "enabled" if event.Announce.IsAnnounce else "disabled"
                self.__client.send_message(
                    jid,
                    f"📢 Announcement mode was *{status}* by @{event.Sender.User}.",
                )
        except Exception as e:
            self.__client.log.error(f"[GroupUpdateError] {e}")

    # --- NEW: Device List Update Handler ---
    def on_device_list_update(self, event):
        """
        Call this method manually when your bot receives a device list update.
        """
        try:
            lid = getattr(event, "LID", None) or getattr(event, "lid", None)
            new_hash = getattr(event, "NewHash", None) or getattr(event, "new_hash", None)
            removed = getattr(event, "Removed", False) or getattr(event, "removed", False)

            action = "removed" if removed else "updated"
            self.__client.log.info(f"[DeviceList] LID {lid} {action}, syncing hash...")

            # Update your bot's local hash (replace with your actual method)
            if hasattr(self.__client, "update_device_hash"):
                self.__client.update_device_hash(lid, new_hash)

        except Exception as e:
            self.__client.log.error(f"[DeviceListSyncError] {e}")
