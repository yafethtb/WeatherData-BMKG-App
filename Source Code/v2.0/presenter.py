from scrapermodule import *
from datetime import datetime as dt
from getpass import getuser
from dataclasses import dataclass
import flet as ft
import literaldata

day_tag = literaldata.DAY_TAG
city_dict = literaldata.CITY_PARAM

@dataclass
class PeriodicTimeUI:
    message: str
    bg_image: str
    fg_image: str
    main_text_color: str
    secondary_text_color: str

# ----------------
# Time functions
# ----------------
def periodic_ui():
    this_time = dt.now()
    this_hour = this_time.hour

    if this_hour > 1 and this_hour <= 5:
        return PeriodicTimeUI(
            f"Selamat subuh, {getuser()}!",
            literaldata.images['dawn-bg'],
            literaldata.images['dawn-fg'],
            "#4E2D3D",
            "#774B56"
        )
    elif this_hour > 5 and this_hour <= 12:
        return PeriodicTimeUI(
            f"Selamat Pagi, {getuser()}!",
            literaldata.images['morning-bg'],
            literaldata.images['morning-fg'],
            "#151C10",
            "#1A3017"
        )
    elif this_hour > 12 and this_hour <= 16:
        return PeriodicTimeUI(
            f"Selamat Siang, {getuser()}!",
            literaldata.images['noon-bg'],
            literaldata.images['noon-fg'],
            "#0B1212",
            "#3B4444"
        )
    elif this_hour > 16 and this_hour <= 19:
        return PeriodicTimeUI(
            f"Selamat Sore, {getuser()}!",
            literaldata.images['dawn-bg'],
            literaldata.images['dawn-fg'],
            "#000733",
            "#292F6C"
        )
    else:
        return PeriodicTimeUI(
            f"Selamat Malam, {getuser()}!",
            literaldata.images['night-bg'],
            literaldata.images['night-fg'],
            "#1B2A3A",
            "#28343E"
        )

# ----------------
# Dropdown options from model
# ----------------
def populate_city(query):
    """Populate city dropdown widget"""
    district_names = sorted(city_dict.keys())
    return [ft.dropdown.Option(city) for city in district_names if query.lower() in city.lower()]

def populate_days():
    """Populate day dropdown widget"""
    return [ft.dropdown.Option(day) for day in day_tag.keys()]

# ----------------
# Data responding from model
# ----------------    
def connection(param: str) -> BMKGScraper:
    return BMKGScraper(param)


# ----------------
# Showing data from model to viewer
# ----------------