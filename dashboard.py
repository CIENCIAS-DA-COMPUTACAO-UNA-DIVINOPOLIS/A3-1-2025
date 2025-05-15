from nicegui import ui

@ui.page('/dashboard')
def dashboard():
    ui.label('Painel Principal')
    ui.button('Cadastrar Usuário', on_click=lambda: ui.navigate.to('/cadastro_usuario'))
    ui.button('Cadastrar Livro', on_click=lambda: ui.navigate.to('/cadastro_livro'))
    ui.button('Registrar Devolução', on_click=lambda: ui.navigate.to('/devolucao'))
    ui.button('Consulta', on_click=lambda: ui.navigate.to('/consulta'))
