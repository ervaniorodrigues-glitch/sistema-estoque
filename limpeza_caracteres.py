#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo para limpeza de caracteres especiais
"""

import re
import pandas as pd

def limpar_caracteres_especiais(texto):
    """
    Remove ou substitui caracteres especiais de uma string
    
    Args:
        texto (str): Texto a ser limpo
        
    Returns:
        str: Texto limpo
    """
    if not texto or not isinstance(texto, str):
        return texto
    
    # Remover caracteres de controle
    texto = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', texto)
    
    # Substituir caracteres problemáticos
    substituicoes = {
        '"': '"',
        '"': '"',
        ''': "'",
        ''': "'",
        '–': '-',
        '—': '-',
        '…': '...',
        '®': '(R)',
        '©': '(C)',
        '™': '(TM)'
    }
    
    for original, substituto in substituicoes.items():
        texto = texto.replace(original, substituto)
    
    # Remover espaços extras
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    return texto

def limpar_dataframe_exportacao(df):
    """
    Limpa um DataFrame para exportação, removendo caracteres especiais
    
    Args:
        df (pandas.DataFrame): DataFrame a ser limpo
        
    Returns:
        pandas.DataFrame: DataFrame limpo
    """
    if df is None or df.empty:
        return df
    
    # Criar cópia do DataFrame
    df_limpo = df.copy()
    
    # Limpar colunas de texto
    for coluna in df_limpo.columns:
        if df_limpo[coluna].dtype == 'object':
            df_limpo[coluna] = df_limpo[coluna].astype(str).apply(limpar_caracteres_especiais)
    
    return df_limpo

def validar_entrada_texto(texto, max_length=None):
    """
    Valida e limpa texto de entrada
    
    Args:
        texto (str): Texto a ser validado
        max_length (int): Comprimento máximo permitido
        
    Returns:
        str: Texto validado e limpo
    """
    if not texto:
        return ""
    
    # Limpar caracteres especiais
    texto_limpo = limpar_caracteres_especiais(str(texto))
    
    # Aplicar limite de comprimento se especificado
    if max_length and len(texto_limpo) > max_length:
        texto_limpo = texto_limpo[:max_length].strip()
    
    return texto_limpo

def sanitizar_nome_arquivo(nome):
    """
    Sanitiza nome de arquivo removendo caracteres inválidos
    
    Args:
        nome (str): Nome do arquivo
        
    Returns:
        str: Nome sanitizado
    """
    if not nome:
        return "arquivo"
    
    # Remover caracteres inválidos para nomes de arquivo
    nome_limpo = re.sub(r'[<>:"/\\|?*]', '_', str(nome))
    
    # Remover espaços extras e pontos no final
    nome_limpo = re.sub(r'\s+', '_', nome_limpo).strip('.')
    
    # Garantir que não seja vazio
    if not nome_limpo:
        nome_limpo = "arquivo"
    
    return nome_limpo