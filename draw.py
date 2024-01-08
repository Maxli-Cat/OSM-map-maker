from PIL import Image, ImageFont, ImageDraw

def setup(x,y):
    img = Image.new("RGB", (x,y), color=(255,255,255))
    drw = ImageDraw.Draw(img)

    return img, drw

def drawPoints(points, drw: ImageDraw.ImageDraw, color=(0,0,0), size=10, projection = lambda x:x, projection_args = []):
    mapped_points = projection(points, *projection_args)

    for point in mapped_points:
        drw.regular_polygon(point + (size,), n_sides=40, fill=color)

def drawCollectionPoints(collection : list[dict], drw : ImageDraw.ImageDraw, default_color = (0, 0, 0), default_size = 1, projection = lambda x:x, projection_args = []):
    for element in collection:
        if "color" in element.keys(): color = element["color"]
        else: color = default_color
        if "size" in element.keys(): size = element["size"]
        else: size = default_size
        for point in element["points"]:
            mapline = projection((point,), *projection_args)[0]
            drw.regular_polygon(mapline + (size,), n_sides=40, fill=color)

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

def drawCollectionPoly(collection : list[dict], drw : ImageDraw.ImageDraw, default_color = ((255,255,255), (0,0,0)), default_width = 1, projection = lambda x:x, projection_args = []):
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
            try:
                drw.polygon(mapline, fill=color[0], outline=color[1], width=width)
            except TypeError as ex:
                print(str(ex))
                print(mapline)

def drawCollectionWater(collection : list[list], drw : ImageDraw.ImageDraw, default_color = ((225,240,255), (225,240,255)), default_width = 1, projection = lambda x:x, projection_args = []):
    for element in collection:
        color = default_color
        width = default_width
        mapline = projection(element, *projection_args)
        try:
            drw.polygon(mapline, fill=color[0], outline=color[1], width=width)
        except TypeError as ex:
            pass
            #print(str(ex))
            #print(mapline)