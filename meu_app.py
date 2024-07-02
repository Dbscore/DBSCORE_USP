import streamlit as st
import pandas as pd
import os
import zipfile
import shutil
import time
import re
import glob
#from my_bibliotec.Start import *
from datetime import datetime

data_e_hora_atuais = datetime.now()
data_e_hora_em_texto = data_e_hora_atuais.strftime("%d-%m-%Y_%H_%M_%S")

st.set_page_config(page_title="DBscore",layout="wide", menu_items={'Get Help':'mailto:lucasaugusto.vb@gmail.com',
'Report a bug': 'mailto:lucasaugusto.vb@gmail.com','About': " Essa ferramenta foi feita pelo Lucas Brito aluno de Doutorado da USP/ICMC!"
})#layout="wide"

codig = ''
LicencaDados= ''

def processar_dadosLocal(caminho_arquivo,LicencaDados,codig):
    Caminhorelat="Dados local"
    #Caminhorelat = AnaliseDBscore(caminho_arquivo,LicencaDados,codig)
    
    return Caminhorelat   
    
    
def processar_dadosWeb(caminho_arquivo,LicencaDados,codig):
    Caminhorelat = "Dados Web"
    #Caminhorelat = AnaliseDBscore(caminho_arquivo,LicencaDados,codig)
    
    return Caminhorelat    
    
    
def download_pasta(Relat):
        print(Relat)
#     # Define o nome do arquivo ZIP que será criado
#     nome_arquivo = 'Resultados_'+ data_e_hora_em_texto+'.zip'
#     caminho_pasta = Relat #Caminho para da pasta de resultados
# # Cria um arquivo ZIP com a pasta especificada
#     with zipfile.ZipFile(nome_arquivo, 'w', zipfile.ZIP_DEFLATED) as zip:
#         # Adiciona os arquivos da pasta ao ZIP
#         for pasta_raiz, pastas, arquivos in shutil.os.walk(caminho_pasta):
#             for arquivo in arquivos:
#                 caminho_completo = shutil.os.path.join(pasta_raiz, arquivo)
#                 #print(caminho_completo)
#                 zip.write(caminho_completo, arcname=caminho_completo[len(caminho_pasta)+1:])
    
#     # Faz o download do arquivo ZIP
#     with open(nome_arquivo, 'rb') as f:
#         bytes_arquivo = f.read()
#         st.download_button(
#             label='Download Resultados',
#             data=bytes_arquivo,
#             file_name=nome_arquivo,
#             mime='application/zip'
#         )


with st.container():    
    # Define o título da página
    st.title('DBscore')
    
    # Define a introdução
    st.write('''O **_DBscore_** é uma ferramenta que reúne as melhores práticas para validar e 
    mensurar a qualidade das base de dados, de forma automática com auxílio de bibliotecas e 
    funções que replicam eficientemente regras que permitem verificar pontos cruciais de uma base de dados. 
    Os indicadores no sistema, se completam no objetivo de oferecer 
    uma visão mais ampla de condições mínimas que respeitam o compartilhamento, maturidade dos dados e sua integridade. Os principais indicadores utilizados 
    por esta ferramenta são: ''')
    
    st.write('''**_FAIR_**: É um princípio, criado para guiar a produção, o armazenamento e o uso de dados 
    científicos e tecnológicos na era digital. Eles visam ajudar a garantir que os dados sejam produzidos e 
    armazenados de maneira consistente, confiável e acessível, a fim de maximizar seu valor e reutilização. [Mais informações](https://fairsfair.eu/)''')
    
    st.write('''**_Openness_**:  Esse indicador verifica a abertura dos dados, validando sua disponibilidade, 
    acessibilidade, descrição, licença de uso e principalmente seu recurso para acesso. [Mais informações](https://5stardata.info/en/)''')
    
    st.write('''**_Modelagem de Maturidade dos dados_**:  Essa métrica foi compilada baseada na técnica da NASA para hardware de voo, onde é validado alguns aspectos que foram adaptado para o sistema, sendo eles: Completude, Singularidade, Consistência, Validade e Precisão. [BETA..](https://esto.nasa.gov/trl/)''')
    
    # st.write('''**_Medidas de qualidade de dados_**:  Essa métrica utiliza conceitos da ISO (Organização Internacional de Normalização) que estabelece os princípios para descrever a qualidade dos dados. Ela define componentes para descrever a qualidade dos dados, estrutura de conteúdo de um
    # registro para medidas de qualidade de dados e também se baseia em modelo de vocabulário de qualidade de dados DQV (Data Quality Vocabulary). [Em construção..](https://www.w3.org/TR/vocab-dqv/#intro)''')
    


with st.container():
    Opcao = st.selectbox("Selecione uma das opções:", [" ","API/HTTPs","Arquivo Local"])

st.write('\n')
st.write('\n')



with st.container():
    
    if Opcao == "API/HTTPs":     
        
        #caminho_salvar = st.text_input('Escolha o local para salvar o resultado da análise: ')
        caminho_arquivo = st.text_input('Digite o caminho do arquivo API/HTTPs:  ') 
            
        cAPI = []
        ListaHttPsF_http = ['https://servicodados.ibge.gov.br/api/v3/agregados','']
        cAPI.append(caminho_arquivo)
        r_api = re.compile("api")
        API = list(filter(r_api.search,cAPI))
        
        if caminho_arquivo in ListaHttPsF_http:
            if API ==[]:
                pass
            else:
                codig = st.text_input('Adicionar Cód ref (Baseado com Assunto que gostaria de buscar na tabela abaixo):  ')
                df= pd.read_csv('CodigoIBGE_Base.csv', index_col= None)
                df = df.reset_index(drop=True)
                CodValidos = df['Cód ref.'].tolist()
                st.dataframe(df)
        else: 
            st.warning("Site/API não compilado para a ferramenta DBScore!",icon="⚠️")
            
                 
    elif Opcao == "Arquivo Local":
        # Define os campos para o usuário digitar o caminho do arquivo e escolher o local para salvar
        
        caminho_arquivo = st.text_input('Adicione o caminho/local para importar a base de dados:  ')
        LicencaDados = st.text_input('Digite a liçenca dos dados (Se não souber digite - Não sei -): ')
        
    
with st.container():    
    
    # Define o botão para processar os dados
    if Opcao == "API/HTTPs":
        
        API = list(filter(r_api.search,cAPI))
        
        #print(API)
        
        if API ==[ ] and caminho_arquivo in ListaHttPsF_http:
        
            if Opcao != '' and caminho_arquivo != '': 
                
                if st.button('Realizar análise'):
                    with st.spinner('Processando Análise...'):
                        Relat=processar_dadosWeb(caminho_arquivo,LicencaDados,codig)                    
                        st.success('Finalizado!')
                        download_pasta(Relat)
        
        else:
            
            if codig != '': 
                
                if st.button('Realizar análise'):
                    with st.spinner('Processando Análise...'):
                        Relat=processar_dadosWeb(caminho_arquivo,LicencaDados,codig)                    
                        st.success('Finalizado!')
                        
                        download_pasta(Relat)   
    
    elif Opcao == "Arquivo Local":
        
        if Opcao != '' and caminho_arquivo != '' and  LicencaDados != '': 
            
            if st.button('Realizar análise'):
                 with st.spinner('Processando Análise...'):
                    Relat = processar_dadosLocal(caminho_arquivo,LicencaDados,codig)                    
                    st.success('Finalizado!')
                    download_pasta(Relat)        
        

            
                
                
                                 
