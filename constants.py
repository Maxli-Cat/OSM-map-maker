import math

DPI = 600
SIZE_INCH = (24, 36)
SIZE = (SIZE_INCH[0] * DPI, SIZE_INCH[1] * DPI)

US_CART_BOUNDS = (46.0, 36.61, -77.65, -68.63)
CZ_CART_BOUNDS = (50.18, 49.9, 14.17, 14.72)
CART_BOUNDS = US_CART_BOUNDS

run = abs(CART_BOUNDS[0] - CART_BOUNDS[1]) * 111.32
rise = abs(CART_BOUNDS[2] - CART_BOUNDS[3]) * (40075 * math.cos(math.radians(CART_BOUNDS[0])) / 360)
aspect = run / rise
SIZE = (SIZE[0], int(SIZE[0] * aspect))
SIZE_INCH = (SIZE[0] / DPI, SIZE[1] / DPI)

nec_counties = ("New Hampshire", "Maine", "Rhode Island", "Vermont, USA", "Massachusetts, USA", "Connecticut, USA", "Delaware, USA", "New Jersey, USA", "Washington, DC", #"Maryland, USA",

                #'Acton, Quebec', "Agglomération de Longueuil", 'Agglomération de Montréal', 'Antoine-Labelle (MRC)', 'Arthabaska, Quebec', 'Beauce-Sartigan', "Beauharnois-Salaberry",
                #'Brome-Missisquoi', 'Coaticook (MRC)', "D'Autray", 'Deux-Montagnes (MRC)', 'Drummond, Quebec', 'Joliette (MRC)', "L'Assomption (MRC)", 'La Haute-Yamaska, Quebec',
                #'La Vallée-de-la-Gatineau', "La Vallée-du-Richelieu", 'Laval, Quebec', 'Le Granit', "Le Haut-Richelieu", 'Le Haut-Saint-François', "Le Haut-Saint-Laurent", 'Le Val-Saint-François',
                #'Les Appalaches', "Les Collines-de-l'Outaouais", "Les Jardins-de-Napierville", 'Les Laurentides', "Les Maskoutains", 'Les Moulins', "Les Pays-d'en-Haut", 'Les Sources',
                #"Marguerite-D'Youville", 'Matawinie (MRC)', "Memphrémagog", 'Mirabel, Quebec', 'Montcalm', 'Papineau (MRC)', 'Pontiac (MRC)', "Pierre-De Saurel", "Rouville, Quebec",
                #"Sherbrooke, Quebec", 'Thérèse-De Blainville', 'Vaudreuil-Soulanges', 'Ville de Gatineau'

                "City of Belleville, Ontario", "City of Cornwall, Ontario", "City of Kingston, Ontario", "City of Quinte West, Ontario",
                "Frontenac County, Ontario", "Hastings County, Ontario", "Gananoque, Ontario", "Leeds and Grenville Counties, Ontario",
                #"Lennox and Addington County, Ontario", "Nipissing District, Ontario", "Northumberland County, Ontario", "Ottawa, Ontario",
                #"Prescott and Russell Counties, Ontario", "Prince Edward County, Ontario", "Renfrew County, Ontario", "Stormont, Dundas and Glengarry Counties, Ottawa", "Town of Prescott, Ontario"

                #"Albany County, NY", "Broome County, NY", "Cayuga County, NY", "Chemung County, NY", 'Clinton County, NY', 'Columbia County, NY',
                #'Dutchess County, NY', 'Essex County, NY', 'Franklin County, NY', "Fulton County, NY", "Hamilton County, NY",
                #"Herkimer County, NY", 'Jefferson County, NY', "Lewis County, NY", "Livingston County, NY", "Montgomery County, NY", "Monroe County, NY", 'Nassau County, NY', 'New York City',
                #"Oneida County, NY", "Onondaga County, NY", "Ontario County, NY", "Oswego County, NY", 'Putnam County, NY', 'Rensselaer County, NY', 'Saint Lawrence County, NY',
                "Saratoga County, NY", "Schenectady County, NY", "Schoharie County, NY", "Schuyler County, NY", "Seneca County, NY", 'Suffolk County, NY', "Tioga County, NY", "Tompkins County, NY",
                'Warren County, NY', 'Washington County, NY', "Wayne County, NY", 'Westchester County, NY', "Yates County, NY",

                "Bradford County, PA","Delaware County, PA", "Mifflin County, PA", "Philadelphia County, PA", "Potter County, PA",
                "Sullivan County, PA", "Susquehanna County, PA", "Tioga County, PA", "Wayne County, PA",

                "Caroline County, MD", "Cecil County, MD", "Dorchester County, MD", "Kent County, MD", "Queen Anne's County, MD",
                "Somerset County, MD", "Talbot County, MD", "Wicomico County, MD", "Worcester County, MD",

                "Accomack County, VA", "Northampton County, VA",
)

cz_counties = ("Praha, CZ",)

if __name__ == "__main__":
    print(rise, run, aspect)
    print(SIZE)
    print(SIZE_INCH)