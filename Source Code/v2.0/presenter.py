from scrapermodule import *
from datetime import datetime as dt, timedelta as td
from getpass import getuser
from dataclasses import dataclass
import flet as ft
import literaldata
import locale

locale.setlocale(locale.LC_ALL, 'ID')

day_tag = literaldata.DAY_TAG
city_dict = literaldata.CITY_PARAM

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
    this_time = dt.now()
    this_hour = this_time.hour

    if this_hour > 1 and this_hour <= 5:
        return PeriodicTimeUI(
            f"Selamat subuh, {getuser()}!",
            literaldata.images['dawn-bg'],
            literaldata.images['dawn-fg'],
            ColorPalette("#4E2D3D","#774B56", "black", "black")
        )
    elif this_hour > 5 and this_hour <= 12:
        return PeriodicTimeUI(
            f"Selamat Pagi, {getuser()}!",
            literaldata.images['morning-bg'],
            literaldata.images['morning-fg'],
            ColorPalette("#151C10", "#1A3017", "black", "black"),            
        )
    elif this_hour > 12 and this_hour <= 16:
        return PeriodicTimeUI(
            f"Selamat Siang, {getuser()}!",
            literaldata.images['noon-bg'],
            literaldata.images['noon-fg'],
            ColorPalette("#0B1212", "#3B4444", "black", "black")           
        )
    elif this_hour > 16 and this_hour <= 19:
        return PeriodicTimeUI(
            f"Selamat Sore, {getuser()}!",
            literaldata.images['dawn-bg'],
            literaldata.images['dawn-fg'],
            ColorPalette("#000733", "#292F6C", "black", "black")  
        )
    else:
        return PeriodicTimeUI(
            f"Selamat Malam, {getuser()}!",
            literaldata.images['night-bg'],
            literaldata.images['night-fg'],
            ColorPalette("#1B2A3A", "#28343E", "#f9f871", "#907b9d"),            
        )

# ----------------
# Dropdown options from model
# ----------------
def populate_city(query):
    """Populate city dropdown widget"""
    district_names = sorted(city_dict.keys())
    return [ft.dropdown.Option(city) for city in district_names if query.lower() in city.lower()]
# ----------------
# Data responding from model
# ----------------    
def weather_block(data: Weatherdata, primary_font: str, secondary_font: str, main_color: str):
    """Create basic widget to contain data from Weatherdata class"""
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
    
def view_data(param: str, main_color: str, primary_font: str, secondary_font: str,  expansion: int):
    """Accessing BMKG and transform their data into information in widgets"""
    area_id = city_dict[param]
    connect = BMKGScraper(area_id)
    
    if connect.is_data:    
        today = [weather_block(data, primary_font, secondary_font, main_color) for data in connect.scraping(day_tag['HARI INI'])]
        tomorrow = [weather_block(data, primary_font, secondary_font, main_color) for data in connect.scraping(day_tag['BESOK'])]
        overmorrow = [weather_block(data, primary_font, secondary_font, main_color) for data in connect.scraping(day_tag['LUSA'])]

        highlight = today[0] if len(today) > 1 else ft.Column()
        bottom_today = today[1:] if len(today) > 0 else []
        
        tabs_today = [weather_container(day) for day in bottom_today] if len(bottom_today) > 0 else None
        tabs_tomorrow = [weather_container(day) for day in tomorrow]
        tabs_overmorrow = [weather_container(day) for day in overmorrow]

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

# ----------------
# Showing data from model to viewer
# ----------------

# Test

def main(page: ft.Page):
    page.title = "Testing"
    page.window_width = 1200
    page.window_height = 850
    page.window_maximizable = False
    page.window_resizable = False
    page.bgcolor = ft.colors.AMBER_50
    page.padding = ft.padding.all(50)
    data = view_data("Biringkanaya - Kota Makasar", 'blue', 1)

    highlight, example = data
    highlight.scale = 1.5
    
    top = ft.Container(
        content = ft.Column(
            controls = [
                ft.Text(
                    dt.now().strftime("%a, %d %b %Y"),
                    text_align = 'center',
                    size = 24,
                    weight = 'w800'
                ),
                highlight
            ],
            alignment = 'center',
            horizontal_alignment = 'center',
            spacing = 20
        ),
        expand = 6,
        alignment = ft.alignment.center,
        bgcolor = ft.colors.AMBER_50,
        padding = ft.padding.all(100)
    )

    bottom = ft.Container(
        content = example,
        expand = 4,
        bgcolor = ft.colors.BLUE_GREY_50,
        padding = ft.padding.all(20)
    )

    page.add(top, bottom)
    page.update()

if __name__ == '__main__':
    ft.app(target = main)