#from nis import cat
from DadosAbertosBrasil import ibge, favoritos
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import os
import requests
from sqlalchemy import case
from datetime import datetime

def Extrair_Base_IBGE(TipoArquivo,codig):
    
    CaminhosN = []
    endH = 'BaseDados/IBGE/'

    try:
        os.makedirs(endH)
    except:    
        pass


    df1 = ibge.referencias('a')#Pegar os codigos dos assuntos
    file_name = 'CodigoIBGE_assunto.xlsx'
    #df1.to_excel(file_name, index = None, header=True)

    df3 = ibge.referencias('n')

    #Assunto = input('Qual é o assunto da busca (indicar o numero com base na tabela "CodigoIBGE_assunto.xlsx"):  ')
    Assunto = codig
    metaListDf = ibge.lista_tabelas(assunto = Assunto)
    tabela =list(metaListDf['tabela_id'])
    identific = list(metaListDf['tabela_nome'])
    df_mostra = df1[df1['cod']==Assunto]
    df_mostra = df_mostra.reset_index(drop=True)
    
    #Palavra Chave
    busca = df_mostra['referencia'][0]

    print('Termo buscado: ', busca)
    print('Quantidade de tabelas (cod) da busca no IBGE:', len(tabela))
    
    bb =[]
    bb.append(busca)
    
    for i, item in enumerate(bb):
        bb[i] = item.replace(' ', '_')
    
    
    D = 'BaseDados/IBGE/DownloadDadosAPI/'+ str(bb[0])+'/'

    try:
        os.makedirs(D)
    except:    
        pass

    TT  = []
    TTN = []
    #TT.append(tabela[0])# Para pegar 1 valor #68 #163
    TT = tabela[0:1]
    #TTN.append(identific[0]) # Para pegar 1 valor 
    TTN = identific[0:1]    
    
    
    for T,NPasta in zip(TT,TTN): 
        
        m = ibge.Metadados(tabela=T)#Teste#992#6449
        
        D1 = D +'Dados_ID'+'_'+str(T) # Encontrar erro talvez nome muito grande..
        
        try:
            os.makedirs(D1)
            
        except:    
            print('Não criado..: ',D1)

        for cateG in m.classificacoes:

            categorias = [cat['id'] for cat in cateG['categorias']]#Pega o codigo de cada categoria
            
            Geograf = m.localidades['Administrativo']    
            Busca1 = [ ]
            BuscaFinal =[ ]
            
            for N in Geograf:
                dfaux =df3.loc[df3['cod']==N]
                dfaux = dfaux.reset_index(drop=True)
                Busca1.append(dfaux['referencia'][0])
            
            dataPadrao = {
            'codigo': [1, 2, 3, 6, 7, 8, 9, 13, 14, 15],
            'ref': ['Brasil', 'Grande Região', 'Unidade da Federação', 'Município', 'Região metropolitana','Mesorregião Geográfica','Microrregião geográfica','Região metropolitana e subdivisão','Região Integrada de Desenvolvimento',' Aglomeração urbana']
            }

            df4 = pd.DataFrame(dataPadrao)

            for N in Busca1:
                dfaux = df4.loc[df4['ref']==N]
                dfaux = dfaux.reset_index(drop=True)
                BuscaFinal.append(dfaux['codigo'][0])

            for Geo,nome in zip(BuscaFinal,Busca1):   
                for catX in categorias:     
                    try:
                        df = ibge.sidra(
                            tabela = T, 
                            periodos = 'last 2', #Quantidades de anos que pega
                            variaveis ='all', 
                            localidades ={Geo:'all'}, #{6:'all'},
                            classificacoes ={cateG['id']:[catX]} #{386:['all']}
                            )
                        NomeM = str(nome).replace(' ', '_')
                        replace_map = {'-': pd.NA, '...': pd.NA}
                        df.replace(replace_map, inplace=True)  
                        df.to_csv(D1 + '/' +'ID_'+ str(T) + '_' + str(NomeM)+'-'+'Classif_'+str(catX)+'.csv',index=False) 
                    except:
                        #print('Não encontrou a base(combinação)!')             
                        print(f"Erro ao fazer download da base id {str(T)!r} com nível geografico {str(nome)!r} e Classif. {str(catX)!r} ")
            CaminhosTemp = [os.path.join(D1, nome) for nome in os.listdir(D1)]
            CaminhosN.extend(CaminhosTemp) 
    #print(CaminhosN)
    print('Download finalizado das bases de dados/metadados!')
    return CaminhosN,busca                     