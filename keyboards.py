from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def generate_categories(categories):  # [(3D, ), (Абстракция, ),.... ]
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    buttons = []
    for category in categories:
        btn = KeyboardButton(text=category[0])
        buttons.append(btn)
    markup.add(*buttons)
    return markup


def download_button(image_id):
    markup = InlineKeyboardMarkup()
    download = InlineKeyboardButton(text='Скачать изображение', callback_data=f'download_{image_id}')  # 64 бит - 64 символа
    markup.add(download)
    return markup
