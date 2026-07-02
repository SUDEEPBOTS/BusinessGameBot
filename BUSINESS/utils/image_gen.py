import io
import re
from PIL import Image, ImageDraw, ImageFont

def clean_text(text):
    # Strip emojis and special characters for PIL rendering to avoid boxes
    if not text:
        return ""
    return re.sub(r'[^\x00-\x7F]+', '', text).strip()

def generate_roll_image(player_name, dice_val, space_name, price=None, rent=None, owner=None, event_text=None, balance=None):
    width, height = 800, 450
    
    # Create background with gradient or solid color
    bg_color = (20, 25, 35)
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Fonts
    font_path_bold = "BUSINESS/assets/fonts/bold.ttf"
    font_path_reg = "BUSINESS/assets/fonts/regular.ttf"
    
    try:
        title_font = ImageFont.truetype(font_path_bold, 50)
        subtitle_font = ImageFont.truetype(font_path_bold, 40)
        text_font = ImageFont.truetype(font_path_reg, 32)
        small_font = ImageFont.truetype(font_path_bold, 28)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # Draw neon border
    draw.rectangle([(15, 15), (width-15, height-15)], outline=(0, 255, 127), width=6)
    draw.rectangle([(25, 25), (width-25, height-25)], outline=(30, 45, 60), width=2)
    
    player_clean = clean_text(player_name)
    if not player_clean:
        player_clean = "PLAYER"
        
    title = f"{player_clean} ROLLED A {dice_val}!"
    
    # Center text
    try:
        bbox = draw.textbbox((0, 0), title, font=title_font)
        title_w = bbox[2] - bbox[0]
    except AttributeError:
        title_w = draw.textsize(title, font=title_font)[0]
        
    draw.text(((width - title_w) / 2, 40), title, font=title_font, fill=(0, 255, 127))
    
    # Line
    draw.line([(80, 110), (width-80, 110)], fill=(0, 255, 127), width=3)
    
    # Content
    y_offset = 140
    space_clean = clean_text(space_name)
    draw.text((60, y_offset), f"Landed on: {space_clean}", font=subtitle_font, fill=(255, 215, 0))
    y_offset += 65
    
    if price:
        draw.text((60, y_offset), f"Price: ${price}", font=text_font, fill=(255, 255, 255))
        y_offset += 45
    if rent:
        draw.text((60, y_offset), f"Base Rent: ${rent}", font=text_font, fill=(255, 100, 100))
        y_offset += 45
        
    if owner:
        draw.text((60, y_offset), f"Owner: {clean_text(owner)}", font=text_font, fill=(100, 255, 100))
        y_offset += 45
        
    if event_text:
        # Wrap event text if needed
        draw.text((60, y_offset), clean_text(event_text), font=text_font, fill=(200, 220, 255))
        y_offset += 45
        
    if balance is not None:
        balance_text = f"Balance: ${balance}"
        try:
            bbox = draw.textbbox((0, 0), balance_text, font=small_font)
            bal_w = bbox[2] - bbox[0]
        except AttributeError:
            bal_w = draw.textsize(balance_text, font=small_font)[0]
            
        draw.text((width - bal_w - 40, height - 60), balance_text, font=small_font, fill=(255, 255, 255))
        
    # Save to IO
    bio = io.BytesIO()
    bio.name = 'board.jpg'
    img.save(bio, 'JPEG', quality=90)
    bio.seek(0)
    return bio
