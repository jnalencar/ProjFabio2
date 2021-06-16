import os
import requests

url = 'http://compras.dados.gov.br/contratos/v1/contratos.json?cnpj_contratada='

arquivo = open('CNPJDF.txt', 'r')
cnpj_beneficiadas = arquivo.readlines()
arquivo.close()
cnpj_beneficiadas = [cnpj.replace('\n', '') for cnpj in cnpj_beneficiadas]

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



# A List of Items
items = list(range(0, 57))
l = len(cnpj_beneficiadas)
j = 1

# Initial call to print 0% progress
printProgressBar(0, l, prefix = 'Criando arquivos TXT... Progresso:', suffix = 'Completo ' + str(j)+ '/' + str(len(cnpj_beneficiadas)), length = 50)
for j, cnpj in enumerate(cnpj_beneficiadas):
    nomearq = cnpj + '.txt'
    urlcnpj = url + cnpj
    i = 0
    printProgressBar(j + 1, l, prefix = 'Criando arquivos TXT... Progresso:', suffix = 'Completo ' + str(j)+ '/' + str(len(cnpj_beneficiadas)), length = 50)
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
    
    
