# 🤖 Auto Request Accept Telegram Bot

This is a free, open-source Telegram bot that automatically accepts **group or channel join requests**.  
It also includes features like:
- ✅ Force Join (mandatory channel join before using)
- 🔄 Bot Clone Generator (users can create their own auto-accept bot)
- 📢 Broadcast System
- 🧠 Help/Instructions menu

---

## 🚀 Features

- 🔓 Auto-accepts all pending & future join requests (group/channel)
- 🔐 Force Join required channels before allowing access
- 🔄 "Create My Own Bot" feature (via token or BotFather message)
- 📢 Admins can broadcast messages to all bot users
- 📋 Clean and simple inline menu

---

## 🧪 Demo

Try the bot: [@YourBotUsername](https://t.me/YourBotUsername)

---

## ⚙️ Deploy to Render (Free Hosting)

### 🧷 1. Fork or Clone This Repo

### 🧷 2. Create Account on [Render](https://render.com)

- Click **“New Web Service”**
- Connect to GitHub
- Select this repo

### 🧷 3. Set Render Settings:

| Field | Value |
|-------|-------|
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `python main.py` |

---

### 🔐 Environment Variables (Render → Environment tab)

| Key | Description |
|-----|-------------|
| `API_ID` | Get from https://my.telegram.org |
| `API_HASH` | Get from https://my.telegram.org |
| `BOT_TOKEN` | Get from @BotFather |
| `OWNER_ID` | Your Telegram numeric ID |
| `REQUIRED_CHANNELS` | Space-separated list of required channels (e.g., `@channel1 @channel2`) |

---

## 🧠 How to Use the Bot

1. **Join required channels**
2. **Add bot to your group or channel**
3. **Make bot admin with "Add Users" + "Approve Join Requests" permissions**
4. ✅ That's it! Bot will auto-accept all join requests

---

## 📦 Create Your Own Bot (Clone)

Users can:
- 🔐 Send their own bot token
- 📨 Or forward the @BotFather message

They’ll get instructions to deploy it themselves.

---

## 📤 Broadcast (Admin Only)

Use `/broadcast your message here` to send message to all users who started the bot.

---

## 👨‍💻 Credits

- Dev: [@YourUsername](https://t.me/YourUsername)
- Built with: [Pyrogram](https://docs.pyrogram.org/)

---

## 🛡 License

This bot is open-source. Feel free to clone, customize, or contribute.