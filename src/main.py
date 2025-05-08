from shape_detect import select_and_run
import flet as ft
import os


def main(page):
    files = ft.Ref[ft.Column]()
    upload_button = ft.Ref[ft.ElevatedButton]()
    image_folder = "processed"  # Local directory containing images
    image_files = [f for f in os.listdir(image_folder) if f.endswith((".png", ".jpg", ".jpeg"))]
    gif_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ubec", "komorebi.gif"))

    page.adaptive = True
    page.scroll = ft.ScrollMode.ALWAYS

    page.bgcolor = "#2C1810"
    page.appbar = ft.AppBar(
        #leading=ft.TextButton("New", style=ft.ButtonStyle(padding=0,color="#FFD700")),
        bgcolor="#4B371C",
        title=ft.Text("༄˖°.🍂.ೃ࿔*:･ [ OtherTongue ] ༄˖°.🍂.ೃ࿔*:･", color="#FFD700"), center_title=True,
        #actions=[
        #    ft.IconButton(ft.cupertino_icons.ADD, style=ft.ButtonStyle(padding=0, color="#FFD700"))
        #],
        #bgcolor=ft.Colors.with_opacity(0.04, ft.CupertinoColors.SYSTEM_BACKGROUND),
    )
    
    counter = 0
    def select_callback(e):
        nonlocal counter
        counter += 1
        select_and_run(counter)
        g.src = f"processed/UNIQoutput{counter}.jpg"
        page.update()
    g = ft.Image(src=f"processed/UNIQoutput{counter}.jpg",
                width=page.width * 0.8,
                height=page.height * 0.8,
                expand=True,
                fit=ft.ImageFit.CONTAIN,
                opacity=1,
                animate_opacity=1000,
                )

    def change_content(e):
        page.controls.clear()
        

        if e == "default":
            nav_dest = 0
        else:
            nav_dest = e.control.selected_index

        if nav_dest == 0:
            nav_content = ft.Container(
                content=ft.Stack([
                    ft.Container(
                        content=ft.Image(
                            src=gif_path,
                            width=page.width,
                            height=page.height,
                            fit=ft.ImageFit.COVER,
                            opacity=0.2,
                        ),
                        width=page.width,
                        height=page.height,
                        gradient=ft.LinearGradient(  # Move gradient here instead
                            begin=ft.alignment.top_center,
                            end=ft.alignment.bottom_center,
                            colors=[
                                ft.colors.with_opacity(0.15, ft.colors.BROWN),
                                ft.colors.with_opacity(0.1, ft.colors.ORANGE),
                            ],
                        ),
                    ),
                    ft.Column([
                        ft.ElevatedButton(
                            text="Upload Image",
                            icon=ft.Icons.IMAGE_OUTLINED,
                            icon_color="#FFD700",
                            on_click=select_callback,
                            style=ft.ButtonStyle(
                                color="#FFD700",
                                bgcolor="#2E1503",
                                shadow_color="#DAA520",
                                surface_tint_color="#FFD700",
                                padding=ft.padding.only(left=10, top=10),
                            ),
                        ),
                        ft.Container(content=g, alignment=ft.alignment.center),
                    ], alignment=ft.alignment.top_left),
                ])
            )

            page.add(nav_content)
            page.update()

        if nav_dest == 1:
            nav_content = ft.Container(
                content=ft.GridView(
                    runs_count=2,  # Number of columns
                    child_aspect_ratio=1.0,
                    spacing=10,
                    run_spacing=10,
                    expand=True,
                    auto_scroll=True,
                    controls=[
                        ft.Image(src=os.path.join(image_folder, img), width=150, height=150)
                        for img in image_files
                    ]
                )
            )
            page.add(nav_content)
            page.update()

    page.navigation_bar = ft.NavigationBar(
        on_change=change_content,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.IMAGE_OUTLINED, label="Upload Image", bgcolor="#D2691E", visible=False),
            ft.NavigationBarDestination(
                icon=ft.Icons.BROWSE_GALLERY_OUTLINED,
                label="Translated",
            ),
        ],
        border=ft.Border(
            top=ft.BorderSide(color=ft.CupertinoColors.SYSTEM_GREY2, width=0)
        ),
        height=65,
        bgcolor="#4B371C",
        surface_tint_color="#FFD700",
        selected_index=0,
        # border=ft.Border(
        #     top=ft.BorderSide(color="#4B371C", width=0)
        # ),
    )

    def synthetic_event(page: ft.Page, control: ft.NavigationBar):
        """Calls the control's event handler"""
        if control.on_change:
            control.on_change(
                ft.ControlEvent(
                target=control.uid,
                name="change",
                data=str(control.selected_index),
                control=control,
                page=page
            )
        )

    # Manually trigger synthetic event if needed
    synthetic_event(page, page.navigation_bar)
    # call the did_mount() once manually if you mess up the order of page.update()
    # page.navigation_bar.did_mount()
    page.update()

ft.app(main)