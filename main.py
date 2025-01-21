import flet as ft

class ChatMessage(ft.Row):
    def __init__(self, user_name, text):
        super().__init__()
        self.vertical_alignment = ft.CrossAxisAlignment.START
        self.controls = [
            ft.CircleAvatar(
                content=ft.Text(self.get_initials(user_name)),
                color=ft.Colors.WHITE,
                bgcolor=self.get_avatar_color(user_name),
            ),
            ft.Column(
                [
                    ft.Text(user_name, weight="bold"),
                    ft.Text(text, selectable=True),
                ],
                tight=True,
                spacing=5,
            ),
        ]

    def get_initials(self, user_name: str):
        return user_name[:1].capitalize()

    def get_avatar_color(self, user_name: str):
        colors_lookup = [
            ft.Colors.AMBER,
            ft.Colors.BLUE,
            ft.Colors.BROWN,
            ft.Colors.CYAN,
            ft.Colors.GREEN,
            ft.Colors.INDIGO,
            ft.Colors.LIME,
            ft.Colors.ORANGE,
            ft.Colors.PINK,
            ft.Colors.PURPLE,
            ft.Colors.RED,
            ft.Colors.TEAL,
            ft.Colors.YELLOW,
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]


def main(pagina):
    # Estilo para o chat
    chat = ft.ListView(
        expand=True,
        spacing=10,
        padding=10,
        auto_scroll=True,
    )

    nome_usuario = ft.TextField(
        label="Escreva seu nome",
        border_color=ft.Colors.BLUE_300,
        focused_border_color=ft.Colors.BLUE_500,
        bgcolor=ft.Colors.WHITE,
        color=ft.Colors.BLACK,
    )

    def enviar_mensagem_tunel(mensagem):
        tipo = mensagem["tipo"]
        if tipo == "mensagem":
            chat_message = ChatMessage(
                user_name=mensagem["usuario"],
                text=mensagem["texto"],
            )
            chat.controls.append(chat_message)
        else:
            login_message = ft.Text(
                f"{mensagem['usuario']} entrou no chat",
                size=12,
                italic=True,
                color=ft.Colors.BLACK45,
            )
            chat.controls.append(login_message)
        pagina.update()

    pagina.pubsub.subscribe(enviar_mensagem_tunel)

    def enviar_mensagem(evento):
        pagina.pubsub.send_all({
            "texto": campo_mensagem.value,
            "usuario": nome_usuario.value,
            "tipo": "mensagem",
        })
        campo_mensagem.value = ""
        pagina.update()

    campo_mensagem = ft.TextField(
        label="Digite uma mensagem",
        expand=True,
        on_submit=enviar_mensagem,
    )

    botao_enviar_mensagem = ft.ElevatedButton(
        "Enviar",
        on_click=enviar_mensagem,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.GREEN_500,
        style=ft.ButtonStyle(
            padding=ft.padding.all(15),
            shape=ft.RoundedRectangleBorder(radius=12),
        )
    )

    def entrar_popup(evento):
        pagina.pubsub.send_all({"usuario": nome_usuario.value, "tipo": "entrada"})
        pagina.controls.clear()
        pagina.add(
            ft.Column(
                controls=[
                    chat,
                    ft.Row([campo_mensagem, botao_enviar_mensagem], spacing=10),
                ],
                expand=True,
            )
        )
        popup.open = False
        pagina.update()

    popup = ft.AlertDialog(
        open=False,
        modal=True,
        title=ft.Text(
            "Bem-vindo ao Fletzap",
            size=18,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_700,
            text_align=ft.TextAlign.CENTER,
        ),
        content=nome_usuario,
        bgcolor=ft.Colors.GREY_100,
        actions_alignment=ft.MainAxisAlignment.CENTER,
        actions=[ft.ElevatedButton(
            "Entrar", on_click=entrar_popup,
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.GREEN_500,
            style=ft.ButtonStyle(
                padding=ft.padding.all(15),
                shape=ft.RoundedRectangleBorder(radius=12),
            )
        ,)],
    )

    def entrar_chat(evento):
        pagina.dialog = popup
        popup.open = True
        pagina.update()

    texto = ft.Text(
        "Fletzap",
        size=40,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE_700,
        italic=True,
        text_align=ft.TextAlign.CENTER,
    )

    botao_iniciar = ft.ElevatedButton(
        "Iniciar chat",
        on_click=entrar_chat,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.GREEN_500,
        style=ft.ButtonStyle(
            padding=ft.padding.all(15),
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
    )

    # Layout da tela inicial
    layout_inicial = ft.Column(
        controls=[texto, botao_iniciar],
        alignment=ft.MainAxisAlignment.CENTER,  # Centraliza verticalmente
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centraliza horizontalmente
    )

    # Colocando o layout em um container com expand=True e alinhamento explícito
    pagina.add(
        ft.Container(
            content=layout_inicial,
            expand=True,  # Garante que o Container ocupe todo o espaço disponível
            alignment=ft.Alignment(0, 0),  # Centraliza corretamente o conteúdo (0,0 é o centro)
        )
    )

ft.app(target=main, view=ft.WEB_BROWSER, port=8000)