from pyrogram import filters
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton
from BUSINESS.core.bot import app
from BUSINESS.utils.fonts import button_font
from BUSINESS.utils.language import get_string
from BUSINESS import config

@app.on_inline_query()
async def inline_query_handler(client, query):
    string = query.query.lower()
    lang = "en"
    
    if string == "" or "help" in string or "start" in string:
        buttons = [
            [
                InlineKeyboardButton(text=button_font(get_string(lang, "BTN_PLAY_NOW")), url=f"https://t.me/{app.me.username}?startgroup=true"),
            ],
            [
                InlineKeyboardButton(text=button_font(get_string(lang, "BTN_SUPPORT")), url="https://t.me/yuki_support"),
            ]
        ]
        
        answers = [
            InlineQueryResultArticle(
                title=get_string(lang, "INLINE_HELP_TITLE"),
                description=get_string(lang, "INLINE_HELP_DESC"),
                thumb_url=config.START_IMG_URL,
                input_message_content=InputTextMessageContent(get_string(lang, "START_TEXT")),
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        ]
        
        await query.answer(answers, cache_time=10)
