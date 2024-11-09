"""Função para ler o arquivo CSV 'clean_result.csv' e retornar um DataFrame com os dados.
"""

import pandas as pd
import os

def ler_arquivo_csv(nome_arquivo):
    # Ajuste o caminho com base no diretório atual
    caminho = os.path.join(os.getcwd(), '..', 'data', nome_arquivo)
    if not os.path.exists(caminho):
        print(f"Arquivo {nome_arquivo} não encontrado! Caminho: {caminho}")
        return None
    df = pd.read_csv(caminho)
    return df

