from typing import Dict
import flet as ft
import os


def main(page):
    prog_bars: Dict[str, ft.ProgressRing] = {}
    files = ft.Ref[ft.Column]()
    upload_button = ft.Ref[ft.ElevatedButton]()

    page.adaptive = True

    page.appbar = ft.AppBar(
        leading=ft.TextButton("New", style=ft.ButtonStyle(padding=0)),
        title=ft.Text("Lol"),
        actions=[
            ft.IconButton(ft.cupertino_icons.ADD, style=ft.ButtonStyle(padding=0))
        ],
        bgcolor=ft.Colors.with_opacity(0.04, ft.CupertinoColors.SYSTEM_BACKGROUND),
    )

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.IMAGE_OUTLINED, label="Upload Image"),
            # ft.NavigationBarDestination(
            #    icon=ft.Icons.BOOKMARK_BORDER,
            #    selected_icon=ft.Icons.BOOKMARK,
            #    label="Bookmark",
            #),
        ],
        border=ft.Border(
            top=ft.BorderSide(color=ft.CupertinoColors.SYSTEM_GREY2, width=0)
        ),
    )

    def upload_files(e):
        if file_picker.result and file_picker.result.files:
            os.makedirs("uploads", exist_ok=True)
            for f in file_picker.result.files:
                save_path = os.path.join("uploads", f.name)  # Automatically handles slashes
                with open(f.path, "rb") as src, open(save_path, "wb") as dest:
                    dest.write(src.read())  # Read and write file manually
        page.update()
   
#file_picker = ft.FilePicker(on_result=upload_files)
#page.overlay.append(file_picker)

    def file_picker_result(e: ft.FilePickerResultEvent):
        upload_button.current.disabled = True if e.files is None else False
        prog_bars.clear()
        files.current.controls.clear()
        if e.files is not None:
            for f in e.files:
                prog = ft.ProgressRing(value=0, bgcolor="#eeeeee", width=20, height=20)
                prog_bars[f.name] = prog
                files.current.controls.append(ft.Row([prog, ft.Text(f.name)]))
        page.update()

    def on_upload_progress(e: ft.FilePickerUploadEvent):
        prog_bars[e.file_name].value = e.progress
        prog_bars[e.file_name].update()

    file_picker = ft.FilePicker(
        on_result=file_picker_result, on_upload=on_upload_progress
    )

    # def upload_files(e):
    #     print("what")
    #     uf = []
    #     if file_picker.result is not None and file_picker.result.files is not None:
    #         for f in file_picker.result.files:
    #             uf.append(
    #                 ft.FilePickerUploadFile(
    #                     f.name,
    #                     upload_url=page.get_upload_url(f"uploads/{f.name}", 600),
    #                 )
    #             )
    #         file_picker.upload(uf)

    # hide dialog in a overlay
    page.overlay.append(file_picker)

    page.add(
        ft.SafeArea(
            ft.Column(
                [
                    ft.ElevatedButton(
                        "Select files...",
                        icon=ft.Icons.FOLDER_OPEN,
                        on_click=lambda _: file_picker.pick_files(allow_multiple=True),
                    ),
                    ft.Column(ref=files),
                    ft.ElevatedButton(
                        "Upload",
                        ref=upload_button,
                        icon=ft.Icons.UPLOAD,
                        on_click=upload_files,
                        disabled=True,
                    ),
                    ft.Text("First field:"),
                    ft.TextField(keyboard_type=ft.KeyboardType.TEXT),
                    ft.Text("Text line 1"),
                    ft.Text("Text line 2"),
                ]
            )
        )
    )


ft.app(main, upload_dir="uploads")