import itertools
import time
import constants
import draw
import maps
import projections

from constants import SIZE

road_types = (
    '"highway"="motorway"',
    '"highway"="motorway_link"',
    '"highway"="trunk"',
    '"highway"="trunk_link"',
    #'"highway"="primary"',
    #'"highway"="secondary"',
    #'"highway"="tertiary"',
    #'"highway"="unclassified"',
    #'"highway"="residential"',
   # '"highway"="service"',
    #'"highway"="path"',
    #['"highway"="footway"','"footway"!="sidewalk"','"footway"!="crossing"', '"footway"!="traffic_island"','"footway"!="link"'],
    #'"highway"="track"',
    '"natural"="coastline"',
    '"railway"="rail"',
    '"route"="ferry"',
    '"highway"="cycleway"',
)

road_sizes = (
    5, #motorway
    4, #link
    4, #trunk
    3, #trunk_link
    #3, #primary
    #2, #secondary
    #1, #tertiary
    #1, #unclassified
    #1, #residential
   # 1, #service
    #1, #path
    #1, #footway
    #1, #track
    5, #coastline
    1, #railway
    1, #ferry
    1, #cycleway
)
road_colors = (
    (50,0,0),      #motorway
    (50,0,0),      #motorway link
    (0,0,0),       #trunk
    (0,0,0),       #trunk_link
    #(0,0,0),       #primary
    #(0,0,0),       #secondary
    #(0,0,0),       #tertiary
    #(50,50,50),    #unclassified
    #(75,75,75),    #residential
   # (125,125,125), #service
    #(0,87,0),     #path
    #(0,87,0),     #footway
    #(63,87,0),   #track
    (0,0,0),    #coastline
    (50,0,0),     #railway
    (0, 255, 255),  # ferry
    (0,175,0),   #bike
    (0,175,0),   #county
)
road_colors_b = (
    (200,200,200),      #motorway
    (200,200,200),      #motorway link
    (205,205,205),       #trunk
    (205,205,205),       #trunk_link
    #(205,205,205),       #primary
    #(210,210,210),       #secondary
    #(210,210,210),       #tertiary
    #(215,215,215),    #unclassified
   # (215,215,215),    #residential
    #(225,225,225), #service
    #(0,87,0),     #path
    #(0,87,0),     #footway
    #(159,171,127),   #track
    (0,0,0),    #coastline
    (250,200,200),     #railway
    (0, 255, 255),  # ferry
    (127,215,127),   #bike
    (0,0,0),   #county
)

container_types = (
    '"place"="island"',
    '"place"="islet"',
    '"natural"="water"',
    ['"aeroway"="aerodrome"', '"iata"'],
)

container_sizes = (
    1, #island
    1, #islet
    1, #water
    1, #airport
)

container_edge = (
    ((255,255,255), (255,255,255)), #island
    ((255,255,255), (255,255,255)), #islet
    ((225,240,255), (225,240,255)), #water
    ((240,120,0), (240,120,0)),#airport
)

route_types = (
    '"route"="train"',
    '"route"="subway"',
    '"route"="light_rail"',
    '"route"="bus"',
    '"route"="ferry"',
    ['"route"="bicycle"','"network"!="lcn"'],
    ['"route"="bicycle"','"network"="lcn"'],
)

route_sizes = (
    2, #train
    2, #subway
    2, #light rail
    1, #bus
    1, #ferry
    1, #bike
    1, #local bike
)

route_colors = (
    (255, 0, 0),  # train
    (255,0,255),  #subway
    (127,0,255),  #light rail
    (0,0,255),  #bus
    (0,255,255),  #ferry
    (0,175,0),   #bike
    (127,215,127),   #local bike
)

stop_types = (
    ['"railway"="station"','"train"="yes"', '"station"!="light_rail"','!"subway"'],
    ['"railway"="station"','"subway"="yes"'],
    ['"railway"="station"','"train"="yes"', '"station"="light_rail"'],
    '"highway"="bus_stop"',
    '"amenity"="ferry_terminal"',
    '"place"="county"',
)

stop_sizes = (
    5, #train
    3, #subway
    3, #light rail
    2, #bus
    3, #ferry
    30, #county
)

stop_colors = (
    (255, 0, 0),  # train
    (255, 0, 255),  # subway
    (127, 0, 255),  # light rail
    (0, 0, 255),  # bus
    (0, 255, 255),  # ferry
    (0, 0, 0),  # county
)

def build_lists(locations, features, colors=((0,0,0),), widths=(1,)):
    roads = []
    for location in locations:
        for feature, color, width in zip(features, itertools.cycle(colors), itertools.cycle(widths)):
            roads.append({"points":maps.cached_load_roads(area=location, element=feature), "width":width, "color":color})
    return roads

def build_list_nodes(locations, features, colors=((0, 0, 0),), sizes=(10,)):
    nodes = []
    for location in locations:
        for feature, color, size in zip(features, itertools.cycle(colors), itertools.cycle(sizes)):
            #print(f"{feature=}, {type(feature)}")
            nodes.append({"points": maps.load_nodes(area=location, element=feature), "size": size, "color": color})
    return nodes

def build_lists_relations(locations, features, colors=((0, 0, 0),), widths=(1,)):
    lines = []
    for location in locations:
        for feature, color, width in zip(features, itertools.cycle(colors), itertools.cycle(widths)):
            lines.append({"points":maps.double_cached_load_relations(area=location, element=feature), "width":width, "color":color})
    return lines

def build_lists_waters(locations, selector=['"natural"="water"']):
    for location in locations:
        for water in maps.cached_get_water_relations(location, selector=selector):
            yield water


counties = constants.nec_counties


if __name__ == '__main__':
    water = False
    start = time.time()
    img, drw = draw.setup(*SIZE)
    stations = build_list_nodes(counties, stop_types, colors=stop_colors, sizes=stop_sizes)

    while True:
        try:
            roads = build_lists(counties, road_types, widths=road_sizes, colors=road_colors_b)
            routes = build_lists_relations(counties, route_types, widths=route_sizes, colors=route_colors)
            break
        except Exception as ex:
            if "your internet connection" in str(ex):
                time.sleep(45)
            else:
                print(ex)
                exit()

    if water:
        while True:
            try:
                waters = build_lists(counties, container_types, widths=container_sizes, colors=container_edge)
                waters2 = build_lists_waters(counties)
                break
            except Exception as ex:
                if "your internet connection" in str(ex):
                    time.sleep(45)
                else:
                    print(ex)
                    exit()
        draw.drawCollectionWater(waters2, drw, projection=projections.cartesian, projection_args=[SIZE])
        draw.drawCollectionPoly(waters, drw, projection=projections.cartesian, projection_args=[SIZE])
    else:
        waters = build_lists(counties, (['"aeroway"="aerodrome"', '"iata"'],), widths=(1,), colors=(((240,120,0), (240,120,0)),))
        draw.drawCollectionPoly(waters, drw, projection=projections.cartesian, projection_args=[SIZE])

    maps.public_save_cache()
    draw.drawCollectionLines(roads[::-1] , drw, projection=projections.cartesian, projection_args=[SIZE])
    draw.drawCollectionLines(routes[::-1], drw, projection=projections.cartesian, projection_args=[SIZE])
    #draw.drawCollectionLines(state_lines , drw, projection=projections.cartesian, projection_args=[SIZE])
    draw.drawCollectionPoints(stations[::-1], drw, projection=projections.cartesian, projection_args=[SIZE])
    img.show()
    img.save("map.png")
    stop = time.time()
    print(f"Took {stop - start} seconds")