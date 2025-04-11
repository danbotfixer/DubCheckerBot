import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
from aiohttp import web

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

@dp.message()
async def handle_message(message: Message):
    if message.text:
        await message.answer("✅ Бот работает!")

# HTTP-сервер для Render
async def handle(request):
    return web.Response(text="Bot is running.")

async def start_webserver():
    app = web.Application()
    app.add_routes([web.get("/", handle)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(os.getenv("PORT", 8080)))
    await site.start()

async def main():
    await start_webserver()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
