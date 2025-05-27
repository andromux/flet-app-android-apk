import flet as ft
import time
import threading
from games_data import games

PAGE_SIZE = 10

class ChakielApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "ANDROMUX ORG"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = 10
        self.page.scroll = ft.ScrollMode.AUTO
        self.page.bgcolor = ft.Colors.BLACK

        self.current_index = 0
        self.filtered_games = games[:]

        self.search_field = ft.TextField(
            hint_text="Buscar juego...",
            prefix_icon=ft.Icons.SEARCH,
            on_change=self.reset_and_load,
            border_radius=10,
            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
            color=ft.Colors.WHITE,
            border_color=ft.Colors.BLUE,
        )

        self.game_grid = ft.ResponsiveRow(
            spacing=10,
            run_spacing=10,
            expand=True,
        )

        self.load_more_container = ft.Container()
        self.game_grid.controls.append(self.load_more_container)

        self.setup_appbar()
        self.page.add(
            ft.Column([
                self.search_field,
                ft.Divider(color=ft.Colors.BLUE),
                self.game_grid
            ], expand=True)
        )

        self.reset_and_load()

    def setup_appbar(self):
        # Botones de la barra superior
        help_button = ft.IconButton(
            icon=ft.Icons.HELP_OUTLINE,
            tooltip="Ayuda",
            on_click=lambda e: self.page.launch_url("https://www.andromux.org/"),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                side=ft.BorderSide(1, ft.Colors.BLUE),
                bgcolor=ft.Colors.TRANSPARENT,
                color=ft.Colors.BLUE,
            )
        )

        # Botón de YouTube
        youtube_button = ft.IconButton(
            content=ft.Image(
                src="youtube.png",
                width=24,
                height=24
            ),
            tooltip="YouTube",
            on_click=lambda e: self.page.launch_url("https://www.youtube.com/@andromux"),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                side=ft.BorderSide(1, ft.Colors.BLUE),
                bgcolor=ft.Colors.TRANSPARENT,
            )
        )

        # Botón de TikTok
        tiktok_button = ft.IconButton(
            content=ft.Image(
                src="tiktok.png",
                width=24,
                height=24
            ),
            tooltip="TikTok",
            on_click=lambda e: self.page.launch_url("https://tiktok.com/@andromux"),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                side=ft.BorderSide(1, ft.Colors.BLUE),
                bgcolor=ft.Colors.TRANSPARENT,
            )
        )

        # Botón de PayPal
        paypal_button = ft.IconButton(
            content=ft.Image(
                src="paypal.png",
                width=24,
                height=24
            ),
            tooltip="PayPal",
            on_click=lambda e: self.page.launch_url("https://x.com/andromuxorg"),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                side=ft.BorderSide(1, ft.Colors.BLUE),
                bgcolor=ft.Colors.TRANSPARENT,
            )
        )

        self.page.appbar = ft.AppBar(
            title=ft.Text("Andromux ORG", color=ft.Colors.BLUE),
            bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
            center_title=True,
            actions=[
                help_button,
                youtube_button,
                tiktok_button,
                paypal_button
            ],
        )

    def reset_and_load(self, e=None):
        query = self.search_field.value.lower()
        self.filtered_games = [
            g for g in games
            if query in str(g.get("id", "")).lower()
            or query in g["title"].lower()
            or query in g["platform"].lower()
        ]
        self.current_index = 0
        self.game_grid.controls.clear()
        self.game_grid.controls.append(self.load_more_container)
        self.load_more()

    def load_more(self):
        # Indicador de carga personalizado
        self.load_more_container.content = ft.Container(
            content=ft.Image(
                src="loading.gif",
                width=100,
                height=100,
            ),
            alignment=ft.alignment.center,
        )
        self.load_more_container.update()

        def load_data():
            time.sleep(0.5)
            start = self.current_index
            end = start + PAGE_SIZE
            batch = self.filtered_games[start:end]

            for g in batch:
                card = self.create_game_card(g)
                self.game_grid.controls.insert(-1, card)

            self.current_index += len(batch)

            if self.current_index < len(self.filtered_games):
                self.load_more_container.content = ft.ElevatedButton(
                    text="Cargar más juegos",
                    on_click=lambda e: self.load_more(),
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.BLUE,
                        color=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=10),
                        padding=ft.padding.symmetric(horizontal=20, vertical=10),
                        elevation=5,
                    ),
                    width=float("inf")
                )
            else:
                self.load_more_container.content = None

            self.game_grid.update()

        threading.Thread(target=load_data).start()

    def create_game_card(self, game):
        return ft.Container(
            content=ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Image(
                            src=game["image"],
                            width=150,
                            height=150,
                            fit=ft.ImageFit.COVER,
                            border_radius=10,
                        ),
                        ft.Text(
                            game['title'],
                            weight=ft.FontWeight.BOLD,
                            size=14,
                            text_align=ft.TextAlign.CENTER,
                            color=ft.Colors.WHITE,
                            max_lines=1,
                            overflow=ft.TextOverflow.ELLIPSIS,
                        ),
                        ft.Text(
                            game['platform'],
                            size=12,
                            color=ft.Colors.BLUE,
                            text_align=ft.TextAlign.CENTER
                        ),
                    ],
                    spacing=5,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=10,
                    bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                    border_radius=10,
                    ink=True,
                    on_click=lambda e: self.page.launch_url(game["url"]),
                ),
                elevation=2,
            ),
            col={"xs": 12, "sm": 6, "md": 4, "lg": 3, "xl": 2}
        )

def main(page: ft.Page):
    ChakielApp(page)

ft.app(target=main, assets_dir="assets")
