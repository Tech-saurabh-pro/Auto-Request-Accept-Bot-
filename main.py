from pyrogram import Client, filters
from pyrogram.types import ChatJoinRequest, Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.enums import ChatMemberStatus
import asyncio, os, re, json

API_ID = int(os.environ.get("API_ID", 17579837))
API_HASH = os.environ.get("API_HASH", "05417aa5a7d4f7bf46bafac7e25ed69e")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7804127796:AAEKb6U6echHnMMpdtfrVTk4KR4Qcm_sCGE")
OWNER_ID = int(os.environ.get("OWNER_ID", 7224704888))
REQUIRED_CHANNELS = os.environ.get("REQUIRED_CHANNELS", "@channel1 @channel2").split()

app = Client("AutoAcceptBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

USERS_FILE = "users.json"

def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_user(user_id):
    users = load_users()
    if user_id not in users:
        users.append(user_id)
        with open(USERS_FILE, "w") as f:
            json.dump(users, f)

async def is_joined(user_id, client):
    for channel in REQUIRED_CHANNELS:
        try:
            member = await client.get_chat_member(channel, user_id)
            if member.status not in [ChatMemberStatus.MEMBER, ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
                return False
        except:
            return False
    return True

@app.on_message(filters.command("start") & filters.private)
async def start(client, message: Message):
    user = message.from_user
    save_user(user.id)
    buttons = [[InlineKeyboardButton("📢 Join " + ch, url=f"https://t.me/{ch.replace('@', '')}")] for ch in REQUIRED_CHANNELS]
    buttons.append([InlineKeyboardButton("✅ I Have Joined", callback_data="check")])
    msg = await message.reply(
        f"👋 Hello {user.first_name}!\n\n🔐 To use this bot, you must:\n1. Join all update channels\n2. Add this bot to your group/channel\n3. Make sure bot is admin with all permissions\nThen press '✅ I Have Joined'",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    client.storage = getattr(client, "storage", {})
    client.storage[user.id] = msg.id

@app.on_callback_query(filters.regex("check"))
async def check_join(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    chat_id = callback_query.message.chat.id
    if await is_joined(user_id, client):
        try:
            old_msg_id = client.storage.get(user_id)
            if old_msg_id:
                await client.delete_messages(chat_id=chat_id, message_ids=old_msg_id)
        except:
            pass
        menu_buttons = [
            [InlineKeyboardButton("ℹ️ Help", callback_data="help"), InlineKeyboardButton("ℹ️ About", callback_data="about")],
            [InlineKeyboardButton("🤖 Create My Own Clone", callback_data="create_clone")],
            [InlineKeyboardButton("📢 Update Channel", url="https://t.me/yourchannel")]
        ]
        await callback_query.message.reply(
            f"Hello {callback_query.from_user.first_name} ✨\n\n🏡 I am a permanent Auto Request Accept bot.\nMake me *Admin* in your Group or Channel for auto request approval.\n\nTo know more click help button 👇",
            reply_markup=InlineKeyboardMarkup(menu_buttons), parse_mode="markdown")
    else:
        await callback_query.answer("❌ You have not joined all channels.", show_alert=True)

@app.on_chat_join_request()
async def approve(client, join_request: ChatJoinRequest):
    try:
        await join_request.approve()
        print(f"✅ Approved: {join_request.from_user.first_name} in {join_request.chat.title}")
    except Exception as e:
        print(f"❌ Failed to approve: {e}")

@app.on_callback_query(filters.regex("help"))
async def help_callback(client, callback_query: CallbackQuery):
    await callback_query.message.edit(
        "**📝 How to Use This Bot:**\n\n1. 🔗 Join all required update channels\n2. ➕ Add this bot to your group or channel\n3. 🛡️ Make the bot admin with these permissions:\n   - Invite Users via Link\n   - Approve Join Requests\n\n✅ Bot will now automatically accept all pending and future join requests!",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="check")]]), parse_mode="markdown")

@app.on_callback_query(filters.regex("about"))
async def about_callback(client, callback_query: CallbackQuery):
    await callback_query.message.edit(
        "**🤖 Bot Info:**\n\nName: Auto Request Accept Bot\nCreator: @YourUsername\nLanguage: Python + Pyrogram",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="check")]]))

@app.on_callback_query(filters.regex("create_clone"))
async def ask_token(client, callback_query: CallbackQuery):
    await callback_query.message.reply(
        "🤖 *Create Your Own Bot*\n\nSend me your bot token (from @BotFather) or just forward the token message.",
        parse_mode="markdown")

@app.on_message(filters.private & filters.text & filters.incoming)
async def receive_token(client, message: Message):
    save_user(message.from_user.id)
    if re.match(r"\d{9,}:[\w-]{30,}", message.text):
        token = message.text.strip()
        await message.reply("✅ Token received. Your bot will be set up shortly. (Fake deploy - just simulation)")
    elif message.forward_from and message.forward_from.username == "BotFather":
        match = re.search(r"\d{9,}:[\w-]{30,}", message.text)
        if match:
            token = match.group(0)
            await message.reply("✅ Token extracted from message. Bot will be deployed (fake demo)")
        else:
            await message.reply("❌ Could not find token in the message. Please try again.")
    else:
        await message.reply("❌ Invalid token format. Please send a valid token or forward the message from @BotFather.")

@app.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast_cmd(client, message: Message):
    if len(message.command) < 2:
        await message.reply("❌ Use: /broadcast your message here")
        return
    text = message.text.split(None, 1)[1]
    users = load_users()
    success = fail = 0
    for user_id in users:
        try:
            await client.send_message(user_id, text)
            success += 1
        except:
            fail += 1
    await message.reply(f"📤 Broadcast sent!\n✅ Delivered: {success}\n❌ Failed: {fail}")

print("Bot Started...")
app.run()