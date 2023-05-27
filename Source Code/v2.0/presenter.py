from scrapermodule import *
import flet as ft
import literaldata

day_tag = literaldata.DAY_TAG
city_dict = literaldata.CITY_PARAM
# color = literaldata.ColorPalette

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
# def show_result(city, tag):
#     """Show results of what user choose to see"""
#     id = city_dict[city]
#     daytag = day_tag[tag]
#     data = BMKGScraper(id, daytag).scraping
    
#     datalist = [datum for datum in data]
#     weather = all([isinstance(point, Weatherdata) for point in datalist])
#     error = all([isinstance(point, ConnError) for point in datalist])
#     badcode = all([isinstance(point, ResponseResult) for point in datalist])

#     if weather:
#         return construct_weather_data(datalist)
#     elif error:
#         return show_error_message(datalist)
#     elif badcode:
#         return show_bad_code(datalist)
    
# ----------------
# Showing data from model to viewer
# ----------------