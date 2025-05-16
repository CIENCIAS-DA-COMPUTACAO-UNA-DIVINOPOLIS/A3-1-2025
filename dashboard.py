from nicegui import ui

@ui.page('/dashboard')
def dashboard():
    
    with ui.column().classes("w-full items-center pt-4"):
        ui.label("📚 Sistema da Biblioteca").classes("text-3xl font-bold")
        ui.label("Bem-vindo ao painel de controle").classes("text-lg")
    with ui.column().classes("w-full items-center pt-1"):
        with ui.card().style(' width: 250px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);'):
                with ui.column().classes("w-full items-center pt-1"):
                    with ui.column().classes("w-full items-center pt-4"):
                        ui.button('Cadastrar Usuário', on_click=lambda: ui.navigate.to('/cadastro_usuario'))
                    with ui.column().classes("w-full items-center pt-4"):
                        ui.button('Cadastrar Livro', on_click=lambda: ui.navigate.to('/cad_livros'))
                    with ui.column().classes("w-full items-center pt-4"):
                        ui.button('Registrar Devolução', on_click=lambda: ui.navigate.to('/devolucao'))
                    with ui.column().classes("w-full items-center pt-4"):
                        ui.button('Consulta', on_click=lambda: ui.navigate.to('/consulta'))
