from nicegui import ui
import mysql.connector
from mysql.connector import Error
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def conectar():
    return mysql.connector.connect(
        host='metro.proxy.rlwy.net',
        port=25858,
        user='root',
        password='bojFqQXsCRiLKyzbmgsPidyeQLJAVlsE',
        database='railway'
    )

@ui.page('/')
def login_page():
    ui.add_head_html('<link rel="stylesheet" href="/static/custom.css">')

    with ui.element('div').classes('login-container'):
        with ui.element('div').classes('login-box'):
            ui.label('Login').classes('text-2xl mb-4')

            email = ui.input('Email').props('outlined').classes('w-full')

            # Container da linha com campo de senha e ícone
            with ui.row().classes('items-center w-full'):
                # Campo de senha com largura flexível
                senha_input = ui.input('Senha', password=True).props('outlined').classes('flex-grow')

                # Estado mutável para alternar visibilidade
                mostrar_senha = {'ativo': False}

                # Ícone do olho clicável
                #icone = ui.icon('visibility').on('click', lambda: alternar_visibilidade()).classes('cursor-pointer')

                # Função para alternar a senha visível/oculta
                def alternar_visibilidade():
                    mostrar_senha['ativo'] = not mostrar_senha['ativo']
                    senha_input.password = not mostrar_senha['ativo']
                    senha_input.update()
                    #icone.text = 'visibility_off' if mostrar_senha['ativo'] else 'visibility'

            def login():
                try:
                    conn = conectar()
                    cursor = conn.cursor()

                    if email.value == '' or senha_input.value == '':
                        ui.notify('Preencha todos os campos')
                        return

                    cursor.execute('SELECT * FROM usuarios WHERE nome = %s AND senha = %s',
                                   (email.value, senha_input.value))
                    usuario = cursor.fetchone()

                    if usuario:
                        if usuario[9] == 'cliente':
                            ui.notify('Login como cliente')
                            ui.navigate.to('/consulta')
                        else:
                            ui.navigate.to('/dashboard')        
                    else:
                        ui.notify('Login inválido')
                        email.value = ''
                        senha_input.value = ''
                except Error as e:
                    ui.notify(f'Erro no banco: {e}')
                finally:
                    if conn.is_connected():
                        cursor.close()
                        conn.close()

            ui.button('Entrar', on_click=login).classes('mt-4 w-full')
            ui.button('Cadastrar Usuario', on_click=lambda: ui.navigate.to('/cadastro_usuario')).classes('mt-2 w-full')
