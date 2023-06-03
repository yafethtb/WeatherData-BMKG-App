from scrapermodule import *
from datetime import datetime as dt, timedelta as td
from time import gmtime, localtime
from getpass import getuser
from dataclasses import dataclass
import flet as ft
import literaldata

day_tag = literaldata.DAY_TAG
city_dict = literaldata.CITY_PARAM

# ----------------
# Data classes for controling UI
# ----------------

@dataclass
class ColorPalette:    
    main_text_color: str
    secondary_text_color: str
    result_main_text_color: str
    result_container_bg_color: str

@dataclass
class PeriodicTimeUI:
    message: str
    bg_image: str
    fg_image: str
    color: ColorPalette

# ----------------
# Time functions
# ----------------
def periodic_ui():
    """
    UI behavior controller.

    Return PeriodicTimeUI object with different data depends on the hour the user using the program.
    """
    this_time = dt.now()
    this_hour = this_time.hour

    if this_hour > 1 and this_hour <= 5:
        return PeriodicTimeUI(
            f"Selamat subuh, {getuser()}!",
            literaldata.images['dawn-bg'],
            literaldata.images['dawn-fg'],
            ColorPalette("#4E2D3D","#774B56", "black", "white")
        )
    elif this_hour > 5 and this_hour <= 12:
        return PeriodicTimeUI(
            f"Selamat Pagi, {getuser()}!",
            literaldata.images['morning-bg'],
            literaldata.images['morning-fg'],
            ColorPalette("#151C10", "#1A3017", "black", "white"),            
        )
    elif this_hour > 12 and this_hour <= 16:
        return PeriodicTimeUI(
            f"Selamat Siang, {getuser()}!",
            literaldata.images['noon-bg'],
            literaldata.images['noon-fg'],
            ColorPalette("#0B1212", "#3B4444", "black", "white")           
        )
    elif this_hour > 16 and this_hour <= 19:
        return PeriodicTimeUI(
            f"Selamat Sore, {getuser()}!",
            literaldata.images['dusk-bg'],
            literaldata.images['dusk-fg'],
            ColorPalette("#000733", "#292F6C", "black", "white")  
        )
    else:
        return PeriodicTimeUI(
            f"Selamat Malam, {getuser()}!",
            literaldata.images['night-bg'],
            literaldata.images['night-fg'],
            ColorPalette("#1B2A3A", "#28343E", "black", "white"),            
        )

def gmt_diff():
    """Return GMT time difference"""
    local_time = localtime().tm_hour
    gmt_time = gmtime().tm_hour
    return local_time - gmt_time

# ----------------
# Dropdown options from model
# ----------------
def populate_city(query: str):
    """Populate city dropdown widget"""
    district_names = sorted(city_dict.keys())
    return [ft.dropdown.Option(city) for city in district_names if query.strip().lower() in city.lower()]

# ----------------
# Transforming data class into widgets
# ----------------    
def weather_block(data: Weatherdata, primary_font: str, secondary_font: str, main_color: str):
    """Create basic widget to contain data from WeatherData class.
    
    It will transform data from WeatherData object into a collection of rows containing 
    variable data from the object inside a column.
    """
    return ft.Column(
        controls = [
            ft.Text(
                value = data.hour,
                size = 24,
                color= main_color,
                font_family = primary_font,
                text_align = 'center',
                weight = 'w800',
                opacity = 1
            ),
            ft.Image(
                src = literaldata.weather_icons[data.weather],
                width = 50,
                height = 50,
                color= main_color,
                tooltip = data.weather,
                opacity = 1
            ),
            ft.Text(
                value = data.temperature,                
                size = 18,
                color= main_color,
                font_family = secondary_font,
                text_align = 'center',
                tooltip = 'Suhu',
                weight = 'w800',
                opacity = 1
            ),                              
            ft.Text(
                value = data.humidity,              
                size = 16,
                color= main_color,
                font_family = secondary_font,
                text_align = 'center',
                tooltip = 'Kelembaban',
                weight = 'w800',
                opacity = 1
            ),
        ],
        alignment = 'center',
        horizontal_alignment = 'center',
        opacity = 1,
        expand = True
    )

def weather_container(control: ft.Column) -> ft.Container:
    """Create container to contain all weather_block's function result"""
    return ft.Container(
        content = control,
        padding = ft.padding.all(15),
        bgcolor = ft.colors.TRANSPARENT
    )

def day_scraping(weather: Weatherdata, main_color: str, primary_font: str, secondary_font: str ):
    """Sraping the website and return simple data"""
    d = [weather_block(data, primary_font, secondary_font, main_color) for data in weather.scraping(day_tag['D'])]
    d1 = [weather_block(data, primary_font, secondary_font, main_color) for data in weather.scraping(day_tag['D1'])]
    d2 = [weather_block(data, primary_font, secondary_font, main_color) for data in weather.scraping(day_tag['D2'])]
    d3 = [weather_block(data, primary_font, secondary_font, main_color) for data in weather.scraping(day_tag['D3'])]

    return d, d1, d2, d3
    
# ----------------
# Connecting web scraper module and UI module
# ----------------
def view_data(param: str, main_color: str, primary_font: str, secondary_font: str,  expansion: int):
    """
    Accessing BMKG and transform their data into information in widgets.
    
    When conected to internet and the website response status is OK, this program will return block of widgets of
    today's, tomorrow's, and overmorrow's weather data in tabs.

    If there is no internet connection or the response status is other than OK, this program will return 
    the error message.

    """
    area_id = city_dict[param]
    connect = BMKGScraper(area_id)
    gmt_time = gmt_diff()
    now = dt.now()
   
    if connect.is_data:    
        d, d1, d2, d3 = day_scraping(connect, main_color, primary_font, secondary_font)

        highlight = d[0] if len(d) > 0 else ft.Column()
        bottom_today = d[1:] if len(d) > 0 else []        
        tabs_today = [weather_container(day) for day in bottom_today] if len(bottom_today) > 0 else None
        tabs_tomorrow = [weather_container(day) for day in d1]
        tabs_overmorrow = [weather_container(day) for day in d2]

        # Untuk mengatasi tanggal tab berubah tapi data dalam tab tidak mengikuti tanggal
        wita_transition = gmt_time == 8 and (now.hour >= 0 and now.hour < 1)
        wit_transition = gmt_time == 9 and (now.hour >= 0 and now.hour < 2)

        if wita_transition or wit_transition:
            highlight = d1[0] if len(d1) > 0 else ft.Column()
            bottom_today = d1[1:] if len(d1) > 0 else []        
            tabs_today = [weather_container(day) for day in bottom_today] if len(bottom_today) > 0 else None
            tabs_tomorrow = [weather_container(day) for day in d2]
            tabs_overmorrow = [weather_container(day) for day in d3]
        
        return highlight, ft.Tabs(
            expand = expansion,
            tabs = [
                ft.Tab(
                    text = dt.now().strftime("%a, %d %b %Y"),
                    content = ft.Row(
                        controls = tabs_today,
                        alignment = 'start',
                        vertical_alignment = 'center',
                        spacing = 15,
                        scroll = 'adaptive'
                    )
                ),
                ft.Tab(
                    text = (dt.now() + td(1)).strftime("%a, %d %b %Y"),
                    content = ft.Row(
                        controls = tabs_tomorrow,
                        alignment = 'start',
                        vertical_alignment = 'center',
                        spacing = 15,
                        scroll = 'adaptive'
                    )
                ),
                ft.Tab(
                    text = (dt.now() + td(2)).strftime("%a, %d %b %Y"),
                    content = ft.Row(
                        controls = tabs_overmorrow,
                        alignment = 'start',
                        vertical_alignment = 'center',
                        spacing = 15,
                        scroll = ft.ScrollMode.ALWAYS
                    )
                )
            ],
            label_color = main_color,
            indicator_color = main_color,
            divider_color = 'white',
            indicator_border_radius = 15,
            opacity = 1
        )
    else:
        return ft.Image(
            src = literaldata.weather_icons['Alert'],
            width = 150,
            height = 150,
            color= main_color,
            tooltip = connect.connection.problem
        ), ft.Container(
            expand = expansion,
            content = ft.Column(
                controls = [
                    ft.Text(
                        connect.connection.problem,
                        size = 24,
                        color = main_color,
                        text_align = 'center',
                        weight = 'w800',
                        opacity = 1
                    ),
                    ft.Text(
                        connect.connection.error_type,
                        size = 18,
                        color = main_color,
                        text_align = 'center',
                        opacity = 1
                    )
                ],
                alignment = 'center',
                horizontal_alignment = 'center'
            ),
            bgcolor = ft.colors.TRANSPARENT,
            padding = ft.padding.all(20),            
        )
