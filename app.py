import os
import requests
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configurações
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "pt-BR,pt;q=0.9"
}

FURIA_TEAM_ID = 8297  # ID da FURIA no HLTV

# Elenco 2024
FURIA_PLAYERS = {
    "fallen": "2023/fallen",
    "kscerato": "15631/kscerato",
    "yuurih": "12553/yuurih",
    "yekindar": "13915/yekindar",
    "molodoy": "24144/molodoy",
    "sidde": "coach"
}

# --- Funções de Scraping ---
def get_player_stats(player_name):
    """Busca estatísticas individuais"""
    if player_name not in FURIA_PLAYERS:
        return None
    
    if player_name == "sidde":
        return "👔 *sidde* (Técnico da FURIA)\n🔗 https://www.hltv.org/team/8297/furia"

    url = f"https://www.hltv.org/stats/players/{FURIA_PLAYERS[player_name]}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        nickname = soup.find("h1", class_="summaryNickname").text.strip()
        stats = {
            "rating": soup.find("div", text="Rating 2.0").find_next("span").text.strip(),
            "kd": soup.find("div", text="K/D Ratio").find_next("span").text.strip(),
            "headshot": soup.find("div", text="Headshots").find_next("span").text.strip()
        }
        
        return (
            f"🔫 *{nickname}* (FURIA)\n"
            f"⭐ Rating: {stats['rating']}\n"
            f"🎯 HS %: {stats['headshot']}\n"
            f"🔫 K/D: {stats['kd']}\n"
            f"🔗 {url}"
        )
    except Exception as e:
        print(f"Erro ao buscar stats: {e}")
        return f"⚠️ Dados incompletos. Veja o perfil: {url}"

def get_matches(match_type="upcoming"):
    """Busca partidas (próximas ou passadas)"""
    url = f"https://www.hltv.org/team/{FURIA_TEAM_ID}/furia#{'matches' if match_type == 'results' else 'upcoming'}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        matches = []
        container = "upcomingMatches" if match_type == "upcoming" else "results"
        
        for match in soup.find_all("div", class_=f"{container}-container")[:5]:  # Limita a 5 partidas
            teams = match.find_all("div", class_="team")
            team1 = teams[0].text.strip() if len(teams) > 0 else "?"
            team2 = teams[1].text.strip() if len(teams) > 1 else "?"
            
            if match_type == "upcoming":
                time = match.find("div", class_="time").text.strip()
                event = match.find("div", class_="event").text.strip()
                matches.append(f"🆚 {team1} vs {team2}\n⏰ {time} | {event}")
            else:
                score = match.find("div", class_="score").text.strip()
                event = match.find("div", class_="event").text.strip()
                matches.append(f"🆚 {team1} {score} {team2}\n🏆 {event}")
        
        return "\n\n".join(matches) if matches else "Nenhuma partida encontrada."
    except Exception as e:
        print(f"Erro ao buscar partidas: {e}")
        return "⚠️ Erro ao buscar partidas. Tente novamente mais tarde."

# --- Rotas do Flask ---
@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get('Body', '').lower().strip()
    resp = MessagingResponse()
    msg = resp.message()

    # Menu interativo
    if incoming_msg in ["oi", "ola", "menu", "help"]:
        msg.body(
            "🏆 *Bot da FURIA CS2* 🎮\n\n"
            "🔍 Comandos disponíveis:\n"
            "• 'jogadores' - Elenco atual\n"
            "• 'próximos' - Próximas partidas\n"
            "• 'resultados' - Últimos jogos\n"
            "• Nome de jogador (ex: 'fallen')\n\n"
            "📢 Atualizado em: " + datetime.now().strftime("%d/%m/%Y")
        )
    
    # Elenco
    elif "jogadores" in incoming_msg:
        msg.body(
            "👥 *Elenco da FURIA 2024*:\n\n"
            "🛡️ FalleN (Capitão)\n"
            "🔫 KSCERATO\n"
            "🎯 yuurih\n"
            "💥 yekindar\n"
            "🆕 molodoy\n\n"
            "👔 sidde (Técnico)\n\n"
            "🔗 https://www.hltv.org/team/8297/furia"
        )
    
    # Próximas partidas
    elif any(word in incoming_msg for word in ["próximos", "proximos", "calendario"]):
        matches = get_matches("upcoming")
        msg.body(f"📅 *Próximas Partidas da FURIA*:\n\n{matches}")
    
    # Resultados recentes
    elif any(word in incoming_msg for word in ["resultados", "ultimos", "jogos"]):
        matches = get_matches("results")
        msg.body(f"📊 *Últimos Resultados da FURIA*:\n\n{matches}")
    
    # Estatísticas de jogador
    elif any(p in incoming_msg for p in FURIA_PLAYERS):
        player = next((p for p in FURIA_PLAYERS if p in incoming_msg), None)
        stats = get_player_stats(player)
        msg.body(stats if stats else "❌ Jogador não encontrado.")
    
    # Comando não reconhecido
    else:
        msg.body(
            "❌ Comando inválido. Envie:\n"
            "• 'menu' para opções\n"
            "• Nome de jogador (ex: 'fallen')\n"
            "• 'próximos' para ver próximas partidas"
        )

    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)