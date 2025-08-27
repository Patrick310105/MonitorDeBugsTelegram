# get_id.py
# -*- coding: utf-8 -*-

import configparser
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import UsernameNotOccupiedError

# --- Leitura das Configurações ---
# Lê as mesmas credenciais do seu arquivo 'config.ini'
try:
    config = configparser.ConfigParser()
    config.read('config.ini')

    API_ID = config.getint('telegram', 'api_id')
    API_HASH = config.get('telegram', 'api_hash')
    # Usaremos um nome de sessão diferente para não interferir com o script principal
    SESSION_NAME = 'id_finder_session' 

except Exception as e:
    print(f"Erro ao ler o arquivo 'config.ini'. Verifique se ele existe e está correto. Detalhe: {e}")
    exit()

def get_chat_id():
    """
    Função que conecta ao Telegram e solicita o username de um canal
    para descobrir e exibir seu ID numérico correto.
    """
    # O 'with' garante que a conexão será fechada corretamente no final
    with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        print("Cliente conectado com sucesso!")
        
        # Loop para permitir a consulta de vários IDs sem reiniciar o script
        while True:
            channel_username = input("\nDigite o @username do canal/grupo (ou 'sair' para fechar): ")
            
            if channel_username.lower() == 'sair':
                print("Encerrando a ferramenta.")
                break
            
            try:
                # Remove o '@' se o usuário tiver digitado
                if channel_username.startswith('@'):
                    channel_username = channel_username[1:]

                # Pega a "entidade" (informações do canal) a partir do username
                entity = client.get_entity(channel_username)
                
                # O ID que precisamos para a API é composto por um prefixo '-100'
                # seguido pelo ID base que a biblioteca nos retorna.
                correct_id = int(f"-100{entity.id}")

                print("\n--- ✅ ID Encontrado! ---")
                print(f"Nome do Canal: {entity.title}")
                print(f"Username: @{entity.username}")
                print(f"ID que você deve usar no config.ini: {correct_id}")
                print("------------------------")

            except (UsernameNotOccupiedError, ValueError):
                print(f"ERRO: O username '{channel_username}' não foi encontrado. Verifique se digitou corretamente.")
            except Exception as e:
                print(f"Ocorreu um erro inesperado: {e}")
                break

if __name__ == "__main__":
    get_chat_id()
