
#Em construção ......

import pandas as pd
from datetime import datetime
import numpy as np
from scipy import stats
import random
import matplotlib.pyplot as plt
import warnings
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import chardet


warnings.simplefilter("ignore", UserWarning)
plt.switch_backend('agg')


def draw_bar_chart(percentages,Salvar,bar_width=0.5):
    """
    Desenha um gráfico de barras com as categorias A, B, C, D.
    
    :param percentages: Lista de percentagens para as categorias A, B, C, D.
    """
    # Categorias
    categories = ['Completude', 'Singularidade','Validade','Consistencia']
    
    # Verifique se a lista tem quatro valores (um para cada categoria)
    if len(percentages) != 4:
        raise ValueError("A lista de percentagens deve conter exatamente quatro valores.")
    
    # Verifique se todos os valores estão entre 0 e 100
    if not all(0 <= val <= 100 for val in percentages):
        raise ValueError("Todos os valores devem estar entre 0% e 100%.")
    
    # Posições das barras no eixo x
    x_pos = range(len(categories))
    
    # Criação do gráfico de barras com espaçamento entre as colunas
    plt.bar(x_pos, percentages, width=bar_width, color=['blue', 'green', 'red', 'purple'], align='center')
    
    # Adicionar rótulos nas barras
    for i, v in enumerate(percentages):
        plt.text(i, v + 1, f"{v}%", ha='center', va='bottom')
    
    # Título e rótulos dos eixos
    plt.title('Gráfico de Barras dos indicadores de maturidade')
    plt.xlabel('Maturidade dos dados')
    plt.ylabel('Percentagens (%)')
    
    # Definir os rótulos do eixo x para as posições das barras
    plt.xticks(x_pos, categories)
    
    # Limites do eixo y
    plt.ylim(0, 110)
    
    # Mostrar o gráfico
    #plt.show()
    plt.savefig(Salvar+'Grafico_Maturidade.png', format='png')#Salvar+'Grafico_FAIR.png'


def CalculoCompletude(df):
    missing_data = df.isnull().sum()
    total_data = np.product(df.shape)
    completeness_score = ((total_data - missing_data.sum()) / total_data)*100
    completeness_SCORE = round(completeness_score ,2)    
    
    return completeness_SCORE


def CalculoSingularidade(data):
    total_linhas = len(data)
    linhas_unicas = len(data.drop_duplicates())
    
    singularidade = (linhas_unicas / total_linhas) * 100
    Singularidade = round(singularidade ,2)    
    
    return Singularidade 


def CalculoConsistencia(df):
    
    total_elementos = df.shape[0] * df.shape[1]  # Total de elementos no DataFrame
    elementos_corretos = 0  # Contador para elementos corretos

    for coluna in df.columns:
        tipo_original = df[coluna].dtype
        
        if tipo_original == 'object':
            # Verificar se todos os valores são strings
            elementos_corretos += df[coluna].apply(lambda x: isinstance(x, str)).sum()
        else:
            # Verificar se todos os valores são numéricos
            elementos_corretos += df[coluna].apply(lambda x: isinstance(x, (int, float))).sum()

    # Calcular a porcentagem de dados corretos
    porcentagem_corretos = (elementos_corretos / total_elementos) * 100
    ConsisT = round(porcentagem_corretos, 2)
    
    return ConsisT


def CalculoValidade(df):
    
    try:
        # Definir colunas categóricas e numéricas
        categorical_features = df.select_dtypes(include='object').columns.tolist()
        numerical_features = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        
        # Criar transformadores para colunas categóricas e numéricas
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), numerical_features),
                ('cat', OneHotEncoder(), categorical_features)
            ]
        )
        
        # Criar o pipeline com o pré-processador e o modelo Isolation Forest
        pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                   ('model', IsolationForest(contamination="auto",random_state=42))])
        
        # Preparar os dados (X) e treinar o modelo
        X = df
        pipeline.fit(X)
        
        # Fazer previsões (1 para normal, -1 para anomalia)
        df['anomaly'] = pipeline.named_steps['model'].predict(pipeline.named_steps['preprocessor'].transform(X))
        
        # Calcular a porcentagem de validade
        # Nota: Aqui, consideramos dados normais (1) como válidos e anomalias (-1) como inválidos
        percent_valid = (df['anomaly'] == 1).mean() * 100
        percent_VALID = round(percent_valid, 2)
    
    except:
        percent_VALID = 1.0    
    
    return percent_VALID


def Completude(H,chave):
    try:
        
        if chave == '.csv':    
            df = pd.read_csv(H)
            completeness_score = CalculoCompletude(df)
        
        elif chave == '.xlsx' or chave == '.xls':     
            df = pd.read_excel(H)
            completeness_score = CalculoCompletude(df)
        
        elif chave == '.pdf':
            completeness_score = 0.0    
            
            #print(completeness_score)
    except:
        completeness_score = 1.0
    return completeness_score
    
    
def Singularidade(H, chave):
    try:
        
        if chave == '.csv':
    
            data = pd.read_csv(H)
            singularidade = CalculoSingularidade(data)
            
        elif chave == '.xlsx' or chave == '.xls':
            data = pd.read_excel(H)
            singularidade = CalculoSingularidade(data)
            
        elif chave == '.pdf':
            singularidade = 0.0    
    except:
        singularidade = 0.0        
        
    return singularidade
    

def Validade(H, chave):
    try:
        if chave == '.csv':
            df = pd.read_csv(H)
            df = df.dropna(inplace = False, axis=0) 
            df = df.astype({col: str for col in df.select_dtypes(include='object').columns})
            percent_valid = CalculoValidade(df)    
            
            return percent_valid        
        
        elif chave == '.xlsx' or chave == '.xls':    
            df = pd.read_excel(H)
            df = df.dropna(inplace = False, axis=0)
            df = df.astype({col: str for col in df.select_dtypes(include='object').columns})
            percent_valid = CalculoValidade(df)    
            
            return percent_valid 
        
        elif chave == '.pdf': 
            percent_valid = 0.0
            
    except:
        percent_valid = 0.0
    
    return percent_valid


def Consistencia(H, chave):
    
    try:
        if chave == '.csv':
            df = pd.read_csv(H)
            Consist = CalculoConsistencia(df)    
            
            return Consist        
        
        elif chave == '.xlsx' or chave == '.xls':    
            df = pd.read_excel(H)
            Consist = CalculoConsistencia(df)     
            
            return Consist 
        
        elif chave == '.pdf': 
            Consist = 0.0
            
    except:
        Consist = 0.0
    return Consist    
    
    
def ValidarMaturidade(H,Save,chave,Perm):
    #print(H,Save,chave,Perm)
    RegrasDefinidas =[]
    Salvar = Save
    #print(Perm)
    R = Completude(H,chave)
    RegrasDefinidas.append(R)
    R =Singularidade(H,chave)
    RegrasDefinidas.append(R)
    R = Validade(H,chave)
    RegrasDefinidas.append(R)
    R = Consistencia(H,chave)
    RegrasDefinidas.append(R)
    draw_bar_chart(RegrasDefinidas,Salvar,bar_width=0.5)    
    
    return RegrasDefinidas    
    
#ValidarMaturidade('C:/Users/belzi/Documents/DoutoradoLucas/indicadores/Versao_0.1/Scripts_novo/BasedadosT/Grajau_Ipvs_2010_1.csv','','.csv')    