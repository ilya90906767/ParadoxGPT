from aiogram import types, Bot
from aiogram import Router
from aiogram import F
from aiogram.types import Message, InputFile, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from django.conf import settings

import random

from .keyboard import CD, CP, start, chose_persona
from .db_methods import update_user_fio, update_user_DateBirth, update_user_DateDeath, update_user_Epigraph, update_user_Photos, generate_short, get_all_personas
from .db_methods import get_persona_and_change
callback_router = Router()

import os
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode 
API_TOKEN=os.getenv('TOKEN')
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

class Chat(StatesGroup):
    isChat = State()
    default = State()
    genPhoto = State()

@callback_router.callback_query(CD.filter(F.cb_text == "chat"))
async def chat_start(query: types.CallbackQuery,state: FSMContext):
    await query.message.delete()
    await query.message.answer("Я вас слушаю...") #Надо будет заменить на уникальное сообщение
    await state.set_state(Chat.isChat)

@callback_router.callback_query(CD.filter(F.cb_text == "end_chat"))
async def cancel_chat(query: types.CallbackQuery, state: FSMContext):
    await state.set_state(Chat.default)
    await query.message.answer(
            text=f"Чат отменен. Вы можете начать заново.",
            reply_markup=start(query.message),
        )

@callback_router.callback_query(CD.filter(F.cb_text == "photo"))
async def start_photo(query: types.CallbackQuery, state: FSMContext):
    await query.message.delete()
    await query.message.answer("Жду от вас сообщение, по которому сгенерируется фото") 
    await state.set_state(Chat.genPhoto)

@callback_router.callback_query(CD.filter(F.cb_text == "personas"))
async def start_photo(query: types.CallbackQuery, state: FSMContext):
    await query.message.delete()
    all_personas = await get_all_personas()
    await query.message.answer(
        text = "Выберайте персону с которой хотите пообщаться",
        reply_markup=chose_persona(all_personas)
        )

@callback_router.callback_query(CP.filter())
async def start_photo(query: types.CallbackQuery, state: FSMContext, callback_data: dict):
    user_id = query.from_user.id
    await query.message.delete()
    persona_name = callback_data.persona
    await get_persona_and_change(user_id,persona_name)
    await query.message.answer(
        text = f"Вы успешно выбрали {persona_name}. Теперь можете начать чат",
        reply_markup=start(query.message)
        )  



# class Form(StatesGroup):
#     waiting_for_fio = State()
#     waiting_for_DateBirth = State()
#     waiting_for_DateDeath = State()
#     waiting_for_Epigraph = State()
#     waiting_for_Photo = State()



# @callback_router.callback_query(CD.filter(F.cb_text == "FIO"))
# async def FIO_callback(query: types.CallbackQuery,state: FSMContext):
#     await query.message.delete()
#     await query.message.answer("Пожалуйста, введите ФИО:")
#     await state.set_state(Form.waiting_for_fio)

# @callback_router.message(Form.waiting_for_fio)
# async def process_fio(message: types.Message, state: FSMContext):
#     current_user_id = message.from_user.id
#     user_fio = message.text
#     user_updated = await update_user_fio(current_user_id, user_fio)  
#     text = f"Новое ФИО {user_fio}"
#     await message.answer(
#             text=f"{text}",
#             reply_markup=start(message)
#         )

# @callback_router.callback_query(CD.filter(F.cb_text == "DateBirth"))
# async def DateBirth_callback(query: types.CallbackQuery,state: FSMContext):
#     await query.message.delete()
#     await query.message.answer("Пожалуйста, введите Дату рождения в формате 2000.12.31 (год,месяц,день)")
#     await state.set_state(Form.waiting_for_DateBirth)

# @callback_router.message(Form.waiting_for_DateBirth)
# async def process_DateBirth(message: types.Message, state: FSMContext):
#     current_user_id = message.from_user.id
#     user_DateBirth = message.text
#     user_updated = await update_user_DateBirth(current_user_id, user_DateBirth)  
#     text = f"Новая Дата Рождения {user_DateBirth}"
#     await message.answer(
#             text=f"{text}",
#             reply_markup=start(message)
#         )

# @callback_router.callback_query(CD.filter(F.cb_text == "DateDeath"))
# async def DateDeath_callback(query: types.CallbackQuery, state: FSMContext):
#     await query.message.delete()
#     await query.message.answer("Пожалуйста, введите Дату смерти в формате 2000.12.31 (год, месяц, день)")
#     await state.set_state(Form.waiting_for_DateDeath)

# @callback_router.message(Form.waiting_for_DateDeath)
# async def process_DateDeath(message: types.Message, state: FSMContext):
#     current_user_id = message.from_user.id
#     user_DateDeath = message.text
#     user_updated = await update_user_DateDeath(current_user_id, user_DateDeath)  
#     text = f"Новая Дата Смерти: {user_DateDeath}"
#     await message.answer(
#             text=text,
#             reply_markup=start(message)
#         )

# @callback_router.callback_query(CD.filter(F.cb_text == "Epigraph"))
# async def Epigraph_callback(query: types.CallbackQuery, state: FSMContext):
#     await query.message.delete()
#     await query.message.answer("Введите короткий эпиграф про человека")
#     await state.set_state(Form.waiting_for_Epigraph)

# @callback_router.message(Form.waiting_for_Epigraph)
# async def process_Epigraph(message: types.Message, state: FSMContext):
#     current_user_id = message.from_user.id
#     user_Epigraph = message.text
#     user_updated = await update_user_Epigraph(current_user_id, user_Epigraph)  
#     text = f"Новый эпиграф {user_Epigraph}"
#     await message.answer(
#             text=text,
#             reply_markup=start(message)
#         )

# @callback_router.callback_query(CD.filter(F.cb_text == "Photos"))
# async def Epigraph_callback(query: types.CallbackQuery, state: FSMContext):
#     await query.message.delete()
#     await query.message.answer("Пришлите фотографии")
#     await state.set_state(Form.waiting_for_Photo)

# @callback_router.message(Form.waiting_for_Photo)
# async def process_Photo(message: types.Message, state: FSMContext):
#     current_user_id = message.from_user.id
#     if message.photo:
#         media_dir = settings.MEDIA_ROOT
#         downloaded_photos = []
#         good_photos = message.photo[-int(len(message.photo) / 2):]
#         for i in range(len(good_photos)):
#             rand_int = random.randint(1, 100) 
#             first_photo = good_photos[i]
#             photo_info = await bot.get_file(first_photo.file_id)
#             file_path = os.path.join(media_dir, f"{photo_info.file_id}.{rand_int}.jpg")
#             await bot.download_file(photo_info.file_path, file_path)
#             downloaded_photos.append(file_path)
#             user_updated = await update_user_Photos(current_user_id, f"{first_photo.file_id}.{rand_int}")


#         await message.answer(
#             f"{len(downloaded_photos)} фото успешно загружены!",
#             reply_markup=start(message)
#             )
#     else:
#         await message.answer("Пожалуйста, отправьте фото.")

# @callback_router.callback_query(CD.filter(F.cb_text == "Short"))
# async def epigraph_callback(callback_query: types.CallbackQuery, state: FSMContext):
#     current_user_id = callback_query.from_user.id
#     chat_id = callback_query.message.chat.id
    
#     # Отправляем сообщение пользователю
#     await callback_query.answer("Спустя некоторое время напишите /getshort и мы отправим вам видео")
#     await bot.send_message(chat_id, "Спустя некоторое время напишите /getshort и мы отправим вам видео")
    
#     # Генерируем короткое видео
#     shorts = await generate_short(current_user_id)
#     #Тут можно отправить Карточку Пользователя по API на ваш сервис

    

