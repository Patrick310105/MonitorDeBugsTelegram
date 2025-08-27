# telegram_bug_monitor.py
# -*- coding: utf-8 -*-

import configparser
import logging
from telethon import TelegramClient, events
import asyncio

# --- Configuração de Logs ---
# Configura o sistema de logs para exibir informações úteis no console.
logging.basicConfig(
    format='[%(levelname)s/%(asctime)s] %(name)s: %(message)s',
    level=logging.INFO
)
log = logging.getLogger(__name__)

# --- Leitura das Configurações ---
# Lê as configurações do arquivo 'config.ini' para não expor dados sensíveis no código.
try:
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Credenciais da API do Telegram
    API_ID = config.getint('telegram', 'api_id')
    API_HASH = config.get('telegram', 'api_hash')
    SESSION_NAME = config.get('telegram', 'session_name', fallback='monitor_bugs')

    # IDs dos canais/grupos a serem monitorados
    # Os IDs devem ser separados por vírgula no arquivo de configuração
    MONITORED_CHATS_INPUT = config.get('settings', 'monitored_chat_ids')
    MONITORED_CHAT_IDS = {int(chat_id.strip()) for chat_id in MONITORED_CHATS_INPUT.split(',')}

    # ID do chat para onde as notificações serão enviadas (pode ser seu user_id ou de um bot)
    NOTIFICATION_CHAT_ID = config.getint('settings', 'notification_chat_id')

except (configparser.NoSectionError, configparser.NoOptionError, ValueError) as e:
    log.error(f"Erro ao ler o arquivo 'config.ini'. Verifique se ele está no formato correto. Detalhe: {e}")
    exit()


async def main():
    """
    Função principal que inicializa o cliente do Telegram,
    define o manipulador de eventos e mantém o programa rodando.
    """
    log.info("Iniciando o monitor de ofertas 'Bug'...")

    # Inicializa o cliente do Telegram com suas credenciais.
    # A primeira vez que rodar, ele pedirá seu número de telefone, código e senha 2FA (se tiver).
    # Depois, criará um arquivo de sessão (ex: monitor_bugs.session) para logins automáticos.
    async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        log.info("Cliente do Telegram conectado com sucesso!")
        me = await client.get_me()
        log.info(f"Logado como: {me.first_name} (ID: {me.id})")

        # --- Manipulador de Eventos para Novas Mensagens ---
        @client.on(events.NewMessage(chats=MONITORED_CHAT_IDS))
        async def bug_detector_handler(event):
            """
            Esta função é chamada automaticamente pela Telethon sempre que uma
            nova mensagem chega em um dos chats monitorados.
            """
            message = event.message
            chat = await event.get_chat()
            chat_title = getattr(chat, 'title', 'Chat Privado')

            log.info(f"Nova mensagem recebida no grupo '{chat_title}' (ID: {event.chat_id})")

            # Verifica se a palavra "bug" (case-insensitive) está no texto da mensagem
            if message.text and 'bug' in message.text.lower():
                log.warning(f"Palavra 'Bug' detectada na mensagem! ID da Mensagem: {message.id}")

                # Monta o link da mensagem (funciona em grupos/canais públicos)
                if getattr(chat, 'username', None):
                    message_link = f"https://t.me/{chat.username}/{message.id}"
                else:
                    # Para chats privados, o link direto é mais complexo, então enviamos um aviso
                    message_link = "Link não disponível (chat privado)"

                # Formata a notificação a ser enviada
                notification_message = (
                    f"🚨 **Oferta BUG detectada!** 🚨\n\n"
                    f"**Grupo/Canal:** {chat_title}\n"
                    f"**Link da Mensagem:** {message_link}\n\n"
                    f"--- CONTEÚDO ORIGINAL ---\n"
                    f"{message.text}"
                )

                try:
                    # Envia a notificação para o seu chat privado ou bot
                    # A vibração tripla não é controlável via API do Telegram.
                    # A notificação chegará com a vibração padrão do seu app.
                    # Para vibração customizada, veja as notas sobre Pushbullet/Pushover.
                    await client.send_message(NOTIFICATION_CHAT_ID, notification_message, link_preview=False)
                    log.info(f"Notificação de BUG enviada com sucesso para o chat ID {NOTIFICATION_CHAT_ID}.")

                except Exception as e:
                    log.error(f"Falha ao enviar a notificação: {e}")

        log.info(f"Monitorando {len(MONITORED_CHAT_IDS)} chats. Aguardando novas mensagens...")
        # Mantém o programa rodando indefinidamente para escutar por novas mensagens.
        await client.run_until_disconnected()

if __name__ == "__main__":
    # Executa a função principal usando o loop de eventos do asyncio.
    asyncio.run(main())
