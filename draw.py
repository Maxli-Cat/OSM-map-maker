from PIL import Image, ImageFont, ImageDraw

def setup(x,y):
    img = Image.new("RGB", (x,y), color=(255,255,255))
    drw = ImageDraw.Draw(img)

    return img, drw

def drawLines(points, drw : ImageDraw.ImageDraw, color=(0,0,0), width=1, closed=False):
    for p1, p2 in zip(points, points[1:]):

        drw.line((p1, p2), width=width, fill=color)
    #if closed:
    #    drw.line((points[0], points[-1]), width=width, fill=color)

def drawCollectionLines(collection : list[dict], drw : ImageDraw.ImageDraw, default_color = (0, 0, 0), default_width = 1, projection = lambda x:x, projection_args = []):
    for element in collection:
        if "color" in element.keys(): color = element["color"]
        else: color = default_color
        if "width" in element.keys(): width = element["width"]
        else: width = default_width
        for line in element["points"]:
            mapline = projection(line, *projection_args)
            drawLines(mapline, drw, width=width, color=color)

def drawCollectionPoly(collection : list[dict], drw : ImageDraw.ImageDraw, default_color = (0, 0, 0), default_width = 1, projection = lambda x:x, projection_args = []):
    for element in collection:
        if "color" in element.keys():
            color = element["color"]
        else:
            color = default_color
        if "width" in element.keys():
            width = element["width"]
        else:
            width = default_width
        for line in element["points"]:
            mapline = projection(line, *projection_args)
            drw.polygon(mapline, fill=color, outline=color, width=width)

