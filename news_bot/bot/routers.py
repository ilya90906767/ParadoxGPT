from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from aiogram import Router
from aiogram import types, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile, URLInputFile
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from django.conf import settings

import os
import random
import shutil
import base64
import io


from users.models import UserProfile, Persona
from .db_methods import get_user_from_db
from .gpt import send_to_gpt, generate_one
from .keyboard import start, gpt_dialog
from .callbacks import Chat

from aiogram import types, Bot
import os
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode 
API_TOKEN=os.getenv('TOKEN')
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


start_router = Router()
chat_router = Router()

@start_router.message(StateFilter(Chat.default))
@start_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    current_user_id = message.from_user.id
    try: 
        user = await get_user_from_db(current_user_id)
        text = "Добро пожаловать в Бот Историческая Парадоксия"
        await message.answer(
            text=f"{text}",
            reply_markup=start(message),
        )
    except ObjectDoesNotExist:
        user = UserProfile(telegram_id=current_user_id)
        current_persona = await sync_to_async(Persona.objects.get)(name="Стандартный")  # Get the persona asynchronously
        user.current_persona = current_persona  # Assign the persona
        await sync_to_async(user.save)()
        text = "Добро пожаловать в Бот Историческая Парадоксия"
        await message.answer(
            text=f"{text}",
            reply_markup=start(message)
        )

@chat_router.message(StateFilter(Chat.isChat))
async def handle_chat_message(message: types.Message, state: FSMContext):
    current_user_id = message.from_user.id
    user_message = message.text
    await bot.send_chat_action(message.chat.id, action='typing')
    gpt_response = await send_to_gpt(user_message,user_id=current_user_id)
    await message.answer(
            text=f"{gpt_response}",
            reply_markup=gpt_dialog(message),
            parse_mode='Markdown'
        )

@chat_router.message(StateFilter(Chat.genPhoto))
async def handle_photo_prompt(message: types.Message, state: FSMContext):
    current_user_id = message.from_user.id
    photo_prompt = message.text
    await bot.send_chat_action(message.chat.id, action='upload_photo')
    rand_int = random.randint(1, 10000)
    image_response = await generate_one(prompt=photo_prompt, telegram_id=current_user_id, name=rand_int)
    image = URLInputFile(str(image_response),filename="python-logo.png")
    await message.answer(
        text="Вот фото по вашему запросу:",

    )

    await message.answer_photo(
        photo=image
    )