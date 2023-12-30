from PIL import Image, ImageFont, ImageDraw

def setup(x,y):
    img = Image.new("RGB", (x,y), color=(255,255,255))
    drw = ImageDraw.Draw(img)

    return img, drw

def drawLines(points, drw : ImageDraw.ImageDraw, color=(0,0,0), width=1, closed=False):
    for p1, p2 in zip(points, points[1:]):
        drw.line((p1, p2), width=width, fill=color)
    if closed:
        drw.line((points[0], points[-1]), width=width, fill=color)

