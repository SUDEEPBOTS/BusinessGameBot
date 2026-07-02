from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from BUSINESS.core.bot import app
from BUSINESS import config
from BUSINESS.utils.fonts import button_font, stylish_font

START_TEXT = """
**Welcome to the International Business Game!** 🎲🏦

Buy properties in big countries, collect rent, and become a billionaire!
Start a game in your group and conquer the world.

Click below to explore commands or add me to your group.
"""

@app.on_message(filters.command(["start", "help"]))
async def start_command(client, message: Message):
    buttons = [
        [
            InlineKeyboardButton(text=button_font("ADD ME"), url=f"https://t.me/{app.me.username}?startgroup=true"),
        ],
        [
            InlineKeyboardButton(text=button_font("HELP"), callback_data="help_menu"),
            InlineKeyboardButton(text=button_font("ABOUT"), callback_data="about_menu"),
        ],
        [
            InlineKeyboardButton(text=button_font("SUPPORT"), url="https://t.me/yuki_support"),
        ]
    ]
    
    await message.reply_photo(
        photo=config.START_IMG_URL,
        caption=START_TEXT,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_callback_query(filters.regex("help_menu"))
async def help_callback(client, callback_query):
    help_text = """
**Game Commands:**
/business - Start a new game lobby in the group
/join - Join the active lobby
/start_game - Start the game (Admin only)
/roll - Roll the dice 🎲
/buy - Buy the current property
/board - View your properties and balance
"""
    buttons = [
        [
            InlineKeyboardButton(text=button_font("BACK"), callback_data="start_menu")
        ]
    ]
    await callback_query.message.edit_caption(
        caption=help_text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_callback_query(filters.regex("start_menu"))
async def start_callback(client, callback_query):
    buttons = [
        [
            InlineKeyboardButton(text=button_font("ADD ME"), url=f"https://t.me/{app.me.username}?startgroup=true"),
        ],
        [
            InlineKeyboardButton(text=button_font("HELP"), callback_data="help_menu"),
            InlineKeyboardButton(text=button_font("ABOUT"), callback_data="about_menu"),
        ],
        [
            InlineKeyboardButton(text=button_font("SUPPORT"), url="https://t.me/yuki_support"),
        ]
    ]
    await callback_query.message.edit_caption(
        caption=START_TEXT,
        reply_markup=InlineKeyboardMarkup(buttons)
    )
