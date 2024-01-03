from OSMPythonTools.api import Api
from OSMPythonTools.nominatim import Nominatim as Nomtm
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
from geopy.geocoders import Nominatim
from joblib import Memory
import tqdm
import sys
import OSMPythonTools
mem = Memory("./cache")

geolocatior = Nominatim(user_agent="Sophies_Art_Maps_maxlicatenby@gmail.com")
overpass = Overpass()
nom = Nomtm(userAgent="Sophies_Art_Maps_maxlicatenby@gmail.com")

def old_lookup(location):
    return nom.query(location)

def raw_lookup(location):
    return geolocatior.geocode(location).raw["osm_id"]

lookup = mem.cache(raw_lookup)

def load_roads(area="Rockingham, NH", element='"highway"="motorway"'):
    osmid = lookup(area)
    areaId = osmid + 3600000000
    query = overpassQueryBuilder(area=areaId, elementType='way', selector=[f'{element}'])
    result = overpass.query(query)
    roads = []
    print(f"{element}, {area}", file=sys.stderr)
    for element in tqdm.tqdm(result.elements()):

        geo = element.geometry()["coordinates"]
        if isinstance(geo[0][0], list):
            geo = [x for xs in geo for x in xs]
        #print(type(geo[0][0]))
        roads.append(geo)
    #print(len(roads))
    return roads

def elements_from_relation(relation : OSMPythonTools.element.Element, level=0):
    assert relation.type() == 'relation'
    if level == -1: it = tqdm.tqdm(relation.members(), position=level+1, leave=False)
    else: it = relation.members()
    for member in it:
        if member.type() == 'way':
            yield member
        elif member.type() == 'node':
            continue
        else:
            print(level, member.type())
            for e in elements_from_relation(member, level + 1):
                yield e


def load_relations(area="New Hampshire", element = '"natural"="water"'):
    osmid = lookup(area)
    areaId = osmid + 3600000000
    query = overpassQueryBuilder(area=areaId, elementType='relation', selector=[f'{element}'])
    results = overpass.query(query)
    lines = []
    for result in tqdm.tqdm(results.elements(), position=0, leave=False):
        for member in elements_from_relation(result):
            lines.append(member.geometry()['coordinates'])
    return lines

if __name__ == "__main__":
    area = "New Hampshire"
    element = '"natural"="water"'
    osmid = lookup(area)
    areaId = osmid + 3600000000
    query = overpassQueryBuilder(area=areaId, elementType='relation', selector=[f'{element}'])
    results = overpass.query(query)

