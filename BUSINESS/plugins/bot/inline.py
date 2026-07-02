from pyrogram import filters
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton
from BUSINESS.core.bot import app
from BUSINESS.utils.fonts import button_font
from BUSINESS.plugins.bot.start import START_TEXT
from BUSINESS import config

@app.on_inline_query()
async def inline_query_handler(client, query):
    string = query.query.lower()
    
    if string == "" or "help" in string or "start" in string:
        buttons = [
            [
                InlineKeyboardButton(text=button_font("PLAY NOW"), url=f"https://t.me/{app.me.username}?startgroup=true"),
            ],
            [
                InlineKeyboardButton(text=button_font("SUPPORT"), url="https://t.me/yuki_support"),
            ]
        ]
        
        answers = [
            InlineQueryResultArticle(
                title="Business Game Bot Help",
                description="Click here to see how to start playing the International Business Game!",
                thumb_url=config.START_IMG_URL,
                input_message_content=InputTextMessageContent(START_TEXT),
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        ]
        
        await query.answer(answers, cache_time=10)
