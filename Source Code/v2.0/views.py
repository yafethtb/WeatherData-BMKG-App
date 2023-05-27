import flet as ft
from presenter import *
from datetime import datetime as dt
from time import sleep
import locale

locale.setlocale(locale.LC_ALL, 'ID')


def main(page: ft.Page):
    # Page initialization
    page.title = 'WeatherData BMKG 2.0'
    page.window_max_height = 850
    page.window_max_width = 1200
    page.window_min_height = 850
    page.window_min_width = 1200
    page.window_maximizable = False
    page.fonts = {
        'josefin_sans': '/fonts/JosefinSans-Regular.ttf',
        'playfair': '/fonts/Playfair_144pt-Regular.ttf',
        'work_sans': '/fonts/WorkSans-Regular.ttf',
    }
    page.update()

    # functions
    def showtime():
        while True:
            clock.value = dt.now().strftime("%H:%M:%S")
            page.update()
            sleep(1)

    def show_dropdown(e):
        if search_query.value != '':
            search_option.visible = True
            search_option.options = populate_city(search_query.value) 
        else:
            search_option.visible = False
        
        search_container.update()

    def animate(e):
        ...


    # Search layer widgets
    search_query = ft.TextField(
        text_style = ft.TextStyle(
            font_family = 'work_sans',
            color = 'black',
            weight = 'w600'
        ),
        on_change = show_dropdown
    )

    search_option = ft.Dropdown(
        options = [],
        visible= False
        )
    
    search_button = ft.IconButton(
        icon = ft.icons.MANAGE_SEARCH_OUTLINED,
        icon_size = 40,
        icon_color = ft.colors.BLUE_GREY_900,
        on_click = animate,
    )

    search_container = ft.Container(
        content =  ft.Column(
        controls = [
            ft.Container(
                content = ft.Column(
                    controls = [
                        ft.Text(
                            value = "WEATHERDATA BMKG",
                            font_family = 'josefin_sans',
                            size = 48,
                            text_align = 'center',
                            weight = 'w800'
                        ),
                        ft.Row(
                            controls = [
                                date := ft.Text(
                                    value = dt.now().strftime("%a, %d %b %Y"),
                                    size = 24,
                                    font_family = 'josefin_sans',
                                    weight = 'w600'
                                ),
                                clock := ft.Text(
                                    size = 24,
                                    font_family = 'josefin_sans',
                                    weight = 'w600'
                                )
                            ],
                            alignment = 'center',
                            vertical_alignment = 'center',
                            spacing = 30
                        ),
                        
                    ],
                    alignment = 'center',
                    horizontal_alignment = 'center',                    
                ),
                margin = ft.margin.all(30)
            ),
            ft.Text(
                "Masukkan nama kecamatan di sini",
                font_family = 'playfair',
                size = 24,
                weight = 'bold',
                text_align = ft.TextAlign.CENTER,
                color = ft.colors.BLUE_GREY_900
                ),
            search_query,
            search_option,
            search_button
        ],
        alignment = 'center_top',
        horizontal_alignment = 'stretch'        
        ),
        border_radius = 10,
        padding = ft.padding.symmetric(horizontal = 150, vertical = 50),
        bgcolor = ft.colors.BLUE_GREY_50,
        opacity = 0.5
    )
    
    # Result layer widgets
    result_container = ft.Container()


    # Lower layer widgets    
    animated_layer = ft.AnimatedSwitcher(
        content = search_container,
        transition =  'fade',
        duration = 3000
    )

    foundation = ft.Container(
        content= animated_layer,
        image_src = 'assets/photos/mohammad-alizade-62t_kKa2YlA-unsplash.jpg',
        image_fit = ft.ImageFit.COVER,
        image_opacity = 0.8,
        border_radius = 10,
        alignment = ft.alignment.center,
        shadow = ft.BoxShadow(
            spread_radius = 10,
            blur_radius = 30,
            blur_style = ft.ShadowBlurStyle.NORMAL,            
            offset = ft.Offset(0, 0),
            color = '#222222'
        )
    )   

    base_page = ft.Container(
        content = foundation,
        height = 850,
        width = 1200,
        image_src = 'assets/photos/lukasz-lada-q7z-AUlHPaw-unsplash.png',        
        image_fit = ft.ImageFit.COVER,
        image_opacity = 0.8,
        alignment = ft.alignment.center,
        padding = ft.padding.only(left = 80, top = 80, right = 80, bottom = 100)
    )

    page.add(base_page)

    showtime()


ft.app(target = main, assets_dir= 'assets')