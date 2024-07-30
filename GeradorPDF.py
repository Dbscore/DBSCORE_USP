import time
from unittest.mock import Base
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY,TA_CENTER,TA_LEFT,TA_RIGHT



def GerarPDF(Star,Salvar,BaseC,CHaveOrigem,Save1,Save2,relat,FairF):
    
    NSalve = BaseC.split(".")
    
    doc = SimpleDocTemplate(relat + 'Relatorio_Analise'+'_'+NSalve[0]+'.pdf',pagesize=letter,
                            rightMargin=72,leftMargin=72,
                            topMargin=72,bottomMargin=18)

    Story = [ ]
    nome = [ ]
    Estrela =[ ]
    
    #Variavel para apresentar ou não texto sobre as informações
    try: 
        C = CHaveOrigem[0]    
    except:
        C=[ ]
    nome.append(BaseC)
    #Estrela.append(Star)

    formatted_time = time.ctime()
    indicadores = ["Openness", "FAIR","Maturidade dados"]
    #nome = ['BaseIPVS.csv']
    Adicional = ' '
    Estrela = 0
    ArrList =[]
    separator = ' '
    Tamanho = 0

    for DD in Star.keys():    
        
        if Star[DD] == 1 or Star[DD] == 0:   
            Estrela= Estrela + Star[DD]
        
        elif Star[DD] == 0.25 or Star[DD] ==0.125 or Star[DD] ==0.5 or Star[DD] ==0.375 or Star[DD] ==0.625 or Star[DD]==0.875 or Star[DD]==0.8 or Star[DD]==0.75:
            ArrList.append('/'+ DD)
            Tamanho = len(ArrList)
            
    if BaseC[-3:]!= 'csv':
        if Tamanho>1:    
            DD = [separator.join(ArrList)]        
            Adicional = ' Entretanto, ressaltamos que por mais que parte das regras das estrelas (%s), foram atingida a base não respeitou todas as condições necessárias para conseguir essas estrelas.'%(DD[0])
        else:
            Adicional = ' Entretanto, ressaltamos que por mais que uma parte da regra da estrela "%s" foi atingida a base não respeitou todas as condições necessárias para conseguir essa estrela.'%(ArrList[0])            
    
    if BaseC[-3:] == 'csv' and ArrList !=[]:
        Adicional = ' Entretanto, ressaltamos que por mais que uma parte da regra da estrela "%s" foi atingida a base não respeitou todas as condições necessárias para conseguir essa estrela.'%(ArrList[0])

    if Estrela == 1:
            Resul = 'ela obteve a nota de nível de 1 estrela, a principal característica desse nível é que os dados estão presos em um documento. Dessa forma, para retirar os dados do documento, você vai ter que escrever um raspador com uma função específica para extrair as informações para um formato de manipulação acessível.'

    elif Estrela == 2:
        
            Resul = 'ela obteve a nota de nível de 2 estrelas, os dados estão acessíveis na Web em uma forma estruturada (isto é, legível por máquina), todavia, os dados ainda estão presos em um documento. Para obter os dados você depende de um software proprietário para realizar as manipulações e utilizar os dados.'

            IncrementHttps = ' a base não alcançou o nível 3, por não estar em um formato aberto (Open Format). Já o nível 4, não foi atingido pois todas a regras do nível 3 não foram alcançadas, por mais que a base foi acessada por uma URI. E no nível 5, faltou as conexões com outras URIs da Web. Portanto, a base não alcançou um nível maior na análise.'

    elif Estrela == 3:
        
            Resul = 'ela obteve a nota de nível de 3 estrelas, os dados não estão apenas disponíveis na Web mas agora qualquer um pode utilizar os dados facilmente. Por outro lado, ainda são "dados empacotados na Web". Dados empacotados na web são aqueles que não são totalmente estruturados para aproveitar o máximo de potencial que tem de alcance a web.'

            if Star['OF']!=0 and Star['URI']==1:

                IncrementHttps = ' a avaliação foi que a base alcançou o nível de estrela 3 (OL, RE, URI), mas com a ressalva de não estar em um formato aberto (Open Format) regra principal da estrela "OF".'

    elif Estrela == 4:
        
            Resul = 'ela obteve a nota de nível 4 estrelas (URI) de dados abertos na internet. Vale destacar que nessa categoria, os dados são classificados como "dados na Web". Os dados foram obtidos por meio de uma URI e podem ser compartilhados na Web. Uma das grandes vantagem da utilização de URIs, é que eles podem ser encontrados e consumidos por outras pessoas e máquinas de forma muito mais simplificada do que a disponibilização de um simples arquivo CSV ou outros formatos abertos.'

            IncrementHttps = 'um dos pontos que não fizeram a base alcançar o nível de 5 estrelas foi que sua conexão com outros dados ficam apenas restritas a sua URI. Como não foram encontradas informações de outras conexões com outras URIs da web, essa se torna sua limitação.'

    elif Estrela == 5:
        
            Resul = 'ela obteve a nota máxima de nível 5 estrelas (LD), os dados estão totalmente ligados a outros na Web por meio de URIs. Esses dados se beneficiam pelo "Efeito da rede" e podem se beneficar por ser uma forma de maior alcance de qualquer outra categoria. Geralmente esses dados estão no forma .RDF ou RDFa.'

    elif Estrela == 0:
            Resul = 'após realizado a análise a base atingiu o nível de 0 estrelas não conseguindo respeitar nenhuma regra estabelecida para cada uma das estrelas/categorias.'    


    logo = "QA.png"

    styles = getSampleStyleSheet()

    #Formatação_Texto

    #Titulo
    title1_style = styles['Heading1']
    title1_style.alignment = 1

    #Subtitulo 
    Subtitle_style = styles['Heading2']
    Subtitle_style.alignment = 1

    #Subtitulo1
    Subtitle1_style = styles['Heading3']
    Subtitle1_style.alignment = 1

    #Subtitulo2
    Subtitle2_style = styles['Heading4']
    Subtitle2_style.alignment = 1
    

    #Titulo
    Titulo = Paragraph("DBScore - Sistema de análise de qualidade de dados", title1_style)
    Story.append(Titulo)


    #Subtitulo

    Subtitle = Paragraph("Resumo dos resultados dos indicadores", Subtitle_style)
    Story.append(Subtitle)    

    
    #Nome Base_dados
    Subtitle = Paragraph('Base de dados analisada: %s'%nome[0], Subtitle1_style)
    Story.append(Subtitle)    
    
    #Espaço
    Story.append(Spacer(1, 12))

    ptext = '%s' % formatted_time
    Story.append(Paragraph(ptext,Subtitle2_style))
    
    #Espaço
    Story.append(Spacer(1, 10))

    im = Image(logo, 4*inch, 2*inch)
    Story.append(im)

    #Espaço
    Story.append(Spacer(1, 48))

    ptext = '''O Sistema avalia as bases de dados utilizando 3 indicadores (%s, %s e %s). O %s é um indicador criado pelo 
    Tim Berners-Lee o inventor da Web, para avaliar o nível de disponibilidade dos dados por meio de boas práticas no contexto de dados abertos na internet e se concentra em aspectos semânticos como estrutura, 
    uso de URIs e links. Essa métrica é composta por 5 categorias/estrelas (OL-Open Licence, RE-REused, OF-Open Format,URI-Uniform Resource Identifier e LD-Linked Data). 
    Os princípios do segundo indicador o %s — encontrabilidade, acessibilidade, interoperabilidade e reutilização — 
    definem um mínimo de práticas para promover a usabilidade dos dados. 
    O RDA FAIR Data Maturity Model Working Group propõe um modelo de maturidade referente aos princípios FAIR que consiste em indicadores, prioridades e métodos de avaliação. 
    Nesse sistema vamos utilizar um modelo intitulado FAIRsFAIR que reúnem as 17 regras mais importantes para identificar a maturidade dos dados. Já o terceiro indicador %s é uma métrica que foi baseada na técnica da NASA para hardware de voo e instrumentação, 
    consiste em utilizar cinco das perspectivas de maturidade que são: Completude, Singularidade, Consistência, Validade e Precisão. '''% (indicadores[0], 
                                                                                                    indicadores[1],
                                                                                                    indicadores[2],
                                                                                                    indicadores[0],
                                                                                                    indicadores[1],
                                                                                                    indicadores[2],
                                                                                                    )

    
    Story.append(Paragraph(ptext, styles["Normal"]))

    Story.append(Spacer(1, 24))          

    Subtitle = Paragraph("Openness", Subtitle_style)
    Story.append(Subtitle)

    Story.append(Spacer(1, 12))

    ptext = 'De maneira geral, a base foi processada e avaliada levando em consideração todas as regras do Openness. Assim, ' + Resul + Adicional 

    #styles.add(ParagraphStyle(name='Justify', alignment=TA_CENTER)) #Justificar o textou, centralizar e etcc ..   
    Story.append(Paragraph(ptext, styles["Normal"]))
    

    if C != [] and Estrela==3 and Star['OF']!=0 and Star['URI']==1:
        Story.append(Spacer(1, 4))

        ptext = 'O site/link processado é o %s, '%(C) + IncrementHttps         
        #styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        #Story.append(Paragraph(ptext, styles["Justify"]))
        Story.append(Paragraph(ptext, styles["Normal"]))

    elif C != [] and Estrela==4:
        
        Story.append(Spacer(1, 4))

        ptext = 'O site/link processado é o %s, '%(C) + IncrementHttps
        #styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        #Story.append(Paragraph(ptext, styles["Justify"]))
        Story.append(Paragraph(ptext, styles["Normal"]))
    
    Story.append(Spacer(1, 8))

    ptext = 'Para melhor explicar a avaliação, desenvolvemos uma forma de visualização para representar o nível que foi alcançado pela base de dados através das análises. A figura abaixo é um gráfico do tipo radar que é uma exibição de dados na forma de um gráfico bidimensional. O gráfico varia na pontuação de "0" significando que as regras não foram atingidas para alcançar o determinado nível. Já as pontuações com valores acima de 0 e abaixo de 1, como por exemplo: i) 0.2, ii) 0.4, iii) 0.6 e iv) 0.8 significam que nível atingido pela base respeitou parcialmente as regras. E as pontuações com o valor 1, indicam que todas as regras da base foram atingidas a partir da realização da análise na base.' 
    
    Story.append(Paragraph(ptext, styles["Normal"]))

    img1 = Salvar+'Openness_radar.png'
    img1 = Image(img1, 4*inch, 4*inch)
    Story.append(img1)

    Story.append(Spacer(1, 12))

    ptext = 'Nesta etapa do relátorio, é apresentado uma figura com uma tabela de relação de regras que “não” foram atingidas conforme a análise. A proposta dessa tabela é permitir que o publicador ou consumidor dos dados possam ter uma visão mais ampla de como melhorar a disponibilidade do dado na web e também como está a estrutura da base de dados que vai ser processada/utilizada. Assim, pretendemos diminuir o tempo que pode se perder na parte de investigação da base de dados e acelerar processos de desenvolvimento de um modelo para uma melhor tomada de decisão.'

    Story.append(Paragraph(ptext, styles["Normal"]))

    Story.append(Spacer(1, 12))

    if Estrela==1 or Estrela==0:
        
        img1 = Salvar+'RegrasN.png'
        img1 = Image(img1, 10*inch, 3*inch)
        Story.append(img1)
    
    elif Estrela != 1:
        
        img1 = Salvar+'RegrasN.png'
        img1 = Image(img1, 10*inch, 2*inch)
        Story.append(img1) 

        
    Story.append(Spacer(1, 20))

    Subtitle = Paragraph("Princípios FAIR ", Subtitle_style)
    Story.append(Subtitle)

    Story.append(Spacer(1, 20))

    ptext = "Os Princípios FAIR são um acrônimo para Findable (localizável), Accessible (acessível), Interoperable (interoperável) e Reusable (reutilizável). Para ser *LOCALIZÁVEL* (FINDABLE)- F1. Os (meta)dados são atribuídos a um identificador persistente, único e global; F2. Os dados são descritos com metadados ricos; F3. Os metadados incluem, de forma clara e explícita, o identificador dos dados que descrevem. F4. Os (meta)dados são registrados ou indexados em um recurso pesquisável. Para ser *ACESSÍVEL* (ACCESSIBLE) - A1. Os (meta)dados são recuperáveis por seu identificador, usando-se um protocolo de comunicação padronizado; A1.1. O protocolo é aberto, gratuito e universalmente implementável; A1.2. O protocolo possibilita um procedimento de autenticação e autorização, quando necessário A2; Os metadados são acessíveis, mesmo quando os dados não estão mais disponíveis. Para ser *INTEROPERÁVEL* (INTEROPERABLE) - I1. Os (meta)dados usam uma linguagem formal, acessível, compartilhada e amplamente aplicável para representar o conhecimento; I2. Os (meta)dados usam vocabulários que seguem os Princípios FAIR; I3. Os (meta)dados incluem referências qualificadas para outros (meta)dados. Para ser *REUTILIZÁVEL* (REUSABLE) - R1. Os (meta)dados são ricamente descritos com uma pluralidade de atributos precisos e relevantes; R1.1. Os (meta)dados são disponibilizados com uma licença de uso de dados clara e acessível; R1.2. Os (meta)dados estão associados a uma proveniência detalhada; R1.3. Os (meta)dados estão de acordo com padrões comunitários relevantes para o domínio."
    
    Story.append(Paragraph(ptext, styles["Normal"]))

    Story.append(Spacer(1, 12))

    ptext = "Na avaliação do conjunto de dados foi utilizado o conceito de cinco níveis de maturidade de indicadores, criado pelo grupo RDA FAIR Data Maturity Model Working Group. O índice varia do nível 0 (não FAIR/regras não atendidas) até o nível 5 (respeitando as regras do FAIR). Abaixo é apresentando um gráfico com os resultados obtidos após a análise da base de dados. Ressaltando que a média atingida pela base avaliada pelos indicadores FAIR foi: %s, considerando que a nota miníma é 1 e a nota maxima é 5 para atingir todos os requisitos."%(FairF)
    
    Story.append(Paragraph(ptext, styles["Normal"]))


    img1 = Save1+'Grafico_FAIR.png'
    img1 = Image(img1, 4*inch, 4*inch)
    Story.append(img1)
    
    Subtitle = Paragraph("Maturidade dos dados", Subtitle_style)
    Story.append(Subtitle)

    Story.append(Spacer(1, 20))
    
    ptext = ''' A maturidade dos dados foi avaliada de forma semelhante à maturidade de hardware utilizando os Níveis de Prontidão Tecnológica (Technology Readiness Levels - TRLs) da NASA, que são um tipo de sistema de medição utilizado para avaliar o nível de maturidade de uma determinada tecnologia. Embora os TRLs sejam específicos para tecnologia e hardware, 
    podemos fazer uma analogia e criar um sistema simplificado de níveis de prontidão dos dados (Data Readiness Levels - DRLs). Segue abeixo o resultado em um gráfico de barras que varia de 0 a 100 por cento, sendo valores mais próximo de 100 uma base bem mais estruturada e valores próximos a 0 uma base não-estruturada.'''
    
    Story.append(Paragraph(ptext, styles["Normal"]))
    
    img3 = Save2+'Grafico_Maturidade.png'
    img3 = Image(img3, 4*inch, 4*inch)
    Story.append(img3)
    
    doc.build(Story)