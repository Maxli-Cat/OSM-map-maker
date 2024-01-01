import itertools

import draw
import maps
import projections

#SIZE = (2500*2,1800*2)
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
    '"highway"="service"',
    '"highway"="path"',
    '"highway"="footway"',
    '"highway"="track"',
)

road_sizes = (5,4,4,3,2,1,1,1,1,1,1,1,1,1,1)
road_colors = (
    (0,0,0),
    (0,0,0),
    (0,0,0),
    (0,0,0),
    (0,0,0),
    (0,0,0),
    (50,50,50),
    (75,75,75),
    (75,75,75),
    (0,175,0),
    (0,175,0),
    (125,175,0)

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
    roads = build_lists(("Epping, NH","Raymond, NH", "Lee, NH", "Newfields, NH", "Exeter, NH", "Nottingham, NH", "Newmarket, NH", "Freemont, NH", "Kingston, NH"),
                        road_types, widths=road_sizes, colors=road_colors)

    draw.drawCollection(roads, drw, projection=projections.cartesian, projection_args=[SIZE])
    img.show()
