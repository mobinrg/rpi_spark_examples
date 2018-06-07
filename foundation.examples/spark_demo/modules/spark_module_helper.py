# RPiSpark Test Module Helper
# 
# Author: Kunpeng Zhang
# 2018.4.15
#
# See LICENSE for details.


from PIL import ImageFont

# Draw button
def drawBtn(draw, x, y, w = 13, h = 13, outline = 255, fill= 0, dire = "center" ):
    """dire: center, right, left, up, down
    """
    if dire.upper() == "CENTER":
        draw.rectangle((x, y, x+w, y+h), outline=outline, fill=fill)
        return

    if dire.upper() == "UP":
        draw.polygon([(x, y+h), (x+w/2, y), (x+w, y+h)], outline=outline, fill=fill)
        return

    if dire.upper() == "DOWN":
        draw.polygon([(x, y), (x+w, y), (x+w/2, y+h)], outline=outline, fill=fill)
        return

    if dire.upper() == "LEFT":
        draw.polygon([(x, y+h/2), (x+w, y), (x+w, y+h)], outline=outline, fill=fill)
        return

    if dire.upper() == "RIGHT":
        draw.polygon([(x, y), (x+w, y+h/2), (x, y+h)], outline=outline, fill=fill)
        return
        
    if dire.upper() in ("A", "B"):
        draw.rectangle((x, y, x+w, y+h), outline=outline, fill=fill)
        # Load default font.
        font = ImageFont.load_default()
        fw, fh = font.getsize(dire.upper())
        draw.text((x + ((w-fw)/1.5), y + (h-fh)/1.5),  dire.upper(),  font=font, fill= 1 if fill==0 else 0 )
        return

def drawText(draw, x, y, title="", fill = 1):
    font = ImageFont.load_default()
    draw.text((x,y), title, font = font, fill= fill )

def drawMultiLineText(draw, x, y, w=128, h=64, text="", align="center", fontName=None, fontSize = 10, fill = 1):
    font = ImageFont.load_default() if fontName==None else ImageFont.truetype(fontName, fontSize)
    try:
        fw, fh = draw.multiline_textsize( text, font )
        draw.multiline_text( (x + (w-fw)/2, y) , text, font = font, align=align, fill=fill)
    except:
#         draw.multiline_text( (x + (w-100)/2, y) , text, font = font, align=align, fill=fill)
        print("")
