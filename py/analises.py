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
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(10,10,25,1)',
        font=dict(
            family="Roboto",                     # Fonte do texto
            size=14,                            # Tamanho da fonte
            color="#E1E1FF"                     # Cor do texto (branco azulado)
        ),
        title_font=dict(size=20, color="#A29BFE"),  # Fonte e cor do título
        xaxis=dict(
            tickmode='array',                   # Usa um array para definir os valores dos ticks
            tickvals=dados_agrupados['ANO'],    # Valores de cada ano no eixo X
            ticktext=dados_agrupados['ANO'],    # Texto dos ticks
            title="Ano",                        # Título do eixo X
            color="#E1E1FF",                    # Cor dos ticks e do título do eixo X
            showgrid=True,
            gridcolor="rgba(68,68,90,0.5)"
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
    dados_agrupados['LOCAL'] = dados_agrupados['LOCAL'].str.capitalize()

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
            family="Roboto",                     # Fonte do texto
            size=14,                            # Tamanho da fonte
            color="#E1E1FF"                     # Cor do texto (branco azulado)
        ),
        title_font=dict(size=20, color="#A29BFE"),
        legend=dict(
            title="Locais",        # Título da legenda
            font=dict(
                size=14,           # Tamanho da fonte
                color="#E1E1FF"    # Cor do texto da legenda
            ),
            orientation="v",
            x=1,
            y=1
        )
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


def local_mais_ocorrencias():
    dados = ler_arquivo_csv("cleaned_result.csv")
    if dados is None:
        return None, None

    local_agrupado = dados.groupby('LOCAL')['CONTAGEM'].sum()
    local = local_agrupado.idxmax()
    ocorrencias = local_agrupado.max()

    return local, ocorrencias


def gerar_grafico_faixa_etaria():
    # Ler os dados do arquivo CSV
    dados = ler_arquivo_csv("cleaned_result.csv")
    if dados is None:
        return "<p>Erro ao carregar os dados.</p>"

    # Criar faixas de 5 em 5 anos para a idade
    faixa_etaria = pd.cut(dados['IDADE'], bins=range(0, 101, 5), right=False,
                          labels=[f"{i}-{i+4}" for i in range(0, 100, 5)])

    # Adicionar a coluna de faixa etária ao DataFrame
    dados['FAIXA_ETARIA'] = faixa_etaria

    # Agrupar os dados pela faixa etária e somar os suicídios
    dados_agrupados = dados.groupby("FAIXA_ETARIA", as_index=False)[
        "CONTAGEM"].sum()

    # Criar gráfico de barras horizontal
    fig = px.bar(
        dados_agrupados,
        x="CONTAGEM",  # Total de suicídios
        y="FAIXA_ETARIA",  # Faixa etária
        orientation="h",  # Gráfico horizontal
        labels={"FAIXA_ETARIA": "Faixa Etária",
                "CONTAGEM": "Total de Suicídios"},
    )

    # Estilo e configuração do gráfico
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Cor de fundo do gráfico
        paper_bgcolor='rgba(10,10,25,1)',  # Cor de fundo do "papel"
        font=dict(
            family="Arial",                     # Fonte do texto
            size=12,                            # Tamanho da fonte
            color="#E1E1FF"                    # Cor do texto
        ),
        xaxis=dict(
            showgrid=True,                      # Mostrar grade horizontal
            gridcolor="rgba(68,68,90,0.5)"      # Cor da grade
        ),
        title_font=dict(size=20, color="#A29BFE"),  # Fonte e cor do título
        xaxis_title="Total de Suicídios",  # Título do eixo X
        yaxis_title="Faixa Etária",  # Título do eixo Y


    )

    # Converter o gráfico em HTML para exibição
    gerar_gr_faixa_etaria_html = pio.to_html(fig, full_html=False)
    return gerar_gr_faixa_etaria_html


# Função para gerar o gráfico de distribuição das maiores causas ao longo dos anos
def gerar_grafico_suicidios_distribuicao():
    # Carregar os dados
    dados = ler_arquivo_csv("cleaned_result.csv")
    if dados is None:
        return "<p>Erro ao carregar os dados.</p>"

    # Agrupar os dados por ANO, CAUSAS e somar a CONTAGEM de suicídios
    dados_agrupados = dados.groupby(['ANO', 'CAUSAS'])[
        'CONTAGEM'].sum().reset_index()

    # Identificar as 5 causas mais comuns
    top_causas = dados_agrupados.groupby(
        'CAUSAS')['CONTAGEM'].sum().sort_values(ascending=False).head(5).index
    dados_top_causas = dados_agrupados[dados_agrupados['CAUSAS'].isin(
        top_causas)]

    # Gerar o gráfico de linha com bolinhas para as 5 principais causas ao longo dos anos
    fig = px.line(dados_top_causas,
                  x='ANO',
                  y='CONTAGEM',
                  color='CAUSAS',
                  markers=True,  # Adicionar bolinhas nos pontos
                  title='Distribuição das Maiores Causas de Suicídios ao Longo dos Anos',
                  labels={'CONTAGEM': 'Número de Suicídios',
                          'CAUSAS': 'Causa do Suicídio',
                          'ANO': 'Ano'},
                  color_discrete_sequence=px.colors.qualitative.Set3)

    # Estilo do gráfico para fundo escuro e texto claro
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Fundo transparente para o gráfico
        paper_bgcolor='#2e2e2e',  # Fundo do papel escuro
        font=dict(color='white'),  # Cor do texto em branco
        title=dict(font=dict(color='white')),  # Cor do título
        xaxis=dict(
            title_font=dict(color='white'),  # Cor do título do eixo X
            tickfont=dict(color='white'),  # Cor dos ticks do eixo X
            tickmode='linear',  # Assegura que os ticks sejam em anos
        ),
        yaxis=dict(
            title_font=dict(color='white'),  # Cor do título do eixo Y
            tickfont=dict(color='white'),  # Cor dos ticks do eixo Y
            tickmode='linear',  # Ticks lineares
            dtick=30  # Definir intervalo de 30 para os valores do eixo Y
        ),
        legend=dict(
            orientation='h',  # Coloca a legenda na horizontal
            yanchor='bottom',  # Alinha a legenda ao fundo do gráfico
            y=-0.2,  # Distância da legenda para baixo do gráfico
            xanchor='center',  # Centraliza a legenda no gráfico
            x=0.5  # Centraliza a legenda horizontalmente
        )
    )

    # Gerar o gráfico em formato HTML
    gerar_grafico_suicidios_distribuicao_html = pio.to_html(
        fig, full_html=False)
    return gerar_grafico_suicidios_distribuicao_html
