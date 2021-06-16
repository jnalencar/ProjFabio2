import json
import pandas as pd
#url = 'http://compras.dados.gov.br/contratos/v1/contratos.json?cnpj_contratada=19452818000173'
#url = "http://compras.dados.gov.br/contratos/v1/contratos.json?uasg=20001&order_by=data_assinatura&order=desc"
i=0
#lista_cnpjs_beneficiadas_rj = ['01236254000176','02385669000174','03033006000153','03438229000109','03447568000143','03508097000136','03848688000152','04213923000182','04871657000185','05021674000196','05422000000101','05979994000153','06220430000103','08189277000116','19452818000173','24260951000168','27901719000150','28638393000182','30020705000131','30022727000130','30036685000197','30277685000189','32504995000114','33469164000111','33469172000168','33641663000144','33754482000124','33798026000186','33868654000352','34174896000147','40226946000195','42270181000116']
vetor_classes = []
vetor_de_vetores =[]

arquivo = open('CNPJDF.txt', 'r')
cnpj_beneficiadas = arquivo.readlines()
arquivo.close()
lista_cnpjs_beneficiadas = [cnpj.replace('\n', '') for cnpj in cnpj_beneficiadas]

def check_modalidade(tipo_de_licitacao):
    tipos = ['NULL','CONVITE','TOMADA DE PREÇOS','NULL','CONCORRÊNCIA INTERNACIONAL','PREGÃO','DISPENSA DE LICITAÇÃO','INEXIGIBILIDADE DE LICITAÇÃO']
    if tipo_de_licitacao is None:
        return tipos[0]
    #ELIF para resolver problema referente ao beneficiado com cnpj = 42270181000116
    elif tipo_de_licitacao == 33:
        return 'CONCORRÊNCIA POR TÉCNICA E PREÇO'
    else:
        return tipos[tipo_de_licitacao]
        
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

for cnpj in lista_cnpjs_beneficiadas:
    nomearq = cnpj + '.txt'
    with open(nomearq,"r", encoding = 'ISO-8859-1') as file:
        print('Arquivo',nomearq)
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
        vetor_tipo_de_licitacao.append(check_modalidade(tipo_de_licitacao))
        vetor_numero_licitacao.append(numero_licitacao)
        vetor_numero_contrato.append(numero_contrato)
        vetor_numero_aditivos.append(numero_aditivos)
        link_licitacao = "http://compras.dados.gov.br" + link_licitacao
        vetor_link_licitacao.append(link_licitacao)
        link_contrato = "http://compras.dados.gov.br" + link_contrato
        vetor_link_contrato.append(link_contrato)
        vetor_data_assinatura.append(data_assinatura)

df1 = pd.DataFrame({'nome_entidade':vetor_nome_entidade, 'cnpj_contratada':vetor_cnpj_contratada, 'valor_inicial':vetor_valor_inicial,
                    'objeto':vetor_objeto,'uasg':vetor_uasg, 'nome_uasg':vetor_nome_uasg, 'tipo_de_licitacao':vetor_tipo_de_licitacao,
                    'numero_licitacao':numero_licitacao, 'numero_contrato':vetor_numero_contrato, 'numero_aditivos':vetor_numero_aditivos,
                    'link_licitacao':vetor_link_licitacao, 'link_contrato':vetor_link_contrato, 'data_assinatura':vetor_data_assinatura})
datatoexcel = pd.ExcelWriter('output.xlsx')
df1.to_excel(datatoexcel)
datatoexcel.save()
print('Planilha pronta!')

        
