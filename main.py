import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

WEBHOOK_PATH = "/webhook"
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "supersecret")
BASE_WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # например: https://your-app-name.onrender.com

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher(storage=MemoryStorage())

@dp.message()
async def handle_message(message: types.Message):
    if message.text and message.chat.type in ["channel", "supergroup"]:
        await message.answer("Бот работает! 🟢")

async def on_startup(app: web.Application):
    webhook_url = BASE_WEBHOOK_URL + WEBHOOK_PATH
    await bot.set_webhook(webhook_url, secret_token=WEBHOOK_SECRET)

app = web.Application()
SimpleRequestHandler(dispatcher=dp, bot=bot, secret_token=WEBHOOK_SECRET).register(app, path=WEBHOOK_PATH)
app.on_startup.append(on_startup)

if __name__ == "__main__":
    web.run_app(app, port=10000)  # Render требует явно указывать порт
