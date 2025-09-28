import makeWASocket, {
    DisconnectReason,
    useSingleFileAuthState,
    fetchLatestBaileysVersion
} from "@adiwajshing/baileys";
import fs from "fs";

const { state, saveState } = useSingleFileAuthState("./auth_info.json");

async function startBot() {
    const { version, isLatest } = await fetchLatestBaileysVersion();
    const sock = makeWASocket({
        auth: state,
        printQRInTerminal: true,
        version
    });

    sock.ev.on('creds.update', saveState);

    // Listen for commands
    sock.ev.on('messages.upsert', async m => {
        if (!m.messages) return;
        const msg = m.messages[0];
        if (!msg.message || !msg.key.fromMe) return;

        const text = msg.message.conversation || "";
        const chatId = msg.key.remoteJid;

        if (text.startsWith("#join ")) {
            const link = text.split(" ")[1];
            const inviteCode = link.split("/").pop();
            try {
                await sock.groupAcceptInvite(inviteCode);
                await sock.sendMessage(chatId, { text: "✅ Joined the group!" });
            } catch (e) {
                await sock.sendMessage(chatId, { text: `❌ Failed to join: ${e.message}` });
            }
        }

        if (text.startsWith("#leave")) {
            try {
                await sock.groupLeave(chatId);
                // No need to send message to same chat; bot already left
                console.log(`Left group ${chatId}`);
            } catch (e) {
                await sock.sendMessage(chatId, { text: `❌ Failed to leave: ${e.message}` });
            }
        }
    });
}

startBot();
