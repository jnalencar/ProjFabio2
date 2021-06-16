indexes = ('nome_entidade', 'cnpj_contratada', 'valor_inicial', 'objeto', 'uasg', 'nome_uasg', 'tipo_de_licitacao', 'numero_licitacao',
           'numero_contrato', 'numero_aditivos', 'link_licitacao', 'link_contrato')

class Contrato:
    def __init__(self, cnpj_contratada, codigo_contrato, cpfContratada, data_assinatura, data_inicio_vigencia, data_termino_vigencia,
                 fundamento_legal, identificador, licitacao_associada, modalidade_licitacao, numero, numero_aditivo, numero_aviso_licitacao, numero_processo,
                 objeto, origem_licitacao, uasg, valor_inicial):
        #18 campos de resposta da API
        self.cnpj_contratada = cnpj_contratada                  #CNPJ da empresa contratada.
        self.codigo_contrato = codigo_contrato                  #Tipo de Contrato.
        self.cpfContratada = cpfCpntratada                      #CPF da contratada.
        self.data_assinatura = data_assinatura                  #Data de assinatura do contrato.
        self.data_inicio_vigencia = data_inicio_vigencia        #Data de início de vigência dos contratos.
        self.data_termino_vigencia = data_termino_vigencia      #Data de término de vigência dos contratos.
        self.fundamento_legal = fundamento_legal                #Fundamento legal do processo de contratação.
        self.identificador = identificador                      #Identificador do Contrato
        self.licitacao_associada = licitacao_associada          #Referência à licitação que originou a contratação.
        self.modalidade_licitacao = modalidade_licitacao        #Número e o ano da licitação que originou a contratação.
        self.numero = numero                                    #Campo seguido pelo número do contrato, seguido do respectivo ano.
        self.numero_aditivo = numero_aditivo                    #Quantidade de termos aditivos de um contrato.
        self.numero_aviso_licitacao = numero_aviso_licitacao    #Número do aviso da licitação que originou a contratação.
        self.numero_processo = numero_processo                  #Número do processo de contratação.
        self.objeto = objeto                                    #Descrição do objeto, a partir de uma descrição de item/serviço informada.
        self.origem_licitacao = origem_licitacao                #Origem da licitação que gerou o contrato: Preço praticado(SISPP) ou Registro de preço(SISRP).
        self.uasg = uasg                                        #Campo de seis digitos que indica o código da UASG contratante.
        self.valor_inicial = valor_inicial                      #Valor inicial do contrato.
        #Mais detalhes sobre esse uso da API em: http://compras.dados.gov.br/docs/contratos/v1/contratos.html

class Licitacao:
    def __init__(self, data_abertura_proposta, data_entrega_edital, data_entrega_proposta, data_publicacao, endereco_entrega_edital, funcao_responsavel,
                 identificador, informacoes_gerais, modalidade, nome_responsavel, numero_aviso, numero_itens, numero_processo, objeto, situacao_aviso,
                 tipo_pregao, tipo_recurso, uasg):
        #18 campos de resposta da API
        self.data_abertura_proposta = data_abertura_proposta    #Data de abertura da proposta.
        self.data_entrega_edital = data_entrega_edital          #Data de Entrega do Edital.
        self.data_entrega_proposta = data_entrega_proposta      #Data de entrega da proposta.
        self.data_publicacao = data_publicacao                  #Data da publicação da licitação.
        self.endereco_entrega_edital = endereco_entrega_edital  #Endereço de Entrega do Edital.
        self.funcao_responsavel = funcao_responsavel            #Função do Responsável pela Licitação.
        self.identificador = identificador                      #Identificador da Licitação.
        self.informacoes_gerais = informacoes_gerais            #Informações Gerais.
        self.modalidade = modalidade                            #Código da Modalidade da Licitação.
        self.nome_responsavel = nome_responsavel                #Nome do Responsável pela Licitação.
        self.numero_aviso = numero_aviso                        #Número do Aviso da Licitação.
        self.numero_itens = numero_itens                        #Número de Itens.
        self.numero_processo = numero_processo                  #Número do Processo.
        self.objeto = objeto                                    #Objeto da Licitação.
        self.situacao_aviso = situacao_aviso                    #Situação do aviso.
        self.tipo_pregao = tipo_pregao                          #Tipo do Pregão.
        self.tipo_recurso = tipo_recurso                        #Tipo do Recurso.
        self.uasg = uasg                                        #Código da UASG.
        #Mais detalhes sobre esse uso da API em: http://compras.dados.gov.br/docs/licitacoes/v1/licitacoes.html

class final_fabio:
            
    def __init__(self, nome_entidade, cnpj_contratada, objeto, uasg, nome_uasg, tipo_de_licitacao, numero_licitacao,
                 numero_contrato, numero_aditivos, link_licitacao, link_contrato, valor_inicial = 0):
        self.nome_entidade = nome_entidade
        self.cnpj_contratada = cnpj_contratada
        self.valor_inicial = valor_inicial
        self.objeto = objeto
        self.uasg = uasg
        self.nome_uasg = nome_uasg
        self.tipo_de_licitacao = check_modalidade(tipo_de_licitacao)
        self.numero_licitacao = numero_licitacao
        self.numero_contrato = numero_contrato
        self.numero_aditivos = numero_aditivos
        self.link_licitacao = "http://compras.dados.gov.br" + link_licitacao
        self.link_contrato = "http://compras.dados.gov.br" + link_contrato

#while(i):
#    try:
#        print('Trying request\n')
#        page = requests.get(url, verify = False).text
#    except requests.ConnectionError:
#        print ("Error")
#        if (i==10):
#            break;
#    else:
#        print("Sucefull")
#        dicion = json.loads(page)
#        print(json.dumps(dicion, indent = 3))
#        #print(dicion)
#        i=0

for cnpj in lista_cnpjs_beneficiadas:
    with open(cnpj + ".txt","r", encoding = 'utf8') as file:
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
        #contrato.append(nome_entidade)
        #contrato.append(cnpj_contratada)
        #contrato.append(valor_inicial)
        if valor_inicial == None:
            valor_inicial = 'Nao Informado'
        #contrato.append(objeto)
        #contrato.append(uasg)
        #contrato.append(nome_uasg)
        #contrato.append(tipo_de_licitacao)
        #contrato.append(numero_licitacao)
        #contrato.append(numero_contrato)
        #contrato.append(numero_aditivos)
        link_licitacao = "http://compras.dados.gov.br" + link_licitacao
        #contrato.append(link_licitacao)
        link_contrato = "http://compras.dados.gov.br" + link_contrato
        #contrato.append(link_contrato)
        #vetor_de_vetores.append(contrato)
        
        #novo = final_fabio(nome_entidade, cnpj_contratada, objeto, uasg, nome_uasg, tipo_de_licitacao, numero_licitacao,
        #         numero_contrato, numero_aditivos, link_licitacao, link_contrato, valor_inicial)
        #vetor_classes.append(novo)

#df1 = pd.DataFrame(vetor_de_vetores, columns = indexes)
