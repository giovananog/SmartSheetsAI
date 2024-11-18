import streamlit as st
import pandas as pd
import plotly.express as px
import openai
from dotenv import load_dotenv
import os


class OpenAIHandler:
    def __init__(self):
        load_dotenv()
        st.set_page_config(layout="wide")
        openai.api_key = os.getenv("OPENAI_API_KEY")

    @staticmethod
    def obter_analise(texto_entrada):
        try:
            resposta = openai.Completion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é um assistente que ajuda a analisar dados."},
                    {"role": "user", "content": texto_entrada},
                ]
            )
            return resposta['choices'][0]['message']['content']
        except Exception as e:
            return f"Erro ao fazer a análise: {e}"


class DataHandler:
    @staticmethod
    def carregar_dados(caminho):
        try:
            return pd.read_csv(caminho)
        except Exception as e:
            st.error(f"Erro ao carregar a planilha. Detalhes: {e}")
            return None


class Dashboard:
    def __init__(self, dados, escolha):
        self.dados = dados
        self.escolha = escolha

    def aplicar_filtros(self):
        if self.escolha == "Partidas":
            clube_filtro = st.selectbox("Selecione o Clube:", self.dados["mandante"].unique())
            rodada_filtro = st.slider("Selecione a Rodada:", int(self.dados["rodata"].min()), int(self.dados["rodata"].max()))
            self.dados = self.dados[
                ((self.dados["mandante"] == clube_filtro) | (self.dados["visitante"] == clube_filtro)) &
                (self.dados["rodata"] <= rodada_filtro)
            ]
        elif self.escolha == "Estatísticas":
            clube_filtro = st.selectbox("Selecione o Clube:", self.dados["clube"].unique())
            self.dados = self.dados[self.dados["clube"] == clube_filtro]

    def mostrar_graficos(self):
        if self.escolha == "Estatísticas":
            self._mostrar_graficos_estatisticas()
        elif self.escolha == "Gols":
            self._mostrar_graficos_gols()
        elif self.escolha == "Cartões":
            self._mostrar_graficos_cartoes()
        elif self.escolha == "Partidas":
            self._mostrar_graficos_partidas()

    def _mostrar_graficos_estatisticas(self):
        st.subheader("Gráficos de Estatísticas")
        tipo_grafico = st.selectbox(
            "Escolha o tipo de gráfico:",
            ["Chutes por Clube", "Posse de Bola por Clube", "Cartões por Clube", "Média de Chutes por Rodada"]
        )
        if tipo_grafico == "Chutes por Clube":
            fig = px.bar(self.dados, x="clube", y="chutes", color="clube", title="Chutes por Clube")
            st.plotly_chart(fig)
        elif tipo_grafico == "Posse de Bola por Clube":
            fig = px.bar(self.dados, x="clube", y="posse_de_bola", color="clube", title="Posse de Bola por Clube")
            st.plotly_chart(fig)
        elif tipo_grafico == "Cartões por Clube":
            fig = px.bar(self.dados, x="clube", y="cartao_amarelo", color="clube", title="Cartões Amarelos por Clube")
            st.plotly_chart(fig)
        elif tipo_grafico == "Média de Chutes por Rodada":
            media_chutes = self.dados.groupby("rodata")["chutes"].mean().reset_index()
            fig = px.line(media_chutes, x="rodata", y="chutes", title="Média de Chutes por Rodada")
            st.plotly_chart(fig)

    def _mostrar_graficos_gols(self):
        st.subheader("Gráficos de Gols")
        fig = px.histogram(self.dados, x="clube", color="clube", title="Distribuição de Gols por Clube")
        st.plotly_chart(fig)

    def _mostrar_graficos_cartoes(self):
        st.subheader("Gráficos de Cartões")
        tipo_grafico = st.selectbox(
            "Escolha o tipo de gráfico:",
            ["Cartões por Clube", "Cartões por Tipo", "Cartões por Rodada", "Cartões por Técnico"]
        )
        if tipo_grafico == "Cartões por Clube":
            fig = px.bar(self.dados, x="clube", y="cartao", color="clube", title="Cartões por Clube")
            st.plotly_chart(fig)
        elif tipo_grafico == "Cartões por Tipo":
            fig = px.pie(self.dados, names="cartao", title="Distribuição de Tipos de Cartões")
            st.plotly_chart(fig)
        elif tipo_grafico == "Cartões por Rodada":
            fig = px.histogram(self.dados, x="rodata", y="cartao", color="cartao", title="Cartões por Rodada", barmode="group")
            st.plotly_chart(fig)
        elif tipo_grafico == "Cartões por Técnico":
            fig = px.bar(self.dados, x="tecnico_mandante", y="cartao_amarelo", color="tecnico_mandante", title="Cartões por Técnico")
            st.plotly_chart(fig)

    def _mostrar_graficos_partidas(self):
        st.subheader("Gráficos de Partidas")
        tipo_grafico = st.selectbox(
            "Escolha o tipo de gráfico:",
            ["Placar por Clube", "Vencedores por Rodada", "Arena Mais Utilizada", "Técnico Vencedor"]
        )
        if tipo_grafico == "Placar por Clube":
            fig = px.bar(self.dados, x="mandante", y="mandante_Placar", color="mandante", title="Placar por Clube Mandante")
            st.plotly_chart(fig)
        elif tipo_grafico == "Vencedores por Rodada":
            fig = px.histogram(self.dados, x="rodata", y="vencedor", color="vencedor", title="Distribuição de Vencedores por Rodada")
            st.plotly_chart(fig)
        elif tipo_grafico == "Arena Mais Utilizada":
            fig = px.bar(self.dados, y="arena", title="Frequência das Arenas Utilizadas")
            st.plotly_chart(fig)
        elif tipo_grafico == "Técnico Vencedor":
            fig = px.bar(self.dados, x="tecnico_mandante", y="vencedor", color="tecnico_mandante", title="Técnico Vencedor por Clube")
            st.plotly_chart(fig)


class App:
    def __init__(self):
        self.openai_handler = OpenAIHandler()

    def run(self):
        st.title("SmartSheetsAI - Análise de Planilhas")
        st.write("Bem-vindo! Este app permite analisar dados do Campeonato Brasileiro.")
        planilhas = {
            "Partidas": "data/campeonato-brasileiro-full.csv",
            "Estatísticas": "data/campeonato-brasileiro-estatisticas-full.csv",
            "Gols": "data/campeonato-brasileiro-gols.csv",
            "Cartões": "data/campeonato-brasileiro-cartoes.csv",
        }
        escolha = st.selectbox("Selecione a planilha que deseja analisar:", list(planilhas.keys()))
        caminho = planilhas[escolha]
        dados = DataHandler.carregar_dados(caminho)

        if dados is not None:
            st.success(f"Planilha '{escolha}' carregada com sucesso!")
            st.write(f"Exibindo os primeiros dados da planilha **{escolha}**:")
            st.dataframe(dados.head())

            dashboard = Dashboard(dados, escolha)
            dashboard.aplicar_filtros()
            dashboard.mostrar_graficos()

            st.subheader("Análise com ChatGPT")
            pergunta_chatgpt = st.text_input("O que você gostaria que o ChatGPT analisasse nos dados?")
            if pergunta_chatgpt:
                resposta = self.openai_handler.obter_analise(pergunta_chatgpt)
                st.write(f"Análise do ChatGPT: {resposta}")


if __name__ == "__main__":
    app = App()
    app.run()
