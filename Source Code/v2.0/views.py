import flet as ft
from presenter import *
from datetime import datetime as dt
from time import sleep

def main(page: ft.Page):
    #------------
    # Page initialization
    #------------
    page.title = 'WeatherData BMKG 2.0'
    page.window_width = 1200
    page.window_height = 850
    page.window_maximizable = False
    page.window_resizable = False
    page.fonts = {
        'josefin_sans': '/fonts/JosefinSans-Regular.ttf',
        'work_sans': '/fonts/WorkSans-Regular.ttf',
        'volkorn': '/fonts/VollkornSC-Black.ttf',
        'outfit': '/fonts/Outfit-Thin.ttf'
    }
    page.update()
    #------------
    # functions
    #------------
    time_ui = periodic_ui()

    def showtime():
        while True:
            result_clock.value = dt.now().strftime("%H:%M:%S")
            page.update()
            sleep(1)

    def show_dropdown(e):
        if search_query.value != '':
            search_option.visible = True
            search_option.options = populate_city(search_query.value) 
        else:
            search_option.visible = False
        
        search_container.update()

    def open_result(e):
        option_value = search_option.value        
        query_value = search_query.value

        if all([option_value, query_value]):
            focus_data, tabs = view_data(
                option_value, 
                time_ui.color.result_main_text_color,
                'josefin_sans',
                'outfit',
                1
            )

            focus_data.scale = 1.5
            bottom_info.content = tabs
            district_name.value = option_value
            left_widget.content = focus_data

            front_layer.content = result_container
           
        else:
            search_query.error_text = "Mohon mengisi kolom ini"
            search_option.error_text = "Mohon memilih salah satu pilihan"
        page.update()

    def open_search(e):
        search_query.error_text = None
        search_option.error_text = None
        search_query.value = None
        search_option.value = None
        search_option.visible = False
        front_layer.content = search_container
        page.update()
    #------------
    # Search layer widgets
    #------------
    search_query = ft.TextField(
        text_style = ft.TextStyle(
            font_family = 'work_sans',
            color = 'black',
            weight = 'w600'
        ),
        on_change = show_dropdown,
    )

    search_option = ft.Dropdown(
        options = [],
        visible= False,
        )
    
    search_button = ft.IconButton(
        icon = ft.icons.MANAGE_SEARCH_OUTLINED,
        icon_size = 40,
        icon_color = ft.colors.BLUE_GREY_900,
        on_click = open_result,
    )

    queries = ft.Column(
        controls = [
            search_query,
            search_option,
            search_button
        ],
        alignment = 'start',
        horizontal_alignment = 'center',
        spacing = 15,
        expand = 4
    )

    search_container = ft.Container(
        content =  ft.Column(
            controls = [
                ft.Container(
                    content = ft.Column(
                        controls = [
                            ft.Image(
                                src = 'assets/logo.svg',
                                color = time_ui.color.main_text_color,
                                height = 100,
                                width = 267
                            ),
                            ft.Text(
                                value = time_ui.message,
                                font_family = 'volkorn',
                                size = 36,
                                text_align = 'justify',
                                weight = 'w500',
                                color = time_ui.color.main_text_color,
                                opacity = 1
                            )                        
                        ],
                        alignment = 'start',
                        horizontal_alignment = 'center',
                        spacing = 20           
                    ),
                    padding = ft.padding.all(20),
                    expand = 3
                ),
                ft.Text(
                    "Untuk melihat prakiraan cuaca, \nmasukkan nama kecamatan di sini:",
                    size = 20,
                    weight = 'w600',
                    text_align = ft.TextAlign.CENTER,
                    color = time_ui.color.secondary_text_color,
                    font_family = 'work_sans' 
                    ),
                queries,         
                
            ],
            alignment = 'center_top',
            horizontal_alignment = 'stretch'        
        ),
        border_radius = 10,
        padding = ft.padding.symmetric(horizontal = 150, vertical = 25),
        bgcolor = ft.colors.with_opacity(0.8,time_ui.color.result_container_bg_color)
    )
    #------------
    # Result layer widgets
    #------------
    left_widget = ft.Container(
        bgcolor = ft.colors.with_opacity(0.85, time_ui.color.result_container_bg_color),
        padding = ft.padding.all(30),
        width = 300,        
        opacity = 0.8,
        border_radius = ft.border_radius.all(15),
        shadow = ft.BoxShadow(
            spread_radius = 5,
            blur_radius = 20,
            blur_style = ft.ShadowBlurStyle.NORMAL,            
            offset = ft.Offset(0, 0),
            color = '#141e3c'
        ) 
    )

    right_widget = ft.Container(
        content = ft.Column(
            controls = [
                ft.Text(
                    value = dt.now().strftime("%a, %d %b %Y"),
                    size = 36,
                    weight = 'w600',
                    text_align = ft.TextAlign.RIGHT,
                    color = time_ui.color.secondary_text_color,
                    font_family = 'josefin_sans',
                    bgcolor = time_ui.color.result_container_bg_color
                ),                
                result_clock := ft.Text(
                    size = 36,
                    weight = 'w300',
                    text_align = ft.TextAlign.RIGHT,
                    color = time_ui.color.secondary_text_color,
                    font_family = 'work_sans',
                    bgcolor = time_ui.color.result_container_bg_color
                ),
                district_name := ft.Text(
                    size = 18,
                    weight = 'w300',
                    text_align = ft.TextAlign.RIGHT,
                    color = time_ui.color.main_text_color,
                    font_family = 'work_sans',
                    bgcolor = time_ui.color.result_container_bg_color
                ) ,
                ft.Container(
                    content = ft.Image(
                        src = 'assets/arrow-right-square-svgrepo-com.svg',
                        width = 100,
                        height = 100,
                        color = time_ui.color.result_container_bg_color,
                        tooltip = 'Kembali ke pencarian'
                    ),   
                    alignment = ft.alignment.center,
                    bgcolor = ft.colors.TRANSPARENT,
                    on_click = open_search
                )
            ],
            alignment = 'start',
            horizontal_alignment = 'end'
        ),
        alignment = ft.alignment.top_right,
        padding = ft.padding.all(20),
        margin = ft.margin.all(20),
    )

    top_info = ft.Container(
        content = ft.Row(
            controls = [
                left_widget,
                right_widget
            ],
            alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing = 20
        ),
        expand = 6,
        alignment = ft.alignment.top_center,
        padding = ft.padding.all(20),
        bgcolor = ft.colors.TRANSPARENT
    )

    bottom_info = ft.Container(
        content = None,
        expand = 4,
        bgcolor = ft.colors.with_opacity(0.85, time_ui.color.result_container_bg_color),
        opacity = 0.8,
        shadow = ft.BoxShadow(
            spread_radius = 5,
            blur_radius = 20,
            blur_style = ft.ShadowBlurStyle.NORMAL,            
            offset = ft.Offset(0, 0),
            color = '#141e3c'
        )   
    )    

    result_container = ft.Container(
        content = ft.Column(
            controls = [top_info, bottom_info],
            alignment = 'center',
        ),
        border_radius = 20,
    )

    #------------
    # Base Page
    #------------    
    front_layer = ft.Container(
        content = search_container,
        expand = True
    )

    front_page = ft.Container(
        expand= 15,
        content= front_layer,
        image_src = time_ui.fg_image,
        image_fit = ft.ImageFit.COVER,
        image_opacity = 0.8,
        border_radius = 20,
        alignment = ft.alignment.center,
        shadow = ft.BoxShadow(
            spread_radius = 10,
            blur_radius = 30,
            blur_style = ft.ShadowBlurStyle.NORMAL,            
            offset = ft.Offset(0, 0),
            color = '#222222'
        )        
    )
    
    created_by = ft.Text(
        value = "App version 2.0.1   Data source from BMKG (https://www.bmkg.go.id).     Created by Yafeth (2023).",
        color = 'white',
        size = 14,
        font_family = 'work_sans',
        weight = 'w200',
        expand = 1
    )

    front = ft.Column(
        controls = [front_page, created_by],
        horizontal_alignment = 'center'
    )
    #------------
    # Base Page
    #------------
    base_page = ft.Container(
        content = front,
        height = 850,
        width = 1200,      
        image_src = time_ui.bg_image,        
        image_fit = ft.ImageFit.COVER,
        image_opacity = 0.9,
        alignment = ft.alignment.center,
        padding = ft.padding.only(left = 80, top = 80, right = 80, bottom = 100)
    )
    #------------
    # Assembling
    #------------
    page.add(base_page)

    showtime()

if __name__  == "__main__":
    ft.app(target = main, assets_dir= 'assets')