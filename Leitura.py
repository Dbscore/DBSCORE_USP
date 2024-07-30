
import pandas as pd
import tabula
from zipfile import ZipFile
from os import chdir, getcwd, listdir
import os
import re
import PyPDF2
import wget 
import requests
import glob
import filecmp
from bs4 import BeautifulSoup
from IBGE import *
import shutil
import chardet

def Entrada_arquivo():
    e = input("Digite o caminho do arquivo ou HTTPs para verificação: ")
    return e


def Permissao():
    l = input("Você sabe qual é a licença do dado? Informe se possível: ")
    return l    


def Arq_csv(TipoArquivo,Permissao):


    BaseDados = pd.read_csv(TipoArquivo)
    sizeT = len(BaseDados) 
    
    if sizeT>1 and sizeT<=1000: 
         df1= BaseDados        
    
    else:    
        df1 = BaseDados.sample(1000)
   
    P=Permissao
    endereco = TipoArquivo
    chave = '.csv'

    return df1,P,endereco,chave


def Arq_xls(TipoArquivo,Permissao):

    BaseDados = pd.read_excel(TipoArquivo)

    #verificar a estrutura da base excel
    ColunasE= ['Unnamed: 1','Unnamed: 2']
    ColunasBase = list(BaseDados.columns)
    Colun= ColunasE[0]

    Verifica = Colun in ColunasBase

    #####_Verifica se a base está lendo corretamente ..
    
    i=1
    
    if Verifica:
    
        BaseDados = pd.read_excel(TipoArquivo,skiprows=range(0,i))
        ColunasBase = list(BaseDados.columns)    
        
    
    else:
        pass

    P=Permissao
    endereco = TipoArquivo
    chave = '.xlsx'    
    
        
    return BaseDados,P,endereco,chave


def Arq_zip(TipoArquivo):
    
    ListZ = [ ]

    frase = re.split("/", TipoArquivo[0])
    out = frase[-1]
    NomPasta = re.sub(r'[^\w\s]','',out)
    NomPasta = NomPasta + '/'
    endF = 'BaseDados/Arquivos_ZIP/'+ NomPasta
    try:
        os.makedirs(endF)
    except:    
        pass
    
    ArquivoOrigem = TipoArquivo[0]
    ZipFile(ArquivoOrigem).extractall(endF)

    chdir(endF)#Importante
    #print(getcwd())
    
    dirlist = os.listdir(getcwd()) 
    
    for i in dirlist:
    
        filename = os.path.abspath(i) 
        ListZ.append(filename)  
    
    return ListZ


def Arq_web(TipoArquivo,codig):

    r_api = re.compile("api")
    API = list(filter(r_api.search, TipoArquivo))
    #print(API)
    
    if API ==[ ]:

        def Limpa_ArquivosDuplicados(dir_path):

            file_lst = []

            for i in glob.glob(dir_path + '/**/*', recursive=True):
                if os.path.isfile(i):
                    file_lst.append(i)    

            for x in file_lst:
                for y in file_lst:
                        if x != y and os.path.exists(x) and os.path.exists(y):
                                if filecmp.cmp(x, y):
                                        os.remove(y)   

        url = TipoArquivo[0]
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')

        urls = []
        Downl= [ ]

        for link in soup.find_all('a'):
            Downl.append(link.get('href'))    

        #Extrair valores None que prejudica a manipulação da base

        Downl = [x for x in Downl if x is not None]


        #Extrair só os link importantes nos formatos especificados

        r1 = re.compile(".*zip|.*xlsx|.*xls|.*csv|.*pdf")
        Downl1 = list(filter(r1.match, Downl))

        endH = 'BaseDados/HTTPS/DownloadDadosHTTPS/'

        try:
            os.makedirs(endH)
        except:    
            pass

        C = getcwd()+'/' #Pegar o caminho original

        Files_save = C + endH


        for item in Downl1:
            url_origem = item
            try:
                filename = wget.download(url_origem,Files_save)
            except Exception as exc:
                print(f"wget failed: {str(exc)}")


        dir_path = Files_save

        #Retira arquivos duplicados
        Limpa_ArquivosDuplicados(dir_path)
        
        #Trata os nome dos arquivos

        #1-Listar todos os arquivos da pasta em uma lista
        caminhos = [os.path.join(dir_path, nome) for nome in os.listdir(dir_path)]

        #Lista de elementos_tirar no nome e renomear a tabela

        pattern = "[,&^*!!:%\$\s]+"

        CaminhosN = [ ]

        #Tratamento do nome do arquivo da pasta 
        for i in caminhos:     
            frase = re.split("/",i)
            out = frase[-1]    
            NomPasta = re.sub(r'[0-9]+', '',out)
            NomPasta = re.sub(pattern,"_",NomPasta)
            os.rename(i,dir_path+NomPasta)

        temp = [os.path.join(dir_path, nome) for nome in os.listdir(dir_path)]  

        for i in temp:
            frase = re.split("/",i)
            out = frase[-1]
            out = re.split("_",out)
            out1 = out[-1]
            out1 = re.split(r'[^\w\s]',out1)
            Nome_real=out[0]  +out[1] +'.'+ out1[-1]
            os.rename(i,dir_path+Nome_real)

        CaminhosN = [os.path.join(dir_path, nome) for nome in os.listdir(dir_path)]    
    
        frase1 = re.split("/", url)
        out1 = frase1[-2]
        BPasta = out1 + '_' + 'Https'
    
    else:
        CaminhosN,BPasta = Extrair_Base_IBGE(TipoArquivo[0],codig)
    
    return CaminhosN,BPasta


def Arq_pdf(TipoArquivo,Permissao):

    #Pegar_Informações PDF(textual/Paginas e etcc)
    
    pdfFileObj = open(TipoArquivo, 'rb') 
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
    Pag = pdfReader.numPages

    lista_tabelas = tabula.read_pdf(TipoArquivo, encoding='utf-8', pages='1')
   
    if lista_tabelas == []:
        
        BaseDados = 0
        P=Permissao
        endereco = TipoArquivo
        chave = '.pdf' 
    else:
        
        dado = lista_tabelas[0]
        dado.to_csv('DataframePDF.csv')
        
        with open('DataframePDF.csv', 'rb') as f:
            resultEnc = chardet.detect(f.read())
         
    
        BaseDados = pd.read_csv('DataframePDF.csv', encoding=resultEnc['encoding'])
        P=Permissao
        endereco = TipoArquivo
        chave = '.pdf'

    return BaseDados,P,endereco,chave   
    
        
def Apagar_Criar_Pastas():
    
    Caminho_result ='Resultados/Openness' 
    Caminho_result1 = 'Resultados/FAIR'
    Caminho_result2 = 'Resultados/Maturidade'
    Relatorio = 'Resultados/Relatorio_Tabela/'
    
    # Apagar pasta e suas raizes .... 
    try:
        shutil.rmtree('Resultados')
        
    except:
        pass
    
    try:
        shutil.rmtree('BaseDados')
        
    except:
        pass
    
    try:
        shutil.rmtree('HTTPS')
        
    except:
        pass
        
    #Criar novas pastas...    
    
    try:
        os.makedirs(Caminho_result)
    
    except:    
        pass

    try:
        os.makedirs(Caminho_result1)
    
    except:    
        pass
        
    try:
        os.mkdir('BaseDados')
        os.makedirs(Relatorio)
    except:
        pass      
        
    try:
        os.makedirs(Caminho_result2)
    
    except:    
        pass    
        
