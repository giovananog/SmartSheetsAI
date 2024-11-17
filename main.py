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

# Carregar dados da planilha selecionada
caminho = planilhas[escolha]
try:
    dados = pd.read_csv(caminho)
    st.success(f"Planilha '{escolha}' carregada com sucesso!")
    st.write(f"Exibindo os primeiros dados da planilha **{escolha}**:")
    st.dataframe(dados.head())  # Mostrar os primeiros dados

    # Gráficos específicos para cada planilha
    if escolha == "Estatísticas":
        st.subheader("Gráficos de Estatísticas")
        
        # Escolher tipo de gráfico
        tipo_grafico = st.selectbox(
            "Escolha o tipo de gráfico:",
            ["Chutes por Clube", "Posse de Bola por Clube", "Cartões por Clube"]
        )
        
        if tipo_grafico == "Chutes por Clube":
            fig = px.bar(dados, x="clube", y="chutes", color="clube", title="Chutes por Clube")
            st.plotly_chart(fig)
        
        elif tipo_grafico == "Posse de Bola por Clube":
            fig = px.bar(dados, x="clube", y="posse_de_bola", color="clube", title="Posse de Bola por Clube")
            st.plotly_chart(fig)
        
        elif tipo_grafico == "Cartões por Clube":
            fig = px.bar(dados, x="clube", y="cartao_amarelo", color="clube", title="Cartões Amarelos por Clube")
            st.plotly_chart(fig)
    
    elif escolha == "Gols":
        st.subheader("Gráficos de Gols")
        fig = px.histogram(dados, x="clube", color="clube", title="Distribuição de Gols por Clube")
        st.plotly_chart(fig)
    
    elif escolha == "Cartões":
        st.subheader("Gráficos de Cartões")
        
        # Escolher tipo de gráfico
        tipo_grafico = st.selectbox(
            "Escolha o tipo de gráfico:",
            ["Cartões por Clube", "Cartões por Tipo", "Cartões por Rodada"]
        )
        
        if tipo_grafico == "Cartões por Clube":
            fig = px.bar(dados, x="clube", y="cartao", color="clube", title="Cartões por Clube")
            st.plotly_chart(fig)
        
        elif tipo_grafico == "Cartões por Tipo":
            fig = px.pie(dados, names="cartao", title="Distribuição de Tipos de Cartões")
            st.plotly_chart(fig)
        
        elif tipo_grafico == "Cartões por Rodada":
            fig = px.histogram(dados, x="rodata", y="cartao", color="cartao", title="Cartões por Rodada", barmode="group")
            st.plotly_chart(fig)

    
    elif escolha == "Partidas":
        st.subheader("Gráficos de Partidas")
        
        # Escolher tipo de gráfico
        tipo_grafico = st.selectbox(
            "Escolha o tipo de gráfico:",
            ["Placar por Clube", "Vencedores por Rodada", "Arena Mais Utilizada"]
        )
        
        if tipo_grafico == "Placar por Clube":
            fig = px.bar(dados, x="mandante", y="mandante_Placar", color="mandante", title="Placar por Clube Mandante")
            st.plotly_chart(fig)
        
        elif tipo_grafico == "Vencedores por Rodada":
            fig = px.histogram(dados, x="rodata", y="vencedor", color="vencedor", title="Distribuição de Vencedores por Rodada")
            st.plotly_chart(fig)
        
        elif tipo_grafico == "Arena Mais Utilizada":
            fig = px.bar(dados, y="arena", title="Frequência das Arenas Utilizadas")
            st.plotly_chart(fig)

except Exception as e:
    st.error(f"Erro ao carregar a planilha '{escolha}'. Verifique o arquivo. Detalhes: {e}")
