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
import re
import warnings
import requests
from urllib.parse import urlparse, urlunparse

warnings.simplefilter("ignore", UserWarning)
plt.switch_backend('agg')

#Referencia site : "https://satifyd.dans.knaw.nl/"

def VerificaLicenca(Perm):
    
    Verif=['PDDL','ODC-by','CC0','CC-BY','ODbL','CC-BY-SA']
    aux = Perm in Verif

    return aux
    
def Grafico_circular(RegrasDefinidas,Salvar):

    categories = ['Findable', 'Accessible', 'Interoperable','Reusable']
    categories =[*categories, categories[0]]
    G = RegrasDefinidas
    G=[*G,G[0]]
    label_loc = np.linspace(start=0, stop=2 * np.pi, num=len(G))
    fig, ax = plt.subplots(figsize=(12, 5))
    plt.figure(figsize=(8, 8))
    plt.subplot(polar=True)
    plt.plot(label_loc, G, label='Restaurant 1')
    lines, labels = plt.thetagrids(np.degrees(label_loc), labels=categories)
    plt.title('Avaliação dos príncipios FAIR', size=20)
    lines, labels = plt.thetagrids(np.degrees(label_loc), labels=categories)  
    plt.savefig(Salvar+'Grafico_FAIR.png', format='png')

# Função para pontuar a Findability
def pontuar_findability(url_or_path,chave,Perm):
    
    if url_or_path == 'https://servicodados.ibge.gov.br/api/v3/agregados':
        return 4.0  # Local file is perfectly findable 
    else:
        return 1.0  # Not findable

# Função para pontuar a Accessibility
def pontuar_accessibility(url_or_path,chave,Perm):
    
    if url_or_path == 'https://servicodados.ibge.gov.br/api/v3/agregados':
        VPerm = VerificaLicenca(Perm) 
        if VPerm == True:
            return 5.0  # Local file is perfectly accessible
    else:
        VPerm = VerificaLicenca(Perm) 
        
        if VPerm == False and Perm == "Não informado":
            return 1.0  # Not accessible
        
        elif VPerm == True and Perm != "Não informado":
            return 2.5
        
        elif VPerm == False and Perm != "Não informado":
            return 2.5

# Função para pontuar a Interoperability
def pontuar_interoperability(url_or_path,chave,Perm):
    # This function should check for standards and formats for interoperability
    VPerm = VerificaLicenca(Perm)
    if url_or_path == 'https://servicodados.ibge.gov.br/api/v3/agregados':
        return 3.75  # CSV format is typically interoperable
    else:
        if chave == '.csv':
            return 2.9
        elif chave == '.pdf' and VPerm == True:
            return 1.9   
        elif chave == '.pdf' and VPerm == False:
            return 1.0
        
        elif chave == '.xlsx' or chave == '.xls':
            return 1.9  # Not interoperable

# Função para pontuar a Reusability
def pontuar_reusability(url_or_path,chave,Perm):
    VPerm = VerificaLicenca(Perm)
    # This function should check for metadata, documentation, and licensing
    # Here we only simulate the presence of these elements
    if url_or_path == 'https://servicodados.ibge.gov.br/api/v3/agregados': 
        return 5.0  # Assumed to be reusable to some extent
    else:  
        if chave == '.csv':
            VPerm = VerificaLicenca(Perm)
            if VPerm == True:
                return 3.0
            else:
                return 2.25        
        
        elif chave == '.pdf':
            VPerm = VerificaLicenca(Perm)
            if VPerm == True:
                return 1.7
            else:
                return 1.0   
        elif chave == '.xlsx' or chave == '.xls':
            VPerm = VerificaLicenca(Perm)
            if VPerm == True:
                return 3.0
            else:
                return 2.25  # Not interoperable


def ValidarRegras(H,Save,chave,Perm):
    RegrasDefinidas =[]
    Salvar = Save
    #print(Perm)
    R = pontuar_findability(H,chave,Perm)
    RegrasDefinidas.append(R)
    R =pontuar_accessibility(H,chave,Perm)
    RegrasDefinidas.append(R)
    R =pontuar_interoperability(H,chave,Perm)
    RegrasDefinidas.append(R)
    R = pontuar_reusability(H,chave,Perm)
    RegrasDefinidas.append(R)
    #print(RegrasDefinidas)
    
    Grafico_circular(RegrasDefinidas,Salvar)
    
    if RegrasDefinidas:
        soma = sum(RegrasDefinidas)
        media = soma/len(RegrasDefinidas)
        
    return media,RegrasDefinidas    