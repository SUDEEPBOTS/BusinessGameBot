from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from BUSINESS.core.bot import app
from BUSINESS import config
from BUSINESS.utils.fonts import button_font
from BUSINESS.utils.language import get_string
from BUSINESS.utils.logger import play_logs

@app.on_message(filters.command(["start", "help"]))
async def start_command(client, message: Message):
    await play_logs(message, "start")
    lang = "en" 
    buttons = [
        [
            InlineKeyboardButton(text=button_font(get_string(lang, "BTN_ADD_ME")), url=f"https://t.me/{app.me.username}?startgroup=true"),
        ],
        [
            InlineKeyboardButton(text=button_font(get_string(lang, "BTN_HELP")), callback_data="help_menu"),
            InlineKeyboardButton(text=button_font(get_string(lang, "BTN_ABOUT")), callback_data="about_menu"),
        ],
        [
            InlineKeyboardButton(text=button_font(get_string(lang, "BTN_SUPPORT")), url="https://t.me/yuki_support"),
            InlineKeyboardButton(text=button_font(get_string(lang, "BTN_OWNER")), url=f"tg://user?id={config.OWNER_ID}")
        ]
    ]
    await message.reply_photo(
        photo=config.START_IMG_URL,
        caption=get_string(lang, "START_TEXT"),
        reply_markup=InlineKeyboardMarkup(buttons)
    )