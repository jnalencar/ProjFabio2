import requests

url = 'http://compras.dados.gov.br/contratos/v1/contratos.json?cnpj_contratada='

arquivo = open('CNPJDF.txt', 'r')
cnpj_beneficiadas = arquivo.readlines()
arquivo.close()
cnpj_beneficiadas = [cnpj.replace('\n', '') for cnpj in cnpj_beneficiadas]

for cnpj in cnpj_beneficiadas:
    nomearq = cnpj + '.txt'
    urlcnpj = url + cnpj
    i = 0
    while(i<5):
        try:
            print('Tentativa de extracao de dados do cnpj =',cnpj,'iniciada.')
            page = requests.get(urlcnpj, verify = False).text
        except requests.ConnectionError:
            print ("Erro na extracao de dados do cnpj =",cnpj)
            i = i+1
            print ("Tentativa",i,"de 5.")
        else:
            print('Extracao de dados bem sucedida.\nCriando arquivo txt...')
            i = 5
    with open(nomearq, 'w') as arq:
        arq.write(page)
        print('Arquivo criado com sucesso.')


    
