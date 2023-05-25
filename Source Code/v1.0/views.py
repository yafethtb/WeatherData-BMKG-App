import flet as ft
import presenter as pt
from literaldata import ColorPalette as clpt


def main(page: ft.Page):
    page.title = "BMKG WEATHER REPORT APP"
    page.window_width = 1200        
    page.window_height = 800       
    page.window_resizable = False  # Freeze the window size
    page.window_maximizable = False # Remove the maximizable button
    page.bgcolor = clpt.PRIMARY
    page.update()

    # ----------------
    # Button Functions
    # ----------------
    def result(e):
        district = city_list.value
        day = day_list.value

        if all([district, day]):
            result_part.content = pt.show_result(district, day)
            result_header.value = f'PRAKIRAAN CUACA {district}'.upper()
            city_list.error_text = None
            day_list.error_text = None
            user_query.visible = True
            user_query.value = ''
            city_list.visible = False
        else:
            city_list.error_text = 'Pilih sebelum mulai'
            day_list.error_text = 'Pilih sebelum mulai'
            result_part.content = ft.Text(
                        'Nama Kecamatan dan Hari harus terisi.', 
                        style = 'titleMedium',
                        weight = 'w700',
                        size = 72
                    )  
        
        page.update()
            

    def stack_modif(e):
        query = user_query.value.lower()
        if query != '':
            city_list.visible = True
            user_query.visible = False
            city_list.options = pt.populate_city(query)
        else: 
            city_list.visible = False

        page.update()

    def show_query(e):
        user_query.visible = True
        city_list.visible = False
        page.update()        

    # ----------------
    # Header Part
    # ----------------
    header_block = ft.Container(
        content = ft.Text(
        'PRAKIRAAN CUACA BMKG',
        color = clpt.TEXT,
        size = 36,
        style = 'titleLarge',
        weight = 'w900'
        ), 
        bgcolor = clpt.TERTIARY,
        height = 100,
        alignment = ft.alignment.center,            
        padding = ft.padding.all(10),
        border_radius= ft.border_radius.only(top_left = 20, top_right = 20)
    )
    # ----------------
    # Control part
    # ----------------
    city_list = ft.Dropdown(width = 550, 
                            autofocus = True,
                            text_size = 16, 
                            options = [],
                            visible = False,
                            on_change = show_query,
                            helper_text = 'Pilih salah satu dari nama kecamatan berikut', 
                            border_color = clpt.QUARTERNARY,
                            color = clpt.QUARTERNARY  
                            )
    
    user_query = ft.TextField(
        width = 550,
        label = "PILIH KECAMATAN",
        on_submit = stack_modif,        
        border_color = clpt.QUARTERNARY,
        color = clpt.QUARTERNARY                   
    )

    stack_list = ft.Stack(
        controls = [city_list, user_query],
        width = 550        
    )
      
    day_list = ft.Dropdown(width = 150, 
                           label = "PILIH HARI",         
                           label_style = ft.TextStyle(color = clpt.TERTIARY),               
                           text_size = 16, 
                           autofocus = True,
                           options = pt.populate_days(),
                           border_color = clpt.QUARTERNARY,
                           color = clpt.QUARTERNARY                                     
                           )

    submitbtn = ft.ElevatedButton (
        text = "TAMPILKAN CUACA",
        bgcolor = clpt.TERTIARY,
        color = clpt.TEXT,        
        width = 200,
        height = 50,
        on_click = result,    
    )

    control_block = ft.Row(
        controls = [stack_list, day_list, submitbtn],
        alignment = 'spaceAround'
    )
    
    # ----------------
    # Result Part
    # ----------------
    result_header = ft.Text(
        size = 24,
        style = 'titleMedium',
        weight = 'w600',
        color = clpt.TEXT,
        text_align = ft.TextAlign.CENTER        
    )

    result_part = ft.Container(
        content = ft.Text(
            'Data diambil dari situs BMKG (https://www.bmkg.go.id)', 
            style = 'titleMedium',
            weight = 'w700',
            size = 36,
            color = clpt.TEXT
            ),
            height = 450,
            alignment = ft.alignment.center,            
            padding = ft.padding.all(5),
    )

    result_block = ft.Column(
        controls=[
            result_header,
            result_part
        ],
        alignment = 'spaceAround',
        horizontal_alignment = 'stretch',
        spacing = 15
    )

    # ----------------
    # Footer Part
    # ----------------
    footer_block = ft.Row(
        controls = [
            ft.Text('Created by Yafeth T. B (2023)', size = 14, color = clpt.TEXT),
            ft.Text('Data source: https://www.bmkg.go.id', size = 14, color = clpt.TEXT)
        ],
        alignment = 'center',
        vertical_alignment = 'center',
        height = 50
    )

    page.add(header_block, control_block, result_block, footer_block)


ft.app(target=main, assets_dir = 'assets')