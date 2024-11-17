import streamlit as st
import pandas as pd

# Título do app
st.title("SmartSheetsAI - Análise de Futebol")

# Descrição do projeto
st.write("Bem-vindo! Este app permite analisar dados do Campeonato Brasileiro. Escolha uma planilha para começar:")

# Opções de planilhas
planilhas = {
    "Partidas": "data/campeonato-brasileiro-full.csv",
    "Estatísticas": "data/campeonato-brasileiro-estatisticas-full.csv",
    "Gols": "data/campeonato-brasileiro-gols.csv",
    "Cartões": "data/campeonato-brasileiro-cartoes.csv"
}

# Dropdown para selecionar a planilha
escolha = st.selectbox("Selecione a planilha que deseja analisar:", list(planilhas.keys()))

# Botão para carregar a planilha
if st.button("Carregar Planilha"):
    caminho = planilhas[escolha]  # Caminho do arquivo escolhido
    try:
        # Carregar dados com pandas
        dados = pd.read_csv(caminho)
        st.success(f"Planilha '{escolha}' carregada com sucesso!")
        st.write(f"Exibindo os primeiros dados da planilha **{escolha}**:")
        st.dataframe(dados.head())  # Mostrar os primeiros dados
    except Exception as e:
        st.error(f"Erro ao carregar a planilha '{escolha}'. Verifique o arquivo. Detalhes: {e}")
