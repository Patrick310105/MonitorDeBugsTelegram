Monitor de Ofertas "Bug" no Telegram
Este projeto consiste num programa em Python que se conecta à sua conta do Telegram para monitorizar grupos e canais de promoções. O seu principal objetivo é detetar mensagens que contenham a palavra "Bug" e enviar uma notificação imediata para si, ajudando-o a não perder ofertas raras.
✨ Funcionalidades
* Conexão Segura: Utiliza a biblioteca Telethon para se conectar como um utilizador (userbot) através das credenciais oficiais da API do Telegram.
* Monitorização Seletiva: Permite configurar uma lista específica de grupos e canais que deseja vigiar.
* Deteção por Palavra-chave: Analisa todas as novas mensagens nos chats selecionados em busca da palavra "Bug" (não diferencia maiúsculas de minúsculas).
* Notificações Imediatas: Ao encontrar uma correspondência, envia instantaneamente uma mensagem de alerta para um chat à sua escolha (por exemplo, as suas "Mensagens Salvas").
* Informação Detalhada: A notificação inclui o nome do grupo onde a oferta foi encontrada, o conteúdo original da mensagem e um link direto para a mesma (se o chat for público).
* Ferramenta Auxiliar: Inclui um script para descobrir facilmente o ID numérico de qualquer canal ou grupo público.
🔧 Como Funciona
O programa principal, telegram_bug_monitor.py, estabelece uma conexão persistente com o Telegram. Ele fica "à escuta" de novas mensagens nos chats que você definiu no ficheiro de configuração. Quando uma mensagem chega, o script verifica o seu conteúdo. Se a palavra "Bug" for encontrada, ele formata e envia uma mensagem de alerta para o ID de notificação que você também configurou.
🚀 Guia de Instalação e Utilização
Siga estes passos para configurar e executar o monitor no seu computador Windows.
1. Pré-requisitos
* Python 3.8 ou superior: É necessário ter o Python instalado. Se não o tiver, pode descarregá-lo em python.org. Importante: Durante a instalação, marque a opção "Add Python to PATH".
2. Instalação das Dependências
Abra um terminal (CMD ou PowerShell) e instale a biblioteca Telethon com o seguinte comando:
pip install telethon

3. Obter Credenciais da API do Telegram
Para o programa se conectar à sua conta, precisa de uma api_id e uma api_hash.
1. Aceda a my.telegram.org e inicie sessão com a sua conta.
2. Clique em "API development tools".
3. Preencha o formulário para criar uma nova aplicação (pode usar nomes como "MonitorDeOfertas" e selecionar a plataforma "Desktop").
4. Após a criação, a página mostrará a sua api_id e api_hash. Guarde-as para o próximo passo.
4. Configuração do Projeto
1. Crie uma pasta no seu computador para o projeto (ex: C:\TelegramMonitor).
2. Dentro dessa pasta, crie os três ficheiros do projeto: telegram_bug_monitor.py, config.ini e get_id.py.
3. Abra o ficheiro config.ini e preencha-o com as suas informações:
[telegram]
api_id = 12345678  # Substitua pelo seu api_id
api_hash = abcdefghijklmnopqrstuvwxyz123456  # Substitua pelo seu api_hash
session_name = monitor_bugs

[settings]
# IDs dos grupos/canais a monitorizar, separados por vírgula.
monitored_chat_ids = -100123456789, -100987654321

# ID do chat para onde a notificação será enviada (o seu ID de utilizador).
notification_chat_id = 987654321

5. Descobrir os IDs dos Chats
Para que o programa saiba quais os chats a monitorizar, precisa dos seus IDs numéricos.
Método A: Para Canais/Grupos Públicos (com @username)
Use a ferramenta get_id.py fornecida.
1. No terminal, na pasta do projeto, execute: python get_id.py
2. Quando solicitado, digite o nome de utilizador do canal (ex: @nome_do_canal) e prima Enter.
3. A ferramenta exibirá o ID correto, já formatado (ex: -100123456789). Copie este número.
Método B: Para Grupos Privados (sem @username)
1. Aceda à versão web do Telegram: web.telegram.org/k/.
2. Abra o grupo privado.
3. Observe a URL na barra de endereços do navegador. O número após /# é o ID do grupo (ex: https://web.telegram.org/k/#-1234567890).
Como obter o seu ID de Notificação
Para receber os alertas, precisa do seu próprio ID de utilizador.
1. No Telegram, procure pelo bot @userinfobot.
2. Envie-lhe qualquer mensagem.
3. Ele responderá com o seu ID. Copie este número para o campo notification_chat_id no config.ini.
6. Executar o Monitor
Após configurar tudo, está pronto para iniciar o programa.
1. Abra o terminal na pasta do projeto.
2. Execute o comando:
python telegram_bug_monitor.py

3. Primeira Execução: O programa solicitará o seu número de telefone, um código de confirmação (que chegará no seu Telegram) e a sua senha de verificação de duas etapas (se tiver uma).
4. Após o primeiro login, será criado um ficheiro .session, e os próximos inícios serão automáticos.
O terminal exibirá logs, informando que está a monitorizar os chats. Agora, basta deixá-lo a ser executado em segundo plano.