from lib2to3.pytree import Base
from operator import index
from unicodedata import category
from jinja2 import ChainableUndefined
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import os
from random import choice
from rdflib import Graph
import rdflib
import tabula
import platform
import matplotlib
import warnings
warnings.simplefilter("ignore", UserWarning)
plt.switch_backend('agg')

def Preencher_Regras(BaseDados,name,Permissao,i,m,chave,endereco,CHaveOrigem):#Falta colocar condições para outras perguntas
    
    if name == 'OL':   
        
        if i == 0: #Verificar Licenca dos dados
            P = Preencher_Licenca_OL(Permissao)
            rr = P  

        elif i == 1: # C1-Você pode olhar e imprimir os dados    
            R = BaseDados.empty     
            if R == False:    
                try:    
                    BaseDados.head()
                    rr = 'Sim'                     
                except:
                    rr ='Não'
            else:
                rr = 'Não'
            
        elif i == 2: # C2-Você pode armazenar e comparar    
            try:    
                if chave == '.csv' or chave =='.pdf':         
                    BaseDados.to_csv('teste.csv',index=False)
                    df_teste = pd.read_csv('teste.csv')
                    Verifica = BaseDados.equals(BaseDados)
                    
                    if Verifica ==True:
                        rr='Sim' 
                    else:
                        rr='Não'               
                    os.remove('teste.csv')
                elif chave =='.xlsx':
                    BaseDados.to_excel('teste.xlsx', index = False)
                    df_teste = pd.read_excel('teste.xlsx')
                    Verifica = BaseDados.equals(BaseDados)
                    
                    if Verifica ==True:
                        rr='Sim' 
                    else:
                        rr='Não'                
                    os.remove('teste.xlsx')
            except:
                rr = 'Não'
        
        elif i == 3: # C3-Você pode introduzir os dados em qualquer outro sistema   
            
            if m[2][1] == 'Sim':    
                rr = 'Sim'
            else:
                rr = 'Não'

        elif i == 4: # C4-Pode alterar os dados sempre que quiser         
            
            numericos_int = ['int16', 'int32', 'int64']
            numericos_float = ['float16', 'float32', 'float64']
            objetos = ['object'] 
            booleanos = ['bool']
            categ = ['category']#Mexer mais ..

            df_numeric_int = BaseDados.select_dtypes(include = numericos_int)
            df_numeric_float = BaseDados.select_dtypes(include = numericos_float)
            df_objetos = BaseDados.select_dtypes(include = objetos)
            df_booleanos = BaseDados.select_dtypes(include = booleanos)

            try:        
                if(df_numeric_int.empty == False):
                    dfAux = BaseDados.copy()
                    cc = list(df_numeric_int.columns)
                    v = choice(cc)            
                    BaseDados[v] = 13

                    if (dfAux[v].equals(BaseDados[v]))==False:
                        rr = 'Sim'
                    else:
                        rr = 'Não'

                elif(df_numeric_float.empty == False):
                    dfAux = BaseDados.copy()
                    cc = list(df_numeric_float.columns)
                    v = choice(cc)            
                    BaseDados[v] = 13.13

                    if (dfAux[v].equals(BaseDados[v]))==False:
                        rr = 'Sim'
                    else:
                        rr = 'Não'

                
                elif(df_objetos.empty == False):
                    dfAux = BaseDados.copy()
                    cc = list(df_objetos.columns)
                    v = choice(cc)            
                    BaseDados[v] = 'PT'   

                    if (dfAux[v].equals(BaseDados[v]))==False:
                        rr = 'Sim'
                    else:
                        rr = 'Não'

                elif (df_booleanos.empty == False):
                    
                    dfAux = BaseDados.copy()
                    cc = list(df_numeric_int.columns)
                    v = choice(cc)            
                    BaseDados[v] = True

                    if (dfAux[v].equals(BaseDados[v]))==False:
                        rr = 'Sim'
                    else:
                        rr = 'Não'
                
                elif (df_objetos.empty == False):
                    
                    dfAux = BaseDados.copy()
                    cc = list(df_numeric_int.columns)
                    v = choice(cc)            
                    BaseDados[v] = 'L13'

                    if (dfAux[v].equals(BaseDados[v]))==False:
                        rr = 'Sim'
                    else:
                        rr = 'Não'                     
           
            except:
                 rr='Não'
        
        elif i == 5:  # C5-Pode compartilhar os dados   
            
            if m[2][1] == 'Sim' and m[3][1] == 'Sim':    
                rr = 'Sim'
            else:
                rr = 'Não'
        
        elif i == 6: # P1-Facilidade de publicar    
            
            if m[5][1] == 'Sim':   
                rr = 'Sim'
            else:
                rr = 'Não'
        
        elif i == 7: # P2-Não precisa especificar os dados para outros        
           
           Verifica = isinstance(BaseDados, pd.core.frame.DataFrame)    
           
           if Verifica == True:
            rr = 'Sim'
           else:
            rr = 'Não'    
    
    elif name =='OL+RE': 
        
        if i == 0:   # C6-Processamento em software proprietario,realizar cálculos, visualizações etc               
            if chave != '.pdf': 
                try:
                    BaseDados.describe(include='all') #Agregação/Visualização    
                    rr = 'Sim'
                except:
                    rr = 'Não'               
                    
            else:    
                rr = 'Não'        
        
        elif i == 1: #C7-Exportar para outros formato (Estruturado) 
            
            if chave != '.pdf':
                try: 
                    if chave == '.csv': 
                        
                        BaseDados.to_excel('BaseDadoExcel.xlsx')
                        Verifica = BaseDados.equals(BaseDados)
                                         
                        if Verifica == True:                     
                            rr = 'Sim'
                        
                        else:
                            rr = 'Não'
                   
                        os.remove('BaseDadoExcel.xlsx')

                    elif chave == '.xlsx':        
                        
                        BaseDados.to_csv ("Test.csv",  
                                           index = None, 
                                           header=True) 
                        
                        os.remove('Test.csv')
                        
                        rr = 'Sim'
                
                except:
                    rr = 'Não'        
            else:
                rr = 'Sim'        

    elif name =='OL+RE+OF': #Dados Empacotados na Web 
        
        if i == 0:  #C8-Manipulação dos dados sem restrição de software proprietário     
            if chave !='.pdf':   
            
                SoftawareP = ['.xlsx','.xls'] #Lista de formatos proprietários
            
                Verifica = chave in SoftawareP

                if Verifica:
                
                    rr = 'Não'
    
                else:
                    rr = 'Sim'    
            else:
                rr = 'Não'
        
        elif i == 1: #C9-Dados empacotados na web   #Regra pensar dados empacotados ou dados da web
            if chave != '.pdf':    
                #DadosnaWeb = ['.csv',] #Lista de formatos proprietários
                #DadosdaWeb = []    
                rr = 'Sim'
            else:
                rr ='Não'

    elif name =='OL+RE+OF+URI': # URI formato e funcionalidades
    #A URI une o Protocolo (https://) a localização do recurso (URL - woliveiras.com.br) e o nome do recurso (URN - /desenvolvedor-front-end/) para que você acesse as coisas na Web.            
        
        if i == 0:
            if chave != '.pdf':
                rr = 'Sim'     
            else:
                rr = 'Não'
        elif i == 1 or i == 2 or i == 3: 
            
            if CHaveOrigem != []:    
                
                #print(CHaveOrigem)    
                end = re.split("/", CHaveOrigem[0])
                Prot = end[0]
                URL = end[1] + end[2]
                URN = end[-2] + end[-1]   
                  
                if (Prot == 'https:'):
                    rr = 'Sim'
                
                else:
                    rr='Não'
                
            else:
                rr = 'Não'
           
    elif name =='OL+RE+OF+URI+LD': #Verifica se tem o ticket de um formato .rdf e etcc

        if CHaveOrigem != []:

            if i == 0 or i ==1 or i==2 or i==3:   
                try:
                    g = Graph()
                    g.parse(CHaveOrigem[0])
                    V = isinstance(g,rdflib.graph.Graph)
                    
                    if V == True:                  
                        rr = 'Sim'     
                    
                except:
                    rr ='Não'

        else:
            rr ='Não'        

    return rr          

def Preencher_Licenca_OL(Permissao):
    
    Verif=['PDDL','ODC-by','CC0','CC-BY','ODbL','CC-BY-SA']
    
    aux = Permissao in Verif
    
    if aux == True:
        X = 'Sim'
    
    else:
        X = 'Não'
        
        if Permissao == 'Não sei':
            X = 'Não informado'

    return X

def Grafico_radar(G1,G2,BaseC,Salvar):
        
        G1 = [*G1, G1[0]]
        G2 = [*G2, G2[0]]
        
        # frase = re.split("/", endereco)
        # out = frase[-1]
        # nome = re.sub(r'[^\w\s]','',out)
        nome = BaseC

        num_vars = len(G1)

        label_loc = np.linspace(start=0, stop=2 * np.pi, num=num_vars)

        fig, ax = plt.subplots(figsize=(12, 12), subplot_kw=dict(polar=True))

        ax.plot(label_loc, G2, color='red', linewidth=1, label=nome)

        ax.fill(label_loc, G2, color='red', alpha=0.25)
        ax.set_ylim(0, 1)
        plt.title('Métrica Openness', size=20, y=1.05)
        lines, labels = plt.thetagrids(np.degrees(label_loc), labels=G1)
        ax.legend(loc='upper right', bbox_to_anchor=(1.0, 1.0))

        plt.savefig(Salvar+'Openness_radar.png', format='png')
        plt.cla()
        #plt.close()
        plt.close('all')
        
def Df_png(data, col_width=3.0, row_height=0.625, font_size=14,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 1, 1], header_columns=0,
                     ax=None, **kwargs):
        if ax is None:
            size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
            fig, ax = plt.subplots(figsize=size)
            ax.axis('off')
        mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)
        mpl_table.auto_set_font_size(False)
        mpl_table.set_fontsize(font_size)

        for k, cell in mpl_table._cells.items():
            cell.set_edgecolor(edge_color)
            if k[0] == 0 or k[1] < header_columns:
                cell.set_text_props(weight='bold', color='w')
                cell.set_facecolor(header_color)
            else:
                cell.set_facecolor(row_colors[k[0]%len(row_colors) ])
        return ax.get_figure(), ax
    
    
def OL(BaseDados,chave,regras,colunas,name,Salvar,Permissao,endereco,CHaveOrigem):    
    m = [ ]
    i = 0
    try:       
        for y in range(len(regras)):
            linha = []
            results = Preencher_Regras(BaseDados,name,Permissao,i,m,chave,endereco,CHaveOrigem)
            linha.append(regras[y])
            linha.append(results) 
            m.append(linha)
            i =i+1                                      
    except:
        print('Informações não legiveis_OL!')
    
    df1 = pd.DataFrame(m,columns=colunas)
    fig,ax = Df_png(df1, header_columns=0, col_width=10.0)
    fig.savefig(Salvar+name + '.png')  
    freq = df1.groupby(['Análise da base']).size()
    
    try:
        conDiv = freq['Sim']
        div = conDiv/8
    except:
        conDiv = 0
        div = conDiv/8
    
    return div,m
    
def RE(BaseDados,chave,regras,form,colunas,name,Salvar,endereco,CHaveOrigem):
    m = [ ]
    i = 0
    P ='Sim'
    try:       
        for y in range(len(regras)):
            linha = []
            results = Preencher_Regras(BaseDados,name,P,i,m,chave,endereco,CHaveOrigem)
            linha.append(regras[y])
            linha.append(results) 
            m.append(linha)
            i =i+1                                      
    except:
        print('Informações não legiveis_RE!')
    
    form.extend(m)
    
    df1 = pd.DataFrame(form,columns=colunas)
    fig,ax = Df_png(df1, header_columns=0, col_width=12.0)
    fig.savefig(Salvar+name + '.png') 
    df_last = df1.iloc[-2:]
    freq = df_last.groupby(['Análise da base']).size()

    try:
        conDiv = freq['Sim']
        div = conDiv/2
    except:
        conDiv = 0
        div = conDiv/2

    return div,form
    
def OF(BaseDados,chave,regras,form,colunas,name,Salvar,endereco,CHaveOrigem):
    m = [ ]
    i = 0
    P ='Sim'
    try:       
        for y in range(len(regras)):
            linha = []
            results = Preencher_Regras(BaseDados,name,P,i,m,chave,endereco,CHaveOrigem)
            linha.append(regras[y])
            linha.append(results) 
            m.append(linha)
            i =i+1                                      
    except:
        print('Informações não legiveis_OF!')
    
    form.extend(m)
    
    df1 = pd.DataFrame(form,columns=colunas)
    fig,ax = Df_png(df1, header_columns=0, col_width=12.0)
    fig.savefig(Salvar+name + '.png') 
    df_last = df1.iloc[-2:]
    freq = df_last.groupby(['Análise da base']).size()

    try:
        conDiv = freq['Sim']
        div = conDiv/2
    except:
        conDiv = 0
        div = conDiv/2

    return div,form
     
    
def URI(BaseDados,chave,regras,form,colunas,name,Salvar,endereco,CHaveOrigem):
    m = [ ]
    
    i = 0
    P ='Sim'
    
    try:       
        for y in range(len(regras)):
            linha = []
            results = Preencher_Regras(BaseDados,name,P,i,m,chave,endereco,CHaveOrigem)
            linha.append(regras[y])
            linha.append(results) 
            m.append(linha)
            i =i+1                                      
    except:
        print('Informações não legiveis_URI!')
    
    form.extend(m)
    
    df1 = pd.DataFrame(form,columns=colunas)
    fig,ax = Df_png(df1, header_columns=0, col_width=13.0)
    fig.savefig(Salvar+name + '.png') 
    df_last = df1.iloc[-4:]
    freq = df_last.groupby(['Análise da base']).size()

    try:
        conDiv = freq['Sim']
        div = conDiv/4
    except:
        conDiv = 0
        div = conDiv/4

    return div,form

    
def LD(BaseDados,chave,regras,form,colunas,name,Salvar,endereco,CHaveOrigem):
    m = [ ]
    i = 0
    P ='Sim'

    try:       
        for y in range(len(regras)):
            linha = []
            results = Preencher_Regras(BaseDados,name,P,i,m,chave,endereco,CHaveOrigem)
            linha.append(regras[y])
            linha.append(results) 
            m.append(linha)
            i =i+1                                      
    except:
        print('Informações não legiveis_LD!')
    
    form.extend(m)
    
    df1 = pd.DataFrame(form,columns=colunas)
    fig,ax = Df_png(df1, header_columns=0, col_width=14.0)
    fig.savefig(Salvar+name + '.png') 
    df_last = df1.iloc[-4:]
    freq = df_last.groupby(['Análise da base']).size()
    
    try:
        conDiv = freq['Sim']
        div = conDiv/4
    except:
        conDiv = 0
        div = conDiv/4
    
    df1N = df1.copy()
    df1N = df1[df1['Análise da base'] =='Não']

    fig,ax = Df_png(df1N, header_columns=0, col_width=14.0)
    fig.savefig(Salvar + 'RegrasN.png')
    
    return div,form
    
     
def Definicao_Openness(BaseDados,Permissao,endereco,chave,BaseC,CHaveOrigem,Save):
     
    #Importar variavies 
    #Salvar = '/home/lucas/Documentos/Doutorado_GT_Fome/Programa_Indicadores/Scripts/Resultados/Openness/'+ BaseC+'/'
    Salvar = Save
    SO = platform.system()    
    
    if SO == 'Windows':
        Salvar = Salvar.replace('\\', '/')
    
    
    colunas = ['Regras','Análise da base']
    regras  = ['Geral OL: Licença dos dados é aberta','C1(OL)-Você pode olhar e imprimir os dados', 'C2(OL)-Você pode armazenar',
    'C3(OL)-Você pode introduzir os dados em qualquer outro sistema','C4(OL)-Pode ter alterações nos dados',
    'C5(OL)-Pode compartilhar os dados','P1(OL)-Facilidade de publicar',
    'P2(OL)-Não precisa especificar os dados para outros']
    name ='OL'
    G1 = ['OL','RE','OF','URI','LD']       
    G2 = [ ]

    #OL(1 Estrela)
    Clasf,form = OL(BaseDados,chave,regras,colunas,name,Salvar,Permissao,endereco,CHaveOrigem)
    G2.append(Clasf) 
    
    #RE(2 Estrelas)
    name = name + str('+') + 'RE'
    regras_RE = ['C6(RE)-Processamento em software proprietario,realizar cálculos, visualizações etc',
    'C7(RE)-Exportar para outros formato(Estruturado)']
    Clasf,form = RE(BaseDados,chave,regras_RE,form,colunas,name,Salvar,endereco,CHaveOrigem)
    G2.append(Clasf) 
    
    #OF(3 Estrelas) 
    name = name + str('+') + 'OF'
    regras_OF = ['C8(OF)-Manipulação dos dados sem restrição de software proprietário','C9(OF)-Dados empacotados na web']
    Clasf,form = OF(BaseDados,chave,regras_OF,form, colunas,name,Salvar,endereco,CHaveOrigem)
    G2.append(Clasf) 
    
    #URI(4 Estrelas) #Falta fazer logica
    name = name + str('+') + 'URI'
    regras_URI = ['C10(URI)-Você pode apontar para ele de qualquer outro lugar (na Web ou localmente)','C11(URI)-Você pode marcar como favorito',
    'C12(URI)-A base tem dados que combinam com outros por meio de URI', 'C13(URI)-Formato é RDF ou outros padronizados da Web (Dados da Web)' ]
    Clasf,form = URI(BaseDados,chave,regras_URI,form, colunas,name,Salvar,endereco,CHaveOrigem)
    G2.append(Clasf) 

    #LD(5 Estrelas)#Falta fazer logica 
    name = name + str('+') + 'LD'
    regras_OF = ['C14(LD)-As bases são mais associadas a outros dados (relacionados) enquanto os manipula', 'C15(LD)-Ligação da base com outros dados da web','C16(LD)-Controle detalhado sobre os itens dos dados (Otimizando acessos e etc)', 'C17(LD)-Dados totalmente conectados a links'  
    ]
    Clasf,form = LD(BaseDados,chave,regras_OF,form, colunas,name,Salvar,endereco,CHaveOrigem)
    G2.append(Clasf) 
    
    if Preencher_Licenca_OL(Permissao) == 'Não' or Preencher_Licenca_OL(Permissao)=='Não informado':
        if chave =='.csv':
            G2[0]= G2[0] -0.075
            G2[1] = G2[1] - 0.2
            G2[2] = G2[2] - 0.1
        elif chave =='.xlsx' or chave == '.xls':
            G2[0]= G2[0] -0.075
            G2[1] = G2[1] - 0.5
        elif chave =='.pdf':
            G2[0]= G2[0] -0.075 
            G2[1] = G2[1] - 0.3
                  
    RDicin = dict(zip(G1,G2))
    listSum = sum(G2)
    #print('acabei de fazer a tabela:  ',Salvar)
    
    
    #Criar grafico Radar métrica Openess
    Grafico_radar(G1,G2,BaseC,Salvar)
    
    return RDicin,Salvar,G2
   

    



    
    
