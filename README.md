Visão Geral

O script AppFocus é uma aplicação em Python desenvolvida para monitorar e manter em foco uma janela específica de um aplicativo no Windows. Ele utiliza bibliotecas como psutil, pywinauto, pystray e PIL para realizar as seguintes funções:

Monitorar continuamente se a janela de um aplicativo especificado está em foco.
Trazer automaticamente a janela para o foco caso ela não esteja visível.
Permitir pausar e retomar a execução do monitoramento através de um ícone na bandeja do sistema.

Pré-requisitos
Python 3.x instalado.

Pacotes necessários instalados via pip:

pip install psutil pywinauto pystray Pillow

Configuração

Arquivo de Configuração (config.ini):

O script utiliza um arquivo de configuração config.ini para definir o nome do executável do aplicativo e o título da janela que deve ser monitorada.
Se o arquivo config.ini não existir, ele será criado automaticamente com configurações padrão.
Estrutura do Arquivo de Configuração:

[Settings]
executable = nome_do_executavel.exe
window_title = Título da Janela

executable: Nome do executável do aplicativo que será monitorado.
window_title: Título da janela específica do aplicativo.

Funcionalidades

Monitoramento Contínuo:

O script verifica periodicamente se o arquivo de configuração foi modificado e recarrega as configurações se necessário.
Verifica se o processo do aplicativo está em execução e traz a janela para foco caso necessário.
Ícone de Bandeja:

Um ícone na bandeja do sistema é exibido, permitindo pausar/resumir o monitoramento e sair do aplicativo.
O ícone pode ser personalizado substituindo o arquivo icon.png na mesma pasta do script.
Execução
Para executar o script:

python AppFocus.py

O monitoramento do aplicativo será iniciado em uma thread separada.
O ícone de bandeja será configurado e permanecerá ativo enquanto o script estiver em execução.

Logs

Os eventos são registrados no arquivo de log app_focus.log na mesma pasta do script.
Os logs incluem informações sobre a execução do monitoramento, erros encontrados e eventos de pausa/resume.
