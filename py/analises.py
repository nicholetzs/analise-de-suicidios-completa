import os
import pandas as pd
import plotly.express as px
import plotly.io as pio
from flask import Flask, render_template

app = Flask(__name__)


def ler_arquivo_csv(nome_arquivo):
    """
    Função para ler o arquivo CSV e retornar um DataFrame com os dados.
    """
    caminho = os.path.join(os.getcwd(), 'data', nome_arquivo)
    if not os.path.exists(caminho):
        print(f"Arquivo {nome_arquivo} não encontrado! Caminho: {caminho}")
        return None
    df = pd.read_csv(caminho)
    return df


def criar_grafico_ocorrencias_por_ano():
    """
    Função para criar um gráfico de barras sobre a distribuição de ocorrências por ano e retornar o HTML.
    """
    # Chama a função para ler o arquivo CSV
    dados = ler_arquivo_csv("cleaned_result.csv")
    if dados is None:
        return "<p>Erro ao carregar os dados.</p>"

    # Agrupa os dados por ano e conta a quantidade de ocorrências
    dados_agrupados = dados.groupby(
        "ANO")["CONTAGEM"].sum().reset_index(name='total_ocorrencias')

    # Cria o gráfico de barras
    fig = px.bar(
        dados_agrupados,
        x="ANO",
        y="total_ocorrencias",
        color_discrete_sequence=['#4B0082']
    )

    # Estilo e configuração do gráfico
    fig.update_layout(
        # Cor de fundo do gráfico (azul escuro)
        plot_bgcolor='rgba(18,18,30,1)',
        # Cor de fundo do "papel" (preto-azulado)
        paper_bgcolor='rgba(10,10,25,1)',
        font=dict(
            family="Arial",                     # Fonte do texto
            size=12,                            # Tamanho da fonte
            color="#E1E1FF"                     # Cor do texto (branco azulado)
        ),
        title_font=dict(size=20, color="#A29BFE"),  # Fonte e cor do título
        xaxis=dict(
            tickmode='array',                   # Usa um array para definir os valores dos ticks
            tickvals=dados_agrupados['ANO'],    # Valores de cada ano no eixo X
            ticktext=dados_agrupados['ANO'],    # Texto dos ticks
            title="Ano",                        # Título do eixo X
            color="#E1E1FF",                    # Cor dos ticks e do título do eixo X
            showgrid=False                      # Remove a grade vertical
        ),
        yaxis=dict(
            title="Total de Ocorrências",       # Título do eixo Y
            color="#E1E1FF",                    # Cor dos ticks e do título do eixo Y
            showgrid=True,                      # Mantém a grade horizontal para orientação
            # Cor da grade (cinza azulado com transparência)
            gridcolor="rgba(68,68,90,0.5)"
        ),

    )

    # Converte o gráfico em HTML
    grafico_html = pio.to_html(fig, full_html=False)
    return grafico_html


def gerar_grafico_local():

    dados = ler_arquivo_csv("cleaned_result.csv")
    if dados is None:
        return "<p>Erro ao carregar os dados.</p>"

    # Agrupar os dados por local e somar as ocorrências
    dados_agrupados = dados.groupby(
        "LOCAL")["CONTAGEM"].sum().reset_index(name='total_ocorrencias')

    # Criar o gráfico de pizza
    fig = px.pie(
        dados_agrupados,
        names='LOCAL',
        values='total_ocorrencias',
        color='LOCAL',  # Cores distintas para os locais
        color_discrete_sequence=px.colors.qualitative.Set3  # Cores definidas
    )

    # Estilo e configuração do gráfico
    fig.update_layout(
        # Cor de fundo do gráfico (azul escuro)
        plot_bgcolor='rgba(18,18,30,1)',
        # Cor de fundo do "papel" (preto-azulado)
        paper_bgcolor='rgba(10,10,25,1)',
        font=dict(
            family="Arial",                     # Fonte do texto
            size=12,                            # Tamanho da fonte
            color="#E1E1FF"                     # Cor do texto (branco azulado)
        ),
        title_font=dict(size=20, color="#A29BFE")  # Fonte e cor do título
    )

    # Converte o gráfico em HTML
    gerar_gr_html = pio.to_html(fig, full_html=False)
    return gerar_gr_html


def total_suicidios():
    dados = ler_arquivo_csv("cleaned_result.csv")
    if dados is None:
        return "<p>Erro ao carregar os dados.</p>"

    total_suicidios = dados['CONTAGEM'].sum()
    return total_suicidios


def idade_mais_afetada():
    dados = ler_arquivo_csv("cleaned_result.csv")
    if dados is None:
        return None, None

    faixa_agrupada = dados.groupby('IDADE')['CONTAGEM'].sum()
    idade = faixa_agrupada.idxmax()
    suicidios = faixa_agrupada.max()

    return idade, suicidios
