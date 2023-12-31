from OSMPythonTools.api import Api
from OSMPythonTools.nominatim import Nominatim as Nomtm
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
from geopy.geocoders import Nominatim
from joblib import Memory
import tqdm
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
    for element in tqdm.tqdm(result.elements()):
        roads.append(element.geometry()["coordinates"])
    #print(len(roads))
    return roads


