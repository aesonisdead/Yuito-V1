from libs import BaseCommand, MessageClass
from neonize.utils import ParticipantChange

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "remove",
                "category": "group",
                "description": {
                    "content": "Remove user(s) from the group.",
                    "usage": "<@mention> | <quote>",
                },
                "admin": True,
                "group": True,
                "exp": 2,
            },
        )

    def exec(self, M: MessageClass, _):
        try:
            targets = M.mentioned or ([M.quoted_user] if M.quoted_user else [])
            if not targets:
                return self.client.reply_message(
                    "❌ Please *mention or quote* a user to remove.", M
                )

            # Normalize JIDs
            target_jids = [self.client.build_jid(str(u.number).lstrip("+")) for u in targets]

            # Use metadata from the message object
            participants = [p.jid for p in (M.group_metadata.participants or [])]

            valid_targets = [jid for jid in target_jids if jid in participants]

            if not valid_targets:
                return self.client.reply_message("⚠️ User not found in this group.", M)

            self.client.update_group_participants(
                M.gcjid,
                valid_targets,
                ParticipantChange.REMOVE,
            )

            self.client.reply_message("✅ User(s) removed from the group.", M)

        except Exception as e:
            self.client.reply_message("❗ Failed to remove user(s).", M)
            self.client.log.error(f"[remove] {e}")
