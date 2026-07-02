# Copyright (c) 2025 @SUDEEPBOTS <HellfireDevs>
# Location: delhi,noida
#
# All rights reserved.
#
# This code is the intellectual property of SUDEEPBOTS.
# You are not allowed to copy, modify, redistribute, or use this
# code for commercial or personal projects without explicit permission.
#
# Allowed:
# - Forking for personal learning
# - Submitting improvements via pull requests
#
# Not Allowed:
# - Claiming this code as your own
# - Re-uploading without credit or permission
# - Selling or using commercially
#
# Contact for permissions:
# Email: sudeepgithub@gmail.com

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from BUSINESS.core.bot import app
from BUSINESS.database.db import db
import config
from BUSINESS.utils.fonts import button_font
from BUSINESS.utils.language import get_string
import math

MODULES = [
    "GAME", "PARTY", "ADMIN", "SUDO", "TOOLS", "STATS", "TRADE"
]

def get_help_buttons(page: int, lang: str):
    items_per_page = 4
    total_pages = math.ceil(len(MODULES) / items_per_page)
    start_idx = page * items_per_page
    end_idx = start_idx + items_per_page
    current_modules = MODULES[start_idx:end_idx]
    buttons = []
    row = []
    for i, mod in enumerate(current_modules):
        row.append(InlineKeyboardButton(text=button_font(mod), callback_data=f"help_{mod.lower()}"))
        if len(row) == 2 or i == len(current_modules) - 1:
            buttons.append(row)
            row = []
    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton(text="<<<", callback_data=f"help_page_{page-1}"))
    else:
        nav_row.append(InlineKeyboardButton(text=" ", callback_data="ignore"))
    nav_row.append(InlineKeyboardButton(text=f"{page+1}/{total_pages}", callback_data="ignore"))
    if page < total_pages - 1:
        nav_row.append(InlineKeyboardButton(text=">>>", callback_data=f"help_page_{page+1}"))
    else:
        nav_row.append(InlineKeyboardButton(text=" ", callback_data="ignore"))
    buttons.append(nav_row)
    buttons.append([InlineKeyboardButton(text=button_font(get_string(lang, "BTN_BACK")), callback_data="start_menu")])
    return buttons

@app.on_callback_query(filters.regex(r"^help_menu$"))
async def help_menu_main(client, callback_query: CallbackQuery):
    lang = await db.get_group_lang(chat_id) if "chat_id" in locals() else (await db.get_group_lang(message.chat.id) if "message" in locals() else (await db.get_group_lang(callback_query.message.chat.id) if "callback_query" in locals() else "en"))
    buttons = get_help_buttons(0, lang)
    await callback_query.message.edit_caption(
        caption=get_string(lang, "HELP_MAIN"),
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_callback_query(filters.regex(r"^help_page_(\d+)$"))
async def help_menu_page(client, callback_query: CallbackQuery):
    lang = await db.get_group_lang(chat_id) if "chat_id" in locals() else (await db.get_group_lang(message.chat.id) if "message" in locals() else (await db.get_group_lang(callback_query.message.chat.id) if "callback_query" in locals() else "en"))
    page = int(callback_query.matches[0].group(1))
    buttons = get_help_buttons(page, lang)
    await callback_query.message.edit_caption(
        caption=get_string(lang, "HELP_MAIN"),
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_callback_query(filters.regex(r"^help_([a-z]+)$"))
async def help_module(client, callback_query: CallbackQuery):
    lang = await db.get_group_lang(chat_id) if "chat_id" in locals() else (await db.get_group_lang(message.chat.id) if "message" in locals() else (await db.get_group_lang(callback_query.message.chat.id) if "callback_query" in locals() else "en"))
    module = callback_query.matches[0].group(1).upper()
    try:
        text = get_string(lang, f"HELP_{module}")
    except:
        text = f"**{module} Module**\n\nCommands for {module} will be listed here."
    buttons = [
        [
            InlineKeyboardButton(text=button_font(get_string(lang, "BTN_BACK")), callback_data="help_menu")
        ]
    ]
    await callback_query.message.edit_caption(
        caption=text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_callback_query(filters.regex("start_menu"))
async def start_callback(client, callback_query: CallbackQuery):
    lang = await db.get_group_lang(chat_id) if "chat_id" in locals() else (await db.get_group_lang(message.chat.id) if "message" in locals() else (await db.get_group_lang(callback_query.message.chat.id) if "callback_query" in locals() else "en"))
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
    lang = await db.get_group_lang(chat_id) if "chat_id" in locals() else (await db.get_group_lang(message.chat.id) if "message" in locals() else (await db.get_group_lang(callback_query.message.chat.id) if "callback_query" in locals() else "en"))
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

@app.on_callback_query(filters.regex("ignore"))
async def ignore_callback(client, callback_query: CallbackQuery):
    await callback_query.answer()