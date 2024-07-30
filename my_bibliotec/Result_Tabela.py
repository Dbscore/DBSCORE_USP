import csv
import os
import pandas as pd
from unidecode import unidecode
import unicodedata

def remover_acentos(texto):
    return ''.join(c for c in unicodedata.normalize('NFKD', texto) if not unicodedata.combining(c))

def arquivo_existe(nome_do_arquivo):
    return os.path.exists(nome_do_arquivo) and os.path.getsize(nome_do_arquivo) > 0
                
def GerarTabela(dadosCombinado,nome_do_arquivo,cabeçalho):
    
    modo_de_abertura = 'a' if arquivo_existe(nome_do_arquivo) else 'w'
    with open(nome_do_arquivo, mode=modo_de_abertura, newline='', encoding='utf-8') as file:
        escritor = csv.writer(file)
        if modo_de_abertura == 'w':
            escritor.writerow(cabeçalho)  # Escreve o cabeçalho apenas se for um novo arquivo
        escritor.writerow(dadosCombinado)    
                
                
def GerarResult_TabelaN(out,OpenTabela,FairN,Maturidade,relat):
    cabeçalho = ['Nome_Base', 'OL', 'RE', 'OF', 'URI', 'LD', 'F','A','I','R','Completude','Singularidade','Validade','Consistencia']#'Consistencia'
    dadosCombinado = out+OpenTabela+FairN+Maturidade
    nome_do_arquivo = relat + 'ResultTabela_unitario.csv'
    GerarTabela(dadosCombinado,nome_do_arquivo,cabeçalho)    
    
        
def GerarResult_TabelaV(out,OpenTabela,FairN,Maturidade,relat):
    
    cabeçalho2 = ['Nome_Base','Openess','FAIR','MaturidadeDados']
    dadosCombinado = out+[OpenTabela]+[FairN]+[Maturidade]
    nome_do_arquivo = relat + 'ResultTabela_Vetorial.csv'
    GerarTabela(dadosCombinado,nome_do_arquivo,cabeçalho2)
        
        
def GerarResult_TabelaM(out,OpenTabela,FairN,Maturidade,relat):
    
    cabeçalho3 = ['Nome_Base','Openess_Media','FAIR_Media','MaturidadeDados_Media']
    mediaOpeness = sum(OpenTabela)/len(OpenTabela)
    mediaFairN = sum(FairN)/len(FairN) 
    mediaMaturidade = sum(Maturidade)/len(Maturidade)  
    dadosCombinado = out+[mediaOpeness,mediaFairN,mediaMaturidade]
    nome_do_arquivo = relat + 'ResultTabela_media.csv' 
    
    GerarTabela(dadosCombinado,nome_do_arquivo,cabeçalho3)
    
def ConfDataframe(relat):
    df1 = pd.read_csv(relat + 'ResultTabela_unitario.csv')
    df2 = pd.read_csv(relat + 'ResultTabela_Vetorial.csv')
    df3 = pd.read_csv(relat + 'ResultTabela_media.csv')
        
    #Pre_processamento_base_dados    
        
    df1 = df1.drop_duplicates()
    df2 = df2.drop_duplicates()
    df3 = df3.drop_duplicates()
    
    df1.loc[:,'Nome_Base'] = df1['Nome_Base'].apply(remover_acentos)
    df2.loc[:,'Nome_Base'] = df2['Nome_Base'].apply(remover_acentos)
    df3.loc[:,'Nome_Base'] = df3['Nome_Base'].apply(remover_acentos)
    
    df3.loc[:,'Openess_Media'] = pd.to_numeric(df3['Openess_Media'], errors='coerce')
    
    df3.loc[:, 'FAIR_Media'] = pd.to_numeric(df3['FAIR_Media'], errors='coerce')
    
    df1.to_csv(relat + 'ResultTabela_unitario.csv', index=False)
    df2.to_csv(relat + 'ResultTabela_Vetorial.csv', index=False)
    df3.to_csv(relat + 'ResultTabela_media.csv', index=False)
    
   
    
    
    
    
    