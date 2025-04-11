import os
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
BASE_WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # пример: https://yourproject.onrender.com

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher(storage=MemoryStorage())

@dp.channel_post()
async def handle_channel_post(message: types.Message):
    text = message.text or message.caption
    if not text:
        return

    # История сохранённых текстов
    history_file = "posted_texts.txt"
    if not os.path.exists(history_file):
        open(history_file, "w").close()

    with open(history_file, "r+", encoding="utf-8") as f:
        past_posts = f.read().splitlines()
        if text in past_posts:
            await bot.send_message(
                chat_id=message.chat.id,
                text="⚠️ Этот пост уже публиковался ранее.",
                reply_to_message_id=message.message_id
            )
        else:
            f.write(text + "\n")

async def on_startup(app: web.Application):
    webhook_url = BASE_WEBHOOK_URL + WEBHOOK_PATH
    await bot.set_webhook(webhook_url, secret_token=WEBHOOK_SECRET)

app = web.Application()
SimpleRequestHandler(dispatcher=dp, bot=bot, secret_token=WEBHOOK_SECRET).register(app, path=WEBHOOK_PATH)
app.on_startup.append(on_startup)

if __name__ == "__main__":
    web.run_app(app, port=10000)
