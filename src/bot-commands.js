import makeWASocket, {
    useSingleFileAuthState,
    fetchLatestBaileysVersion
} from "@adiwajshing/baileys";
import fs from "fs";

const { state, saveState } = useSingleFileAuthState("./auth_info.json");

// Get CLI arguments
const args = process.argv.slice(2);
const command = args[0]; // "join" or "leave"
const param = args[1];   // group link for join

async function main() {
    const { version } = await fetchLatestBaileysVersion();
    const sock = makeWASocket({
        auth: state,
        printQRInTerminal: true,
        version
    });

    sock.ev.on('creds.update', saveState);

    // Wait until connection is ready
    await new Promise(resolve => setTimeout(resolve, 3000));

    if (command === "join") {
        if (!param) return console.log("❌ Please provide a group link.");
        const inviteCode = param.split("/").pop();
        try {
            await sock.groupAcceptInvite(inviteCode);
            console.log("✅ Successfully joined the group!");
        } catch (e) {
            console.log("❌ Failed to join the group:", e.message);
        }
        process.exit(0);
    }

    if (command === "leave") {
        // Use your bot account to leave a group; you'll need the chat ID
        if (!param) return console.log("❌ Please provide the group ID to leave.");
        try {
            await sock.groupLeave(param);
            console.log("👋 Successfully left the group!");
        } catch (e) {
            console.log("❌ Failed to leave the group:", e.message);
        }
        process.exit(0);
    }

    console.log("❌ Unknown command. Use 'join <link>' or 'leave <groupId>'.");
    process.exit(0);
}

main();
