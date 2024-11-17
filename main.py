import streamlit as st
import pandas as pd

# Carregar dados
partidas = pd.read_csv("data/campeonato-brasileiro-full.csv")

# Título do app
st.title("SmartSheetsAI - Football Analysis")

# Filtro por rodada
rodada = st.selectbox("Selecione a rodada", sorted(partidas["rodata"].unique()))

# Exibir dados filtrados
dados_filtrados = partidas[partidas["rodata"] == rodada]
st.write(f"Partidas da Rodada {rodada}")
st.dataframe(dados_filtrados)
