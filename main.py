import itertools

import draw
import maps
import projections

from constants import SIZE

road_types = (
    '"highway"="motorway"',
    '"highway"="motorway_link"',
    '"highway"="trunk"',
    '"highway"="primary"',
    '"highway"="secondary"',
    '"highway"="tertiary"',
    '"highway"="unclassified"',
    '"highway"="residential"',
    #'"highway"="service"',
    '"highway"="path"',
    '"highway"="footway"',
    '"highway"="track"',
)

road_sizes = (
    5, #motorway
    4, #link
    4, #trunk
    3, #primary
    2, #secondary
    1, #tertiary
    1, #unclassified
    1, #residential
    #1, #service
    1, #path
    1, #footway
    1, #track
)
road_colors = (
    (50,0,0),      #motorway
    (50,0,0),      #motorway link
    (0,0,0),       #trunk
    (0,0,0),       #primary
    (0,0,0),       #secondary
    (0,0,0),       #tertiary
    (50,50,50),    #unclassified
    (75,75,75),    #residential
    #(125,125,125), #service
    (0,175,0),     #path
    (0,175,0),     #footway
    (125,175,0),   #track
    (0,50,150),    #island
    (0,50,150),    #islet
    (0,50,150),    #water
)

container_types = (
    '"place"="island"',
    '"place"="islet"',
    '"natural"="water"',
)

container_sizes = (
    2, #island
    1, #islet
    1, #water
)

container_edge = (
    (137,101,53), #island
    (137,101,53), #islet
    (55,121,229), #water
)
def buildlist(location):
    roads = [{"points": maps.load_roads(area=location, element='"highway"="motorway"'),        "width": 5, "color": (10, 0, 0)},
             {"points": maps.load_roads(area=location, element='"highway"="motorway_link"'),   "width": 4, "color": (10, 0, 0)},
             {"points": maps.load_roads(area=location, element='"highway"="trunk"'),           "width": 4},
             {"points": maps.load_roads(area=location, element='"highway"="primary"'),         "width": 3},
             {"points": maps.load_roads(area=location, element='"highway"="secondary"'),       "width": 2},
             {"points": maps.load_roads(area=location, element='"highway"="tertiary"'),        "width": 1},
             {"points": maps.load_roads(area=location, element='"highway"="unclassified"'),    "width": 1, "color": (175, 175, 175)},
             {"points": maps.load_roads(area=location, element='"highway"="residential"'),     "width": 1, "color": (125, 125, 125)},
             {"points": maps.load_roads(area=location, element='"highway"="path"'),            "width": 1, "color": (0, 175, 0)},
             {"points": maps.load_roads(area=location, element='"highway"="footway"'),         "width": 1, "color": (0, 175, 0)},
             {"points": maps.load_roads(area=location, element='"highway"="track"'),           "width": 1, "color": (125, 175, 0)},
             {"points": maps.load_roads(area="New Hampshire", element='"boundary"="administrative"'), "width": 3, "color":(255,0,0)}
             ]
    return roads

def build_lists(locations, features, colors=((0,0,0),), widths=(1,)):
    roads = []
    for location in locations:
        for feature, color, width in zip(features, itertools.cycle(colors), itertools.cycle(widths)):
            roads.append({"points":maps.load_roads(area=location, element=feature), "width":width, "color":color})
    return roads

if __name__ == '__main__':
    img, drw = draw.setup(*SIZE)

    #roads = buildlist("Rockingham, NH") + buildlist("Strafford, NH")
    roads = build_lists(("Rockingham, NH", "Strafford, NH"),
                        road_types, widths=road_sizes, colors=road_colors)

    draw.drawCollection(roads, drw, projection=projections.cartesian, projection_args=[SIZE])
    img.show()
