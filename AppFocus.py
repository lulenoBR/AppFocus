import configparser
import time
import psutil
from pywinauto.application import Application
from pywinauto.findwindows import find_window, ElementNotFoundError
import os
import logging
import pystray
from pystray import MenuItem as item
from PIL import Image
import threading

# Configuração do logging
log_filename = 'app_focus.log'
logging.basicConfig(filename=log_filename, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Caminho do arquivo de configuração
config_path = 'config.ini'

# Configurações padrão
DEFAULT_CONFIG = {
    'Settings': {
        'executable': 'nome_do_executavel.exe',
        'window_title': 'Título da Janela'
    }
}

# Variável global para pausar/despausar o loop
is_paused = False

def load_config():
    if not os.path.exists(config_path):
        create_default_config()
    
    config = configparser.ConfigParser()
    config.read(config_path, encoding='utf-8')  # Especifica a codificação UTF-8 para ler o arquivo
    executable_name = config['Settings']['executable']
    window_title = config['Settings']['window_title']
    return executable_name, window_title

def create_default_config():
    config = configparser.ConfigParser()
    config['Settings'] = {
        'executable': DEFAULT_CONFIG['Settings']['executable'],
        'window_title': DEFAULT_CONFIG['Settings']['window_title']
    }

    with open(config_path, 'w', encoding='utf-8') as configfile:
        config.write(configfile)
        logging.info(f"Arquivo de configuração '{config_path}' criado com configurações padrão.")

def get_process_by_name(name):
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'].lower() == name.lower():
            return process
    return None

def is_window_active(window_title):
    try:
        handle = find_window(title=window_title)
        if handle:
            app = Application().connect(handle=handle)
            window = app.window(handle=handle)
            return window.is_active()
        return False
    except ElementNotFoundError:
        return False
    except Exception as e:
        logging.error(f"Erro ao verificar se a janela está ativa: {e}")
        return False

def bring_window_to_front(window_title):
    try:
        if not is_window_active(window_title):
            handle = find_window(title=window_title)
            app = Application().connect(handle=handle)
            window = app.window(handle=handle)
            if window.is_minimized():
                window.restore()
            window.set_focus()
            return True
        else:
            logging.info(f"Janela '{window_title}' já está em foco.")
            return True
    except ElementNotFoundError:
        logging.error(f"Janela com título '{window_title}' não encontrada.")
    except Exception as e:
        logging.error(f"Erro ao trazer a janela para frente: {e}")
    return False

def monitor_application():
    global is_paused
    executable_name, window_title = load_config()
    last_modified_time = os.path.getmtime(config_path)

    while True:
        if not is_paused:
            # Verifica se o arquivo de configuração foi modificado
            current_modified_time = os.path.getmtime(config_path)
            if current_modified_time != last_modified_time:
                logging.info("Arquivo de configuração modificado. Recarregando configurações...")
                executable_name, window_title = load_config()
                last_modified_time = current_modified_time

            # Verifica se o processo está em execução
            process = get_process_by_name(executable_name)
            if process:
                # Tenta trazer a janela da aplicação para frente
                success = bring_window_to_front(window_title)
                if not success:
                    logging.warning(f"Janela com título '{window_title}' não encontrada.")
            else:
                logging.error(f"Processo '{executable_name}' não encontrado.")
        
        # Aguarda 1 segundo antes de verificar novamente
        time.sleep(1)

def on_quit(icon, item):
    icon.stop()

def on_pause_resume(icon, item):
    global is_paused
    is_paused = not is_paused
    if is_paused:
        icon.update_menu()
        logging.info("Aplicativo pausado.")
    else:
        icon.update_menu()
        logging.info("Aplicativo despausado.")

def create_image():
    # Crie ou carregue uma imagem para o ícone
    image = Image.open("icon.png")  # Substitua por seu próprio ícone
    return image

def setup_tray_icon():
    menu = (item('Pause/Resume', on_pause_resume), item('Quit', on_quit))
    icon = pystray.Icon("AppFocus", create_image(), "App Focus", menu)
    icon.run()

if __name__ == "__main__":
    # Iniciar o monitoramento do aplicativo em uma thread separada
    monitor_thread = threading.Thread(target=monitor_application)
    monitor_thread.daemon = True
    monitor_thread.start()

    # Configurar e executar o ícone de bandeja
    setup_tray_icon()
