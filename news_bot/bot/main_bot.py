import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode 

from .routers import start_router, chat_router
from .callbacks import callback_router

API_TOKEN=os.getenv('TOKEN')


async def main() -> None:
    # Dispatcher is a root router
    dp = Dispatcher()

    dp.include_routers(
        start_router,
        callback_router,
        chat_router
    #    form_process
    )
    # Register all the routers from handlers package

    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)
