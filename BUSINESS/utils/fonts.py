def stylish_font(text: str) -> str:
    # A simple mapping for bold serif or stylish English font
    # You can map A-Z to 𝐀-𝐙 or something similar.
    # We will use simple mapping here for demonstration
    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    stylish = "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳"
    trans = str.maketrans(normal, stylish)
    return text.translate(trans)

def button_font(text: str) -> str:
    return f"˹ {stylish_font(text)} ˼"
