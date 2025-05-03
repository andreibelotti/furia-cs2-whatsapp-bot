# 🤖 FURIA CS2 WhatsApp Bot

Um chatbot para WhatsApp criado com Flask e Twilio, que fornece informações atualizadas sobre o time de CS2 da FURIA, como estatísticas dos jogadores, próximas partidas e resultados recentes. Os dados são extraídos do site HLTV.org via web scraping.

---

## 📌 Funcionalidades

- 📊 Estatísticas individuais dos jogadores
- 📅 Lista de próximas partidas da FURIA
- 🧾 Últimos resultados dos jogos
- 👥 Elenco atualizado do time
- 🔗 Links diretos para as páginas do HLTV

---

## 🚀 Tecnologias Utilizadas

- Python 3.11+
- Flask
- Twilio API (para WhatsApp)
- BeautifulSoup
- Requests
- dotenv (para variáveis de ambiente)
- Selenium (versão futura com screenshots)
- Web Scraping com HLTV.org

---

## 📷 Comandos Suportados (via WhatsApp)

- `menu`, `oi`, `help` → Mostra o menu de opções
- `jogadores` → Exibe o elenco atual da FURIA
- `próximos`, `proximos`, `calendario` → Mostra as próximas partidas
- `resultados`, `ultimos`, `jogos` → Exibe os resultados mais recentes
- `fallen`, `kscerato`, `yuurih`, `yekindar`, `molodoy`, `sidde` → Estatísticas individuais

---
Crie um ambiente virtual e ative:

bash
python -m venv venv
venv\Scripts\activate  # no Windows
Instale as dependências:

bash
pip install -r requirements.txt
Crie um arquivo .env com suas credenciais da Twilio:

ini
TWILIO_ACCOUNT_SID=SEU_SID
TWILIO_AUTH_TOKEN=SEU_TOKEN
TWILIO_PHONE_NUMBER=SEU_NUMERO_TWILIO

Inicie o servidor Flask:
bash
Copiar
Editar
python app.py
Configure o webhook da Twilio para apontar para http://localhost:5000/webhook.

📌 Observações
A Twilio precisa de uma URL pública para receber mensagens. Use ngrok para testes locais:

bash
ngrok http 5000
O projeto usa scraping do HLTV, que pode mudar seu layout a qualquer momento. Mantenha o código atualizado caso ocorram erros de parsing.

📸 Futuras Melhorias
Enviar screenshots automáticos com Selenium

Reconhecer variações de escrita dos comandos (ex: “kserato”, “molodói”)

Banco de dados para salvar preferências dos usuários

📬 Contato
Desenvolvido por Andrei Belotti.
Entre em contato no LinkedIn ou abra uma issue no repositório.

🧡 Go FURIA!
