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
    lang = "en" # We can add DB check for language later
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
        ]
    ]
    
    await message.reply_photo(
        photo=config.START_IMG_URL,
        caption=get_string(lang, "START_TEXT"),
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_callback_query(filters.regex(r"^help_page_(\d+)$"))
async def help_callback(client, callback_query):
    lang = "en"
    page = int(callback_query.matches[0].group(1))
    
    total_pages = 3
    
    buttons = []
    nav_row = []
    
    if page > 1:
        nav_row.append(InlineKeyboardButton(text=button_font("PREV"), callback_data=f"help_page_{page-1}"))
    
    nav_row.append(InlineKeyboardButton(text=f"• {page}/{total_pages} •", callback_data="none"))
    
    if page < total_pages:
        nav_row.append(InlineKeyboardButton(text=button_font("NEXT"), callback_data=f"help_page_{page+1}"))
        
    buttons.append(nav_row)
    buttons.append([InlineKeyboardButton(text=button_font(get_string(lang, "BTN_BACK")), callback_data="start_menu")])
    
    await callback_query.message.edit_caption(
        caption=get_string(lang, f"HELP_PAGE_{page}"),
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_callback_query(filters.regex("^help_menu$"))
async def help_menu_initial(client, callback_query):
    # Route to page 1
    callback_query.matches = [{"group": lambda x: "1"}] # mock match
    class MockMatch:
        def group(self, x): return "1"
    callback_query.matches = [MockMatch()]
    await help_callback(client, callback_query)

@app.on_callback_query(filters.regex("start_menu"))
async def start_callback(client, callback_query):
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
        ]
    ]
    await callback_query.message.edit_caption(
        caption=get_string(lang, "START_TEXT"),
        reply_markup=InlineKeyboardMarkup(buttons)
    )
