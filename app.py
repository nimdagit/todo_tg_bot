import os
import asyncio
import logging

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from config import BOT_TOKEN
from handlers.commands import router as cmd_router


# --- Настройки, специфичные для деплоя ---
# WEBHOOK_HOST — это твой публичный адрес на Render, например:
# https://my-todo-bot.onrender.com
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# Render сам подставляет порт через переменную окружения PORT
WEB_SERVER_HOST = "0.0.0.0"
WEB_SERVER_PORT = int(os.getenv("PORT", 8080))


bot = Bot(BOT_TOKEN)
dp = Dispatcher()

dp.include_router(cmd_router)


bot_cmds = [
    BotCommand(command='start', description='wake up the bot and registration'),
    BotCommand(command='add', description='add task'),
    BotCommand(command='task_list', description='show task list'),
    BotCommand(command='help', description='help'),
]


async def on_startup(bot: Bot) -> None:
    # Сообщаем Telegram, куда слать апдейты
    await bot.set_webhook(WEBHOOK_URL)
    await bot.set_my_commands(bot_cmds)


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    dp.startup.register(on_startup)

    app = web.Application()
    # Подключаем обработчик, который будет принимать POST-запросы от Telegram
    webhook_requests_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)

    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


if __name__ == "__main__":
    main()