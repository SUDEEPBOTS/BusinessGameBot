from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from BUSINESS.core.bot import app
from BUSINESS import config
from BUSINESS.utils.fonts import button_font
from BUSINESS.utils.language import get_string

@app.on_callback_query(filters.regex("^help_menu$"))
async def help_menu(client, callback_query: CallbackQuery):
    lang = "en"
    buttons = [
        [
            InlineKeyboardButton(text=button_font("GAME"), callback_data="help_game"),
            InlineKeyboardButton(text=button_font("ADMIN"), callback_data="help_admin"),
        ],
        [
            InlineKeyboardButton(text=button_font("SUDO"), callback_data="help_sudo"),
            InlineKeyboardButton(text=button_font("TOOLS"), callback_data="help_tools"),
        ],
        [
            InlineKeyboardButton(text=button_font(get_string(lang, "BTN_BACK")), callback_data="start_menu")
        ]
    ]
    await callback_query.message.edit_caption(
        caption=get_string(lang, "HELP_MAIN"),
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_callback_query(filters.regex(r"^help_(game|admin|sudo|tools)$"))
async def help_module(client, callback_query: CallbackQuery):
    lang = "en"
    module = callback_query.matches[0].group(1).upper()
    
    buttons = [
        [
            InlineKeyboardButton(text=button_font(get_string(lang, "BTN_BACK")), callback_data="help_menu")
        ]
    ]
    await callback_query.message.edit_caption(
        caption=get_string(lang, f"HELP_{module}"),
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_callback_query(filters.regex("start_menu"))
async def start_callback(client, callback_query: CallbackQuery):
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
    await callback_query.message.edit_caption(
        caption=get_string(lang, "START_TEXT"),
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_callback_query(filters.regex("about_menu"))
async def about_callback(client, callback_query: CallbackQuery):
    lang = "en"
    about_text = "> **Business Game Bot** 🏦\n>\n> A multiplayer board game bot built with Kurigram.\n> Play with your friends globally!"
    buttons = [
        [
            InlineKeyboardButton(text=button_font(get_string(lang, "BTN_BACK")), callback_data="start_menu")
        ]
    ]
    await callback_query.message.edit_caption(
        caption=about_text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )
