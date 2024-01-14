import math

DPI = 600
SIZE_INCH = (24, 36)
SIZE = (SIZE_INCH[0] * DPI, SIZE_INCH[1] * DPI)

CART_BOUNDS = (46.0, 36.61, -77.65, -68.63)

run = abs(CART_BOUNDS[0] - CART_BOUNDS[1]) * 111.32
rise = abs(CART_BOUNDS[2] - CART_BOUNDS[3]) * (40075 * math.cos(math.radians(CART_BOUNDS[0])) / 360)
aspect = run / rise
SIZE = (SIZE[0], int(SIZE[0] * aspect))
SIZE_INCH = (SIZE[0] / DPI, SIZE[1] / DPI)

nec_counties = ("Coaticook (MRC)", "Le Haut-Saint-François", "Le Granit",
            "New Hampshire", "Maine", "Rhode Island", "Vermont, USA", "Massachusetts, USA", "Connecticut, USA", "Delaware, USA",
            "Suffolk County, NY", "Clinton County, NY", "Essex County, NY", "Warren County, NY", "Washington County, NY", "Rensselaer County, NY", "Columbia County, NY", "Dutchess County, NY", "Putnam County, NY", "Westchester County, NY", "Nassau County, NY", "New York City",
            "Saint Lawrence County, NY", "Franklin County, NY",
            "Atlantic County, NJ", "Burlington County, NJ", "Camden County, NJ", "Cape May County, NJ", "Cumberland County, NJ", "Gloucester County, NJ", "Mercer County, NJ", "Monmouth County, NJ", "Ocean county, NJ", "Salem County, NJ",
            "Mifflin County, PA", "Sullivan County, PA",
            #"Dorchester County, MD", "Somerset County, MD", "Wicomico County, MD", "Worcester County, MD",
            "Accomack County, VA", "Northampton County, VA"
            )

if __name__ == "__main__":
    print(rise, run, aspect)
    print(SIZE)
    print(SIZE_INCH)