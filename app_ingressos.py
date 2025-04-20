# Protótipo: App de Ingressos – Austrália (v2 com Streamlit)

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import streamlit as st

# --- PARTE 1: Lista de plataformas locais ---
PLATAFORMAS = {
    'Tixel': 'https://tixel.com/au/music-tickets',
}

# --- PARTE 2: Função para buscar eventos do Tixel ---
def buscar_eventos_tixel():
    url = PLATAFORMAS['Tixel']
    eventos = []
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    for event in soup.find_all('a', class_='event-card'):
        nome_tag = event.find('h3')
        nome = nome_tag.text.strip() if nome_tag else 'Nome não encontrado'
        data_tag = event.find('time')
        data_evento = data_tag['datetime'] if data_tag and 'datetime' in data_tag.attrs else 'Data não encontrada'
        link = 'https://tixel.com' + event['href'] if 'href' in event.attrs else 'Link não encontrado'
        eventos.append({
            'nome': nome,
            'data': data_evento,
            'link': link,
            'plataforma': 'Tixel'
        })
    return eventos

# --- PARTE 3: Simular popularidade ---
def simular_popularidade(eventos):
    for evento in eventos:
        evento['popularidade'] = 'Alta' if 'festival' in evento['nome'].lower() or 'tour' in evento['nome'].lower() else 'Média'
        evento['recomendado'] = evento['popularidade'] == 'Alta'
    return eventos

# --- PARTE 4: Streamlit App ---
st.set_page_config(page_title="Bot de Ingressos – Austrália", layout="wide")
st.title("🎫 Bot de Ingressos – Austrália")
st.markdown("Veja eventos com potencial de revenda na Austrália 🇦🇺")

with st.spinner("🔍 Buscando eventos em Tixel..."):
    eventos_tixel = buscar_eventos_tixel()
    eventos_analise = simular_popularidade(eventos_tixel)
    df = pd.DataFrame(eventos_analise)

st.success("✅ Eventos carregados!")
st.dataframe(df[['nome', 'data', 'popularidade', 'recomendado', 'link']])
