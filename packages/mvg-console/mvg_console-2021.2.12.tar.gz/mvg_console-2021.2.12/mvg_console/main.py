# coding=utf-8
import mvg_api as mvg

from .departure import Departure

from colr import color
from prettytable import PrettyTable

from typer import Typer

MVG_BG = "#2a4779"
MVG_FG = "#ffffff"

######
# Types of Transports
# 1. UBAHN
# 2. BUS
# 3. REGIONAL_BUS
# 4. TRAM
# 5. SBAHN
# 5. NACHT_BUSs
#######
app = Typer()

__package_name__ = "mvg_console"
__version__ = "2021.02.12"
__description__ = "A Command Line Tool to get the MVG departures for a station."

def display_title_bar():
    """ Print a title bar. """

    color_it_mvg = lambda x: color(x, fore=MVG_FG, back=MVG_BG)
    bar_mvg_colored = color_it_mvg("*" * 48)
    fifteen_stars = "*" * 15

    print(bar_mvg_colored)
    print(color_it_mvg(fifteen_stars + " MVG - Departures " + fifteen_stars))
    print(bar_mvg_colored + "\n")

def display_departures(station_name, limit=10, mode=None):
    station_id = mvg.get_id_for_station(station_name)
    assert station_id is not None, f"Station {station_name} not found!"

    departuresJSON = mvg.get_departures(station_id)

    departures = []
    if mode is not None:
        for d in departuresJSON:
            if mode.upper() in d['product']:
                departures += [Departure(d)]
    else:
        departures = [ Departure(i) for i in departuresJSON ]

    departures = departures[:limit]
    
    print('\nStation: '+station_name+'\n')
    
    
    table = PrettyTable(['Line', 'Destination', 'Departure (min)'])
    # table.set_deco(Texttable.HEADER)
 
    
    rows = []
    # rows.append(['Line', 'Destination', 'Departure (min)'])
    for dep in departures:
        rows.append( [dep.get_label_colored(), dep.destination, dep.departure_time_minutes] )
    table.add_rows(rows)
    # print( color(table.draw(), fore=MVG_FG, back=MVG_BG) )
    print(table)
    
def get_nearest_stations(address):
    location = mvg.get_locations(address)
    
    assert len(location) > 0, f"Location: {address} not found!"
    
    lat = location[0]['latitude']
    lng = location[0]['longitude']

    stations_json = mvg.get_nearby_stations(lat,lng)[:5]

    print('Nearest Stations to '+address+' :')
    print(''.join([str(idx+1)+". "+station['name']+": "+', '.join(station['products'])+'\n' for idx,station in enumerate(stations_json)]))
    return

@app.command("dest", help="Prints the departures from the station.")
def departures(station: str, limit: int=10, mode=None):
    display_departures(station_name=station, limit=limit, mode=mode)

@app.command("search", help="Displays the nearest stations to the search query.")
def search(query: str):
    get_nearest_stations(query)

@app.command("version", help="Displays version info.")
def version():
    print(__package_name__)
    print(__description__)
    print(f"Version: {__version__}")

if __name__ == "__main__":
    # main()
    app()
