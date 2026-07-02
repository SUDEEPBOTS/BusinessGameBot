from pyrogram.types import Message
from BUSINESS.core.bot import app
from BUSINESS import config

async def play_logs(message: Message, command: str):
    """
    Logs when someone uses a command in a group or private chat.
    Sends the log to the LOGGER_ID channel.
    """
    try:
        chat_type = message.chat.type
        user = message.from_user
        chat = message.chat

        log_text = f"""
#NEW_COMMAND_LOG

**Command:** `{command}`
**User:** {user.mention if user else 'Unknown'} [`{user.id if user else 'N/A'}`]
**Chat:** {chat.title if chat.title else 'Private'} [`{chat.id}`]
"""
        if config.LOGGER_ID:
            await app.send_message(config.LOGGER_ID, text=log_text)
    except Exception as e:
        print(f"Error in play_logs: {e}")
