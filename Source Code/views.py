import flet as ft
import presenter as pt

def main(page: ft.Page):
    page.title = "BMKG WEATHER REPORT APP"
    page.window_width = 1200        
    page.window_height = 800       
    page.window_resizable = False  # Freeze the window size
    page.window_maximizable = False # Remove the maximizable button
    page.bgcolor = '#F6FFDE' # ft.colors.LIME_50    
    page.update()

    # ----------------
    # Button Functions
    # ----------------
    def result(e):
        district = city_list.value
        day = day_list.value

        if all([district, day]):
            result_block.content = pt.show_result(district, day)
            city_list.error_text = None
            day_list.error_text = None
        else:
            city_list.error_text = 'Pilih sebelum mulai'
            day_list.error_text = 'Pilih sebelum mulai'
            result_block.content = ft.Text(
                        'Nama Kecamatan dan Hari harus terisi.', 
                        style = 'titleMedium',
                        weight = 'w700',
                        size = 72
                    )  
            
        city_list.update()
        day_list.update()
        result_block.update()

    # ----------------
    # Header Part
    # ----------------
    header_block = ft.Container(
        content = ft.Text(
        'PRAKIRAAN CUACA BMKG',
        color = '#F6FFDE',
        size = 36,
        style = 'titleLarge',
        weight = 'w900'
        ), 
        bgcolor = '#AAC8A7',
        height = 100,
        alignment = ft.alignment.center,            
        padding = ft.padding.all(10)
    )
    # ----------------
    # Control part
    # ----------------
    city_list = ft.Dropdown(width = 550, 
                            label = "PILIH KECAMATAN",
                            # helper_text = 'Jakarta Pusat - Kota Jakarta Pusat', 
                            autofocus = True,
                            text_size = 16, 
                            options = pt.populate_city(),
                            )
      
    day_list = ft.Dropdown(width = 150, 
                           label = "PILIH HARI",                        
                           text_size = 16, 
                           autofocus = True,
                           options = pt.populate_days()
                           )

    submitbtn = ft.ElevatedButton (
        text = "TAMPILKAN CUACA",
        bgcolor = '#AAC8A7',
        color = '#F6FFDE',        
        width = 200,
        height = 50,
        on_click = result,    
    )

    control_block = ft.Row(
        controls = [city_list, day_list, submitbtn],
        alignment = 'spaceAround'
    )
    
    # ----------------
    # Result Part
    # ----------------
    result_block = ft.Container(
        content = ft.Text(
            'Data diambil dari situs BMKG (https://www.bmkg.go.id)', 
            style = 'titleMedium',
            weight = 'w700',
            size = 36),
            height = 500,
            alignment = ft.alignment.center,            
            padding = ft.padding.all(10)
    )

    # ----------------
    # Footer Part
    # ----------------
    footer_block = ft.Row(
        controls = [
            ft.Text('Created by Yafeth T. B (2023)', size = 14),
            ft.Text('Data source: https://www.bmkg.go.id', size = 14)
        ],
        alignment = 'center',
        vertical_alignment = 'center',
        height = 50
    )

    page.add(header_block, control_block, result_block, footer_block)


ft.app(target=main, assets_dir = 'assets')

