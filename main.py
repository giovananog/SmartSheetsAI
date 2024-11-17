import streamlit as st
import pandas as pd
import plotly.express as px

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
        
        # Se a planilha for "Estatísticas", mostrar gráficos relevantes
        if escolha == "Estatísticas":
            st.subheader("Gráficos de Estatísticas")
            
            # Escolher tipo de gráfico
            tipo_grafico = st.selectbox(
                "Escolha o tipo de gráfico:",
                ["Chutes por Clube", "Posse de Bola por Clube", "Cartões por Clube"]
            )
            
            if tipo_grafico == "Chutes por Clube":
                fig = px.bar(dados, x="Clube", y="Chutes", color="Clube", title="Chutes por Clube")
                st.plotly_chart(fig)
            
            elif tipo_grafico == "Posse de Bola por Clube":
                fig = px.bar(dados, x="Clube", y="Posse de bola", color="Clube", title="Posse de Bola por Clube")
                st.plotly_chart(fig)
            
            elif tipo_grafico == "Cartões por Clube":
                fig = px.bar(dados, x="Clube", y="cartao_amarelo", color="Clube", title="Cartões Amarelos por Clube")
                st.plotly_chart(fig)

        # Outros gráficos para planilhas diferentes podem ser adicionados aqui
        elif escolha == "Gols":
            st.subheader("Gráficos de Gols")
            fig = px.histogram(dados, x="Clube", title="Distribuição de Gols por Clube")
            st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Erro ao carregar a planilha '{escolha}'. Verifique o arquivo. Detalhes: {e}")
