#Aviso: o PowerShell detectou que você talvez esteja usando um leitor de tela e 
#tenha desabilitado o PSReadLine para fins de compatibilidade. Se desejar reabilitá-lo, execute 'Import-Module PSReadLine'.

from lib2to3.pytree import Base
import pandas as pd
import sys
import numpy as np
import re
from requests import get
from sqlalchemy import true
import matplotlib.pyplot as plt
import time
from datetime import datetime
from my_bibliotec.Leitura import *
from my_bibliotec.Openness import *
import os
import shutil
from os import getcwd
from my_bibliotec.GeradorPDF import *
from my_bibliotec.FAIR import *
import platform
from my_bibliotec.MaturidadeDados import *
from my_bibliotec.ISOData import *
from my_bibliotec.Result_Tabela import *
   
   
def Resultado_csv(N_base,OpenTabela,FairN,Maturidade,relat):
    
    GerarResult_TabelaN(N_base,OpenTabela,FairN,Maturidade,relat)
    GerarResult_TabelaV(N_base,OpenTabela,FairN,Maturidade,relat)
    GerarResult_TabelaM(N_base,OpenTabela,FairN,Maturidade,relat)
       
   
def Separar_tipo(d1):
    
    r_csv = re.compile(".*csv")
    r_excel = re.compile(".*xlsx|.*xls")
    r_pdf = re.compile(".*pdf")   

    C = list(filter(r_csv.match, d1))
    X = list(filter(r_excel.match, d1)) 
    P = list(filter(r_pdf.match, d1)) 

    return C,X,P


def PadronizaEstruturaWeb(Caminho_Original,Vn,direc):
    
    os.chdir(Caminho_Original)
    
    Vn = Vn.replace('\\', '/')
    frase = re.split("/", Vn)
    out = frase[-1]
    BaseC = re.sub(r'[^\w\s]','',out)   
    Ccaminho = 'Resultados/Openness/'+  str(direc) + BaseC
    Ccaminho1 = 'Resultados/FAIR/'+ BaseC
    Relatorio = 'Resultados/Relatorio_Tabela/'
    Ccaminho2 = 'Resultados/Maturidade/'+ BaseC
    
    try:
        os.makedirs(Ccaminho)

    except:
        pass

    try:
        os.makedirs(Ccaminho1)
        os.makedirs(Relatorio)
    except:
        pass
        
    try:
        os.makedirs(Ccaminho2)

    except:
        pass    

    Save = Caminho_Original+'/'+Ccaminho+'/'
    Save1 = Caminho_Original+'/'+Ccaminho1+'/'    
    relat = Caminho_Original+ '/'+Relatorio
    Save2 = Caminho_Original+'/'+Ccaminho2+'/'
    
    
    return BaseC,Save,Save1,Save2,out,relat


def PadronizaEstruturaLocal(Caminho_Original,Vn):
    
    os.chdir(Caminho_Original)
    
    Vn = Vn.replace('\\', '/')
    frase = re.split("/", Vn)
    out = frase[-1]
    BaseC = re.sub(r'[^\w\s]','',out)   
    Ccaminho = 'Resultados/Openness/'+ BaseC 
    Ccaminho1 = 'Resultados/FAIR/'+ BaseC
    Ccaminho2 = 'Resultados/Maturidade/'+ BaseC
    Relatorio = 'Resultados/Relatorio_Tabela/'
    
    try:
        os.makedirs(Ccaminho)

    except:
        pass

    try:
        os.makedirs(Ccaminho1)
        os.makedirs(Relatorio)
        
    except:
        pass
    
    try:
        os.makedirs(Ccaminho2)
        
    except:
        pass
    
    Save = Caminho_Original+'/'+Ccaminho+'/'
    Save1 = Caminho_Original+'/'+Ccaminho1+'/'    
    Save2 = Caminho_Original+'/'+Ccaminho2+'/'
    relat = Caminho_Original+ '/'+Relatorio
    
    return BaseC,Save,Save1,Save2,out,relat


def CorrigeCaminho(Vn):
    
    Vn = Vn.replace('\\', '/')        
    
    return Vn    


def AnaliseDBscore(caminho_arquivo):
    codig =0
    #Gerar/Apagar pastas principais...
    Apagar_Criar_Pastas( )
    pathR=''
    Caminho_Original = getcwd() # Guarda Caminho para salvar Corretamente 
    
    #Começo do tempo do codigo 
    #start_time = datetime.now() 
    
    #dado = [ ] 
    ListZ = [ ]
    CHaveOrigem = [ ] #Variavel que determina o tipo de input/como foi importado os dados 
    ListaHttPsF_http = ['https://servicodados.ibge.gov.br/api/v3/agregados']#'https://aplicacoes.mds.gov.br/sagirmps/portal-san/artigo.php?link=23' Fora do ar ..
    
    #infile = Entrada_arquivo()
    infile = caminho_arquivo
    #dado.append(infile)
    
    r_htt = re.compile("API_")
    H = list(filter(r_htt.match, infile))
    
    r_htt1 = re.compile("Dados_Abertos_")
    H2 = list(filter(r_htt1.match, infile))
    
    
    if H != [ ]:
        Perm = 'CC-BY' #PDDL, ODC-by or CC0 entre outros ..
    
    else:
        #Perm = Permissao()    
        Perm = 'CC-BY'
    
    if (H!=[]):    
        
        Verf = True
        
        if Verf == True:
            
            dado=H
            direc = '0'
            CHaveOrigem = ListaHttPsF_http
            direc = direc + '/'
            #print('\n')
            #print("\nProcessando análises dos indicadores...\n")
            
            for d in dado:
                d1= [ ]
                d1.append(d)
                
                # Verifica se é um arquivo.zip
                r_zip = re.compile(".*zip")
                Z = list(filter(r_zip.match, d1))
    
                C,X,P = Separar_tipo(d1)
                
                if(Z != []):
                    dado1 = Arq_zip(Z) 
                    
                    r_csv = re.compile(".*csv")
                    r_excel = re.compile(".*xlsx|.*xls") 
                    r_pdf = re.compile(".*pdf")   
    
                    C = list(filter(r_csv.match, dado1))
                    X = list(filter(r_excel.match, dado1)) 
                    P = list(filter(r_pdf.match, dado1))    
             
                if(C != []):
                    
                    for Vn in C:
                        
                    # #Direcionar o caminho para a pasta Original 
                    #     os.chdir(Caminho_Original)
                        
                        SO = platform.system() 
                        
                        if SO == 'Windows': 
                            
                            BaseDados, Const,endereco,chave = Arq_csv(TipoArquivo = Vn,Permissao=Perm)
                            BaseC,Save,Save1,Save2,out,relat = PadronizaEstruturaWeb(Caminho_Original,Vn,direc)              
                            Star,Salvar,OpenTabela = Definicao_Openness(BaseDados,Const,endereco,chave,BaseC,CHaveOrigem,Save) 
                            FairF,FairN = ValidarRegras(CHaveOrigem[0],Save1,chave,Const)
                            Maturidade = ValidarMaturidade(Vn,Save2,chave,Const)
                            
                            N_base = [out]
                            Resultado_csv(N_base,OpenTabela,FairN,Maturidade,relat)
                            GerarPDF(Star,Salvar,out,CHaveOrigem,Save1,Save2,relat,FairF)
                            
                        else:
                            
                            BaseDados, Const,endereco,chave = Arq_csv(TipoArquivo = Vn,Permissao=Perm)
                            BaseC,Save,Save1,Save2,out,relat = PadronizaEstruturaWeb(Caminho_Original,Vn,direc)
                            Star,Salvar,OpenTabela = Definicao_Openness(BaseDados,Const,endereco,chave,BaseC,CHaveOrigem,Save) 
                            FairF,FairN = ValidarRegras(H[0],Save1,chave,Perm)
                            Maturidade = ValidarMaturidade(Vn,Save2,chave,Const)
                            
                            N_base = [out]
                            Resultado_csv(N_base,OpenTabela,FairN,Maturidade,relat)
                            
                            GerarPDF(Star,Salvar,out,CHaveOrigem,Save1,Save2,relat,FairF)
                    
                                
                
                if(X != []):
                    
                    for Vn in X:
    
                        BaseDados, Const,endereco,chave = Arq_xls(TipoArquivo = Vn,Permissao=Perm)
                        BaseC,Save,Save1,Save2,out,relat = PadronizaEstruturaWeb(Caminho_Original,Vn,direc) 
                        Star,Salvar,OpenTabela = Definicao_Openness(BaseDados,Const,endereco,chave,BaseC,CHaveOrigem,Save)
                        FairF,FairN = ValidarRegras(H[0],Save1,chave,Const)
                        Maturidade = ValidarMaturidade(Vn,Save2,chave,Const)
                        N_base = [out]
                        Resultado_csv(N_base,OpenTabela,FairN,Maturidade,relat)
                        GerarPDF(Star,Salvar,out,CHaveOrigem,Save1,Save2,relat,FairF)
                    
                    
                
                if(P != []):
                    
                    for Vn in P:
                
                        Vn = CorrigeCaminho(Vn)
                        BaseDados, Const,endereco,chave = Arq_pdf(TipoArquivo = P[0],Permissao=Perm)           
                        BaseC,Save,Save1,Save2,out,relat = PadronizaEstruturaWeb(Caminho_Original,Vn)
                        #print(BaseDados)
                        try:
                            
                            if isinstance(BaseDados,pd.core.frame.DataFrame):   
                
                                Star,Salvar,OpenTabela = Definicao_Openness(BaseDados,Const,endereco,chave,BaseC,CHaveOrigem,Save)
                                FairF,FairN = ValidarRegras(Vn,Save1,chave,Const)
                                Maturidade = ValidarMaturidade(Vn,Save2,chave,Const)
                                N_base = [out]
                                Resultado_csv(N_base,OpenTabela,FairN,Maturidade,relat)
                                GerarPDF(Star,Salvar,out,CHaveOrigem,Save1,Save2,relat,FairF)
                                
                
                                os.remove('DataframePDF.csv')
                            
                            else:
                                print('O arquivo (%s) não é um base de dados !'%(P[0]))
                        except:
                            pass
        
                ConfDataframe(relat)
                            
        else:
            print("Http não adicionado ao sistema!")                    
        
        #ConfDataframe(relat)
        controleHTTPS = 1
    #parte de controle
    
    if (H2 !=[]): 
        CHaveOrigem = []
        
        dado=H2
        
        r_zip = re.compile(".*zip")
        Z = list(filter(r_zip.match, dado))
    
        if(Z != []):   
            
            dado = Arq_zip(Z)
    
        C,X,P =Separar_tipo(dado)
    
        if(C != []):
            
            for Vn in C:
                
                Vn = CorrigeCaminho(Vn)
                BaseDados, Const,endereco,chave = Arq_csv(TipoArquivo = Vn,Permissao=Perm)
                BaseC,Save,Save1,Save2,out,relat = PadronizaEstruturaLocal(Caminho_Original,Vn)
                            
                Star,Salvar,OpenTabela = Definicao_Openness(BaseDados,Const,endereco,chave,BaseC,CHaveOrigem,Save) 
                FairF,FairN = ValidarRegras(Vn,Save1,chave,Const)
                Maturidade = ValidarMaturidade(Vn,Save2,chave,Const)
                
                N_base = [out]
                Resultado_csv(N_base,OpenTabela,FairN,Maturidade,relat)
                GerarPDF(Star,Salvar,out,CHaveOrigem,Save1,Save2,relat,FairF)#Falta arrumar..
    
        if(X != []):
            
            for Vn in X:
                
                Vn = CorrigeCaminho(Vn)
                BaseDados, Const,endereco,chave = Arq_xls(TipoArquivo = Vn,Permissao=Perm)
                BaseC,Save,Save1,Save2,out,relat = PadronizaEstruturaLocal(Caminho_Original,Vn)
                
                Star,Salvar,OpenTabela = Definicao_Openness(BaseDados,Const,endereco,chave,BaseC,CHaveOrigem,Save) 
                FairF,FairN = ValidarRegras(Vn,Save1,chave,Const)
                Maturidade = ValidarMaturidade(Vn,Save2,chave,Const)
                GerarPDF(Star,Salvar,out,CHaveOrigem,Save1,Save2,relat,FairF)
                
                N_base = [out]
                Resultado_csv(N_base,OpenTabela,FairN,Maturidade,relat)
        
        if(P != []):
            
            for Vn in P:
                
                Vn = CorrigeCaminho(Vn)
                BaseDados, Const,endereco,chave = Arq_pdf(TipoArquivo = P[0],Permissao=Perm)           
                BaseC,Save,Save1,Save2,out,relat = PadronizaEstruturaLocal(Caminho_Original,Vn)
                #print(BaseDados)
                try:
                    
                    if isinstance(BaseDados,pd.core.frame.DataFrame):   
        
                        Star,Salvar,OpenTabela = Definicao_Openness(BaseDados,Const,endereco,chave,BaseC,CHaveOrigem,Save)
                        FairF,FairN = ValidarRegras(Vn,Save1,chave,Const)
                        Maturidade = ValidarMaturidade(Vn,Save2,chave,Const)
                        N_base = [out]
                        Resultado_csv(N_base,OpenTabela,FairN,Maturidade,relat)
                        GerarPDF(Star,Salvar,out,CHaveOrigem,Save1,Save2,relat,FairF)
                        
        
                        os.remove('DataframePDF.csv')
                    
                    else:
                        print('O arquivo (%s) não é um base de dados !'%(P[0]))
                except:
                    pass
        
        ConfDataframe(relat)
    
    pathR = Caminho_Original + '/'+"Resultados"#/Relatorio

    return pathR










