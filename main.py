
import os
import json
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "supersecret")
BASE_WEBHOOK_URL = os.getenv("WEBHOOK_URL")

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

HISTORY_FILE = "history.json"

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_history(data):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@dp.channel_post()
async def handle_channel_post(message: types.Message):
    if not message.text:
        return

    history = load_history()
    text = message.text.strip()

    if text in history:
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"⚠️ Похоже, это уже публиковалось ранее!",
            reply_to_message_id=message.message_id
        )
    else:
        history.append(text)
        save_history(history)
        print("✅ Новый пост сохранён в истории")

async def on_startup(app: web.Application):
    webhook_url = BASE_WEBHOOK_URL + WEBHOOK_PATH
    await bot.set_webhook(webhook_url, secret_token=WEBHOOK_SECRET)

app = web.Application()
SimpleRequestHandler(dispatcher=dp, bot=bot, secret_token=WEBHOOK_SECRET).register(app, path=WEBHOOK_PATH)
app.on_startup.append(on_startup)

if __name__ == "__main__":
    web.run_app(app, port=10000)
