import streamlit as st
import requests

# Usa secrets do Streamlit para proteger a chave
API_HOST = "tennis-api-atp-wta-itf.p.rapidapi.com"
API_KEY = st.secrets["RAPIDAPI_KEY"]

HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": API_HOST
}

def buscar_jogador(nome):
    url = f"https://{API_HOST}/players"
    params = {"name": nome}
    response = requests.get(url, headers=HEADERS, params=params)
    return response.json()

def partidas_do_jogador(player_id):
    url = f"https://{API_HOST}/player-matches"
    params = {"id": player_id}
    response = requests.get(url, headers=HEADERS, params=params)
    return response.json()

def buscar_torneios(ano, nivel="ATP"):
    url = f"https://{API_HOST}/tournaments"
    params = {"year": ano, "level": nivel}
    response = requests.get(url, headers=HEADERS, params=params)
    return response.json()

st.title("🎾 Explorador de Tênis Profissional")

aba = st.sidebar.selectbox("Escolha uma opção:", ["Buscar Jogador", "Buscar Torneios"])

if aba == "Buscar Jogador":
    nome = st.text_input("Digite o nome do jogador:")
    if nome:
        dados = buscar_jogador(nome)
        if dados and dados.get("players"):
            jogador = dados["players"][0]
            st.subheader(jogador["name"])
            st.write(f"País: {jogador.get('country')}")
            st.write(f"Ranking Atual: {jogador.get('ranking')}")
            st.write(f"Idade: {jogador.get('age')}")
            st.write(f"Altura: {jogador.get('height')} cm")

            with st.expander("Ver partidas recentes"):
                partidas = partidas_do_jogador(jogador["id"])
                for partida in partidas.get("matches", [])[:5]:
                    st.markdown(f"- **{partida['tournament']}** - {partida['round']} - {partida['result']}")
        else:
            st.warning("Jogador não encontrado.")

elif aba == "Buscar Torneios":
    ano = st.number_input("Ano", min_value=2000, max_value=2025, value=2024)
    nivel = st.selectbox("Nível", ["ATP", "WTA", "ITF"])
    if st.button("Buscar"):
        dados = buscar_torneios(ano, nivel)
        if dados.get("tournaments"):
            for torneio in dados["tournaments"][:10]:
                st.markdown(f"🏟️ **{torneio['name']}** - {torneio['city']}, {torneio['country']} - {torneio['start_date']} a {torneio['end_date']}")
        else:
            st.warning("Nenhum torneio encontrado.")
