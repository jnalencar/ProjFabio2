import json
import pandas as pd
import os
import requests
import sys

if((os.path.isfile('CNPJ.txt')) == False):
    print("O bloco de notas a ser lido deve ter o nome CNPJ (com letras maiusculas) e deve estar na mesma pasta que este programa.")
    input()
    sys.exit()
    
arquivo = open('CNPJ.txt', 'r')
cnpj_beneficiadas = arquivo.readlines()
arquivo.close()
cnpjs_beneficiadas = [cnpj.replace('\n', '') for cnpj in cnpj_beneficiadas]

url = 'http://compras.dados.gov.br/contratos/v1/contratos.json?cnpj_contratada='
vetor_nome_entidade = []
vetor_cnpj_contratada = []
vetor_valor_inicial = []
vetor_objeto = []
vetor_uasg = []
vetor_nome_uasg = []
vetor_tipo_de_licitacao = []
vetor_numero_licitacao = []
vetor_numero_contrato = []
vetor_numero_aditivos = []
vetor_link_licitacao = []
vetor_link_contrato = []
vetor_data_assinatura = []
vetor_erro_licitacao = []
l = len(cnpjs_beneficiadas)

def check_modalidade(tipo_de_licitacao, cnpj, numcontrato):
    tipos = ['NULL','CONVITE','TOMADA DE PREÇOS','CONCORRÊNCIA','CONCORRÊNCIA INTERNACIONAL','PREGÃO','DISPENSA DE LICITAÇÃO','INEXIGIBILIDADE DE LICITAÇÃO']
    if tipo_de_licitacao is None:
        return tipos[0]
    elif tipo_de_licitacao >= 0 and tipo_de_licitacao <= 7:
        return tipos[tipo_de_licitacao]
    #ELIF para resolver problema referente ao beneficiado com cnpj = 42270181000116 referente ao RJ
    elif tipo_de_licitacao == 33:
        return 'CONCORRÊNCIA POR TÉCNICA E PREÇO'
    #ELIF para resolver problema referente a um beneficiado do DF
    elif tipo_de_licitacao == 22:
        return 'TOMADA DE PREÇOS POR TÉCNICA E PREÇO'
    else:
        vetor_erro_licitacao.append([tipo_de_licitacao,cnpj, numcontrato])
        return 'ERROR'

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()
j=0
printProgressBar(0, l, prefix = 'Criando arquivos TXT\tProgresso:', suffix = 'Completo ' + str(j)+ '/' + str(len(cnpjs_beneficiadas)), length = 50)
for j, cnpj in enumerate(cnpjs_beneficiadas):
    nomearq = cnpj + '.txt'
    urlcnpj = url + cnpj
    i = 0
    #printProgressBar(j + 1, l, prefix = 'Criando arquivos TXT\tProgresso:', suffix = 'Completo ' + str(j+1)+ '/' + str(len(cnpjs_beneficiadas)), length = 50)
    if((os.path.isfile(nomearq)) == False):
        while(i<5):
            try:
                #print('Tentativa de extracao de dados do cnpj =',cnpj,'iniciada.')
                page = requests.get(urlcnpj, verify = False).text
            except requests.ConnectionError:
                #print()
                #print("Erro na extracao de dados do cnpj =",cnpj)
                i = i+1
                #print("Tentativa",i,"de 5.")
            else:
                #print('Extracao de dados bem sucedida.\nCriando arquivo txt...')
                i = 5
        with open(nomearq, 'w') as arq:
            arq.write(page)
            #print('Arquivo criado com sucesso.')
j=0
printProgressBar(0, l, prefix = 'Organizando dados\tProgresso:', suffix = 'Completo ' + str(j)+ '/' + str(len(cnpjs_beneficiadas)), length = 50)
for j, cnpj in enumerate(cnpjs_beneficiadas):
    nomearq = cnpj + '.txt'
    try:
        with open(nomearq,"r", encoding = 'utf-8') as file: #ISO-8859-1 ou utf-8 #, errors = 'ignore' 
            info_beneficiada = file.read()
            dicion = json.loads(info_beneficiada)
    except UnicodeDecodeError:
        with open(nomearq,"r", encoding = 'ISO-8859-1') as file: #ISO-8859-1 ou utf-8 #, errors = 'ignore' 
            info_beneficiada = file.read()
            dicion = json.loads(info_beneficiada)
            
    for i in range(len(dicion['_embedded']['contratos'])):
        contrato = []
        nome_entidade = dicion['_embedded']['contratos'][i]['_links']['fornecedor']['title']
        cnpj_contratada = dicion['_embedded']['contratos'][i]['cnpj_contratada']
        valor_inicial = dicion['_embedded']['contratos'][i]['valor_inicial'] #Pode ser null (definir default)
        objeto = dicion['_embedded']['contratos'][i]['objeto']
        uasg = dicion['_embedded']['contratos'][i]['uasg']
        nome_uasg = dicion['_embedded']['contratos'][i]['_links']['uasg']['title']
        tipo_de_licitacao = dicion['_embedded']['contratos'][i]['modalidade_licitacao'] #if != null
        numero_licitacao = dicion['_embedded']['contratos'][i]['licitacao_associada']
        numero_contrato = dicion['_embedded']['contratos'][i]['identificador']
        numero_aditivos = dicion['_embedded']['contratos'][i]['numero_aditivo']
        link_licitacao = dicion['_embedded']['contratos'][i]['_links']['licitacao']['href']
        link_contrato = dicion['_embedded']['contratos'][i]['_links']['self']['href']
        data_assinatura = dicion['_embedded']['contratos'][i]['data_assinatura']
        vetor_nome_entidade.append(nome_entidade)
        vetor_cnpj_contratada.append(cnpj_contratada)
        if valor_inicial == None:
            valor_inicial = 'Nao Informado'
        vetor_valor_inicial.append(valor_inicial)
        vetor_objeto.append(objeto)
        vetor_uasg.append(uasg)
        vetor_nome_uasg.append(nome_uasg)
        vetor_tipo_de_licitacao.append(check_modalidade(tipo_de_licitacao, cnpj, numero_contrato))
        vetor_numero_licitacao.append(numero_licitacao)
        vetor_numero_contrato.append(numero_contrato)
        vetor_numero_aditivos.append(numero_aditivos)
        link_licitacao = "http://compras.dados.gov.br" + link_licitacao
        vetor_link_licitacao.append(link_licitacao)
        link_contrato = "http://compras.dados.gov.br" + link_contrato
        vetor_link_contrato.append(link_contrato)
        vetor_data_assinatura.append(data_assinatura)
    #printProgressBar(j + 1, l, prefix = 'Organizando dados\tProgresso:', suffix = 'Completo ' + str(j+1)+ '/' + str(len(cnpjs_beneficiadas)), length = 50)

df1 = pd.DataFrame({'nome_entidade':vetor_nome_entidade, 'cnpj_contratada':vetor_cnpj_contratada, 'valor_inicial':vetor_valor_inicial,
                    'objeto':vetor_objeto,'uasg':vetor_uasg, 'nome_uasg':vetor_nome_uasg, 'tipo_de_licitacao':vetor_tipo_de_licitacao,
                    'numero_licitacao':vetor_numero_licitacao, 'numero_contrato':vetor_numero_contrato, 'numero_aditivos':vetor_numero_aditivos,
                    'link_licitacao':vetor_link_licitacao, 'link_contrato':vetor_link_contrato, 'data_assinatura':vetor_data_assinatura})
datatoexcel = pd.ExcelWriter('DadosContratos.xlsx')
df1.to_excel(datatoexcel)
datatoexcel.save()
print('Planilha pronta!')
if vetor_erro_licitacao != []:
    for erro in vetor_erro_licitacao:
        print('Por favor verificar manualmente o contrato de numero:',erro[2],'vinculado ao cnpj:',erro[1])     
    print('Se essa lista estiver muito grande me chama que é simples de resolver! Pode ter passado uma modalidade de contrato despercebido.')
    print('Para encontrar de maneira simples na planilha, basta filtrar a planilha na coluna "tipo_de_licitacao" e procurar pela palavra ERRO.')
else:
    print('Sem erros encontrados')
input()
sys.exit()
