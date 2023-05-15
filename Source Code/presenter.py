from scrapermodule import *
import flet as ft
import literaldata

day_tag = literaldata.DAY_TAG
city_dict = literaldata.CITY_PARAM

# ----------------
# Dropdown options from model
# ----------------
def populate_city():
    """Populate city dropdown widget"""
    return [ft.dropdown.Option(city) for city in sorted(city_dict.keys())]

def populate_days():
    """Populate day dropdown widget"""
    return [ft.dropdown.Option(day) for day in day_tag.keys()]

# ----------------
# Data responding from model
# ----------------
def show_result(city, tag):
    """Show results of what user choose to see"""
    id = city_dict[city]
    daytag = day_tag[tag]
    data = BMKGScraper(id, daytag).scraping
    
    datalist = [datum for datum in data]
    weather = all([isinstance(point, Weatherdata) for point in datalist])
    error = all([isinstance(point, ConnError) for point in datalist])
    badcode = all([isinstance(point, ResponseResult) for point in datalist])

    if weather:
        return construct_weather_data(datalist)
    elif error:
        return show_error_message(datalist)
    elif badcode:
        return show_bad_code(datalist)
    
# ----------------
# Showing data from model to viewer
# ----------------
def weather(data: Weatherdata): 
    """Reconstrucing data from Weatherdata dataclass into column of texts inside flet widget"""
    return ft.Column(
        controls = [
            ft.Text(f'Tanggal: {data.date}', size = 24,style = 'titleMedium', weight = 'bold'),
            ft.Text(f'Jam: {data.hour}', size = 20, style = 'bodyLarge'),
            ft.Text(f'Suhu: {data.temperature}', size = 20, style = 'bodyLarge'),
            ft.Text(f'Cuaca: {data.weather}',  size = 20, style = 'bodyLarge'),
            ft.Text(f'Kelembaban: {data.humidity}',  size = 20, style = 'bodyLarge'),
            ft.Text(f'Kecepatan Angin: {data.wind_speed}',  size = 20, style = 'bodyLarge')
        ],        
        alignment = 'spaceEvenly'
    )        

def construct_weather_data(data: list[Weatherdata]):
    """Construct all weather widgets to the bigger widget"""
    container_list = []
    for datum in data:
        container_list.append(
            ft.Container(
                content = weather(datum), 
                border_radius = ft.border_radius.all(5),
                margin = ft.margin.all(20),
                padding = ft.padding.all(20),
                shadow = ft.BoxShadow(
                    spread_radius = 10.0,
                    blur_radius = 5.0,
                    color = '#AAC8A7',
                    blur_style = ft.ShadowBlurStyle.OUTER
                ),
                width = 100,
                bgcolor = '#C9DBB2'
            )
        )

    return ft.GridView(
        child_aspect_ratio = 1.0,
        controls = container_list,
        padding = ft.padding.all(50),
        runs_count = 3,
        spacing = 10
    )

def show_error_message(data: list[ConnError]):
    error_msg = data[0].problem
    return ft.Container(
        content = ft.Column(
            controls = [
                ft.Text(
                    'Terdapat masalah dalam pengambilan data',
                    size = 60,
                    weight = 'bold',
                    style = 'titleLarge'
                    ),
                ft.Text(
                    f'Tipe masalah: {error_msg}',
                    size = 48,
                    weight = 'bold',
                    style = 'headerLarge'
                    )
            ]                
        ),
        alignment = ft.alignment.center,        
        bgcolor = '#C9DBB2',
        border_radius = ft.border_radius.all(5),
        margin = ft.margin.all(20),
        padding = ft.padding.all(20),
        shadow = ft.BoxShadow(
            spread_radius = 10.0,
            blur_radius = 5.0,
            color = '#AAC8A7',
            blur_style = ft.ShadowBlurStyle.OUTER
        )
    )

def show_bad_code(data: list[ResponseResult]):
    bad_code = data[0].code
    return ft.Container(
        content = ft.Column(
            controls = [
                ft.Text(
                    'Terdapat masalah dalam koneksi.',
                    size = 60,
                    weight = 'bold',
                    style = 'titleLarge'
                    ),
                ft.Text(
                    f'Kode status: {bad_code}',                    
                    size = 48,
                    weight = 'bold',
                    style = 'headerLarge'
                    )
            ]
        ),        
        alignment = ft.alignment.center,        
        bgcolor = '#C9DBB2',
        border_radius = ft.border_radius.all(5),
        margin = ft.margin.all(20),
        padding = ft.padding.all(20),
        shadow = ft.BoxShadow(
            spread_radius = 10.0,
            blur_radius = 5.0,
            color = '#AAC8A7',
            blur_style = ft.ShadowBlurStyle.OUTER
        )
    )
    
