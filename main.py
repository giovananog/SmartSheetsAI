import streamlit as st
import pandas as pd
import plotly.express as px
import openai
from dotenv import load_dotenv
import os

# Carregar a chave da API do OpenAI a partir do arquivo .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(layout="wide")

# Função para fazer uma análise do conjunto de dados com ChatGPT
def obter_analise_com_gpt(texto_entrada):
    try:
        resposta = openai.Completion.create(
            model="gpt-3.5-turbo",  
            messages=[
                {"role": "system", "content": "Você é um assistente que ajuda a analisar dados."},
                {"role": "user", "content": texto_entrada}
            ]
        )
        return resposta['choices'][0]['message']['content']
    except Exception as e:
        return f"Erro ao fazer a análise: {e}"


# Título do app
st.title("SmartSheetsAI - Análise de Planilhas")

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

    # Adicionando filtros interativos
    if escolha == "Partidas":
        clube_filtro = st.selectbox("Selecione o Clube:", dados["mandante"].unique())
        rodada_filtro = st.slider("Selecione a Rodada:", int(dados["rodata"].min()), int(dados["rodata"].max()))
        dados = dados[(dados["mandante"] == clube_filtro) | (dados["visitante"] == clube_filtro)]
        dados = dados[dados["rodata"] <= rodada_filtro]

    elif escolha == "Estatísticas":
        clube_filtro = st.selectbox("Selecione o Clube:", dados["clube"].unique())
        dados = dados[dados["clube"] == clube_filtro]

    # Gráficos específicos para cada planilha
    if escolha == "Estatísticas":
        st.subheader("Gráficos de Estatísticas")
        
        # Escolher tipo de gráfico
        tipo_grafico = st.selectbox(
            "Escolha o tipo de gráfico:",
            ["Chutes por Clube", "Posse de Bola por Clube", "Cartões por Clube", "Média de Chutes por Rodada"]
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
        
        elif tipo_grafico == "Média de Chutes por Rodada":
            media_chutes = dados.groupby("rodata")["chutes"].mean().reset_index()
            fig = px.line(media_chutes, x="rodata", y="chutes", title="Média de Chutes por Rodada")
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
            ["Cartões por Clube", "Cartões por Tipo", "Cartões por Rodada", "Cartões por Técnico"]
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

        elif tipo_grafico == "Cartões por Técnico":
            fig = px.bar(dados, x="tecnico_mandante", y="cartao_amarelo", color="tecnico_mandante", title="Cartões por Técnico")
            st.plotly_chart(fig)
    
    elif escolha == "Partidas":
        st.subheader("Gráficos de Partidas")
        
        # Escolher tipo de gráfico
        tipo_grafico = st.selectbox(
            "Escolha o tipo de gráfico:",
            ["Placar por Clube", "Vencedores por Rodada", "Arena Mais Utilizada", "Técnico Vencedor"]
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

        elif tipo_grafico == "Técnico Vencedor":
            fig = px.bar(dados, x="tecnico_mandante", y="vencedor", color="tecnico_mandante", title="Técnico Vencedor por Clube")
            st.plotly_chart(fig)

    # Seção de Análise com ChatGPT
    st.subheader("Análise com ChatGPT")

    # Caixa de texto onde o usuário pode perguntar ao ChatGPT sobre os dados
    pergunta_chatgpt = st.text_input("O que você gostaria que o ChatGPT analisasse nos dados?")

    if pergunta_chatgpt:
        try:
            tipo_analise = "análise geral"  
            analise_resposta = obter_analise_com_gpt(tipo_analise)
            st.write(f"Análise do ChatGPT: {analise_resposta}")
        except Exception as e:
            st.error(f"Erro ao processar a análise com o ChatGPT: {e}")

except Exception as e:
    st.error(f"Erro ao carregar a planilha '{escolha}'. Verifique o arquivo. Detalhes: {e}")
