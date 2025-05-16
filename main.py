from nicegui import ui, app

app.add_static_files('/static', 'static')  # serve a pasta /static
ui.add_head_html('<link rel="stylesheet" href="/static/custom.css">')  # Adiciona o CSS no <head>



# Importa páginas
import paginas.login
import paginas.dashboard
import paginas.cadastro_usuario
import paginas.cad_livros
import paginas.devolucao
import paginas.consulta

ui.run()
