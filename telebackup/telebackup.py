import yaml
import os
import asyncio
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.types import MessageMediaWebPage
from telethon.errors import MediaCaptionTooLongError, FloodWaitError

# 📁 Define Config Directory & File
CONFIG_DIR = os.path.expanduser("~/.config/telebackup")
CONFIG_PATH = os.path.join(CONFIG_DIR, "provider-config.yaml")

# 🛠 Load YAML Config
def load_config():
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(f"❌ Config file not found: {CONFIG_PATH}")
    
    with open(CONFIG_PATH, 'r') as f:
        config = yaml.safe_load(f)

    # Flatten values (all should be single-item lists)
    for key, value in config.items():
        if not value or not isinstance(value, list) or not value[0]:
            raise ValueError(f"⚠️ Please configure your '{key}' in {CONFIG_PATH} before running the script.")
        config[key] = value[0] if len(value) == 1 else value
    
    return config

# 📦 Load & Save Sent Message IDs
def load_sent_ids(file_path):
    if not os.path.exists(file_path):
        return set()
    with open(file_path, 'r') as f:
        return set(line.strip() for line in f if line.strip())

def save_sent_id(file_path, msg_url):
    with open(file_path, 'a') as f:
        f.write(f"{msg_url}\n")

# 🚪 Join Telegram Chat
async def join_chat_if_needed(client, invite_link):
    try:
        if '/+' in invite_link:
            await client(ImportChatInviteRequest(invite_link.split('+')[1]))
        elif '/joinchat/' in invite_link:
            await client(ImportChatInviteRequest(invite_link.split('/joinchat/')[1]))
    except Exception as e:
        print(f"⚠️ Join failed or already a member: {invite_link} — {e}")

# 🚀 Main Task
async def main():
    try:
        config = load_config()
    except Exception as e:
        print(e)
        return

    # Create ~/.config/telebackup if it doesn't exist
    os.makedirs(CONFIG_DIR, exist_ok=True)

    # Extract config
    api_id = config['api_id']
    api_hash = config['api_hash']
    session_name = os.path.join(CONFIG_DIR, config['session_name'])  # path to session
    source_channel = config['source_channel']
    destination_channel = config['destination_channel']
    sent_ids_file = os.path.join(CONFIG_DIR, config['sent_ids_file'])  # path to sent_ids.txt

    sent_ids = load_sent_ids(sent_ids_file)

    async with TelegramClient(session_name, api_id, api_hash) as client:
        await join_chat_if_needed(client, destination_channel)
        dest = await client.get_entity(destination_channel)

        for source_link in source_channel:
            print(f"\n🔄 Processing source: {source_link}")
            await join_chat_if_needed(client, source_link)

            try:
                source = await client.get_entity(source_link)
                source_username = source.username or f"c{abs(source.id)}"
            except Exception as e:
                print(f"❌ Failed to get entity for {source_link}: {e}")
                continue

            async for msg in client.iter_messages(source, reverse=True):
                msg_url = f"https://t.me/{source_username}/{msg.id}"

                if msg_url in sent_ids:
                    print(f"⏭️ Skipping already sent: {msg_url}")
                    continue

                try:
                    if not msg.text and not msg.media:
                        print(f"⚠️ Skipped empty message: {msg_url}")
                        continue

                    if isinstance(msg.media, MessageMediaWebPage):
                        await client.send_message(dest, msg.text or msg.message)
                    elif msg.media:
                        await client.send_file(dest, msg.media, caption=msg.text or msg.message)
                    else:
                        await client.send_message(dest, msg.text or msg.message)

                    save_sent_id(sent_ids_file, msg_url)
                    print(f"✅ Copied: {msg_url}")

                except MediaCaptionTooLongError:
                    print(f"⚠️ Caption too long for message: {msg_url}, skipping.")
                    continue  # Skip this message and continue

                except FloodWaitError as e:
                    print(f"🕒 FloodWaitError: Sleeping for {e.seconds} seconds...")
                    await asyncio.sleep(e.seconds)

                except Exception as e:
                    print(f"⚠️ Error copying {msg_url}: {e}")

# 🧠 Start the Script
def run():
    asyncio.run(main())

if __name__ == "__main__":
    run()
