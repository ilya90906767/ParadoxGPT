from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

class CD(CallbackData, prefix="CallbackData"):
    cb_text: str = ""
    cb_message_id: int = 0

class CP(CallbackData, prefix="CallbackPersonas"):
    persona: str = ""

# def start(message):
#     builder = InlineKeyboardBuilder()
#     builder.button(text="Ввести ФИО", callback_data=CD(cb_text="FIO",cb_message_id=message.message_id).pack())
#     builder.button(text="Ввести дату рождения", callback_data=CD(cb_text="DateBirth",cb_message_id=message.message_id).pack())
#     builder.button(text="Ввести дату смерти (если есть)", callback_data=CD(cb_text="DateDeath",cb_message_id=message.message_id).pack())
#     builder.button(text="Прикрепить Эпиграф", callback_data=CD(cb_text="Epigraph",cb_message_id=message.message_id).pack())
#     builder.button(text="Прикрепить фотографии", callback_data=CD(cb_text="Photos",cb_message_id=message.message_id).pack())
#     builder.button(text="Сгенерировать короткое видео", callback_data=CD(cb_text="Short",cb_message_id=message.message_id).pack())
#     builder.adjust(1)

#     return builder.as_markup()

def start(message):
    builder = InlineKeyboardBuilder()
    builder.button(text="Начать чат", callback_data=CD(cb_text="chat",cb_message_id=message.message_id).pack())
    builder.button(text="Фото", callback_data=CD(cb_text="photo",cb_message_id=message.message_id).pack())
    builder.button(text="Личности", callback_data=CD(cb_text="personas",cb_message_id=message.message_id).pack())
    # builder.button(text="Настройки", callback_data=CD(cb_text="settings",cb_message_id=message.message_id).pack())
    # builder.button(text="Обратная связь", callback_data=CD(cb_text="feedback",cb_message_id=message.message_id).pack())
    builder.adjust(1)
    return builder.as_markup()

def gpt_dialog(message):
    builder = InlineKeyboardBuilder()
    builder.button(text="Закончить чат", callback_data=CD(cb_text="end_chat",cb_message_id=message.message_id).pack())
    builder.adjust(1)
    return builder.as_markup()

def chose_persona(personas):
    builder = InlineKeyboardBuilder()
    for persona in personas: 
        builder.button(text=f"{persona.name}", callback_data=CP(persona=persona.name).pack())
    builder.adjust(1)
    return builder.as_markup()