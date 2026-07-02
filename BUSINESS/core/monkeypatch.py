import random
from pyrogram.types import InlineKeyboardButton
from pyrogram.enums import Button

# Premium Emojis IDs (You can customize these to fit the business game theme)
PREMIUM_EMOJIS = [
    "5238162283368035495", # Green leaf or play
    "5408916593780470262",
    "5409262351532701571",
    "5409042015415448331",
    "6294287714887933094",
    "6291837599254322363",
    "6294047505957003963",
]

# Standard Styles
STYLES = [Button.PRIMARY, Button.SUCCESS, Button.DANGER, Button.SECONDARY]

def get_random_style():
    return random.choice(STYLES)

def get_random_emoji():
    return random.choice(PREMIUM_EMOJIS)

# YUKI6 Style Monkeypatching
original_init = InlineKeyboardButton.__init__

def patched_init(self, text: str, callback_data: str = None, url: str = None,
                 web_app=None, login_url=None, user_id=None, switch_inline_query=None,
                 switch_inline_query_current_chat=None, switch_inline_query_chosen_chat=None,
                 callback_game=None, pay=None, style=None, icon_custom_emoji_id=None,
                 icon_emoji=None, icon_is_centered=None, copy_text=None):
    
    # Inject Custom Styles and Emojis dynamically if not provided
    if style is None:
        style = get_random_style()
    if icon_custom_emoji_id is None:
        icon_custom_emoji_id = get_random_emoji()

    # Call original init
    original_init(self, text=text, callback_data=callback_data, url=url,
                  web_app=web_app, login_url=login_url, user_id=user_id, 
                  switch_inline_query=switch_inline_query,
                  switch_inline_query_current_chat=switch_inline_query_current_chat, 
                  switch_inline_query_chosen_chat=switch_inline_query_chosen_chat,
                  callback_game=callback_game, pay=pay, style=style, 
                  icon_custom_emoji_id=icon_custom_emoji_id,
                  icon_emoji=icon_emoji, icon_is_centered=icon_is_centered, copy_text=copy_text)

# Apply patch
InlineKeyboardButton.__init__ = patched_init
