import pdfplumber
from os import listdir
import re
import csv

# Lista todos os arquivos no diretório './dados'
raw = listdir('./dados')

# Abre um arquivo CSV para escrita
with open('dados.csv', 'w') as csvfile:

    # Itera sobre cada arquivo listado
    for r in raw:
        print("'"+r+"'")

        # Abre o arquivo PDF usando pdfplumber
        with pdfplumber.open('./Chamados SOC/'+r) as pdf:
            pages = pdf.pages
            text = ""

            # Extrai o texto de cada página do PDF
            for page in pages:
                text += page.extract_text()
        data = text
        linhas = data.splitlines()

        # Extrai informações específicas do texto usando expressões regulares
        id = next((linha for linha in linhas if linha.startswith('Ticket#')), None)
        titulo = next((linha for linha in linhas if re.match(r'Qradar|QRADAR|QRadar', linha)), None)
        prioridade = ''.join(re.findall(r'Prioridade\s(.*?)Idade', data))
        estado = ''.join(re.findall(r'Estado\s(.*?)ID', data))
        criado = ''.join(re.findall(r'Criado\s(\d{2}/\d{2}/\d{4})', data))
        hora = ''.join(re.findall(r'Criado .*\s(\d{2}:\d{2}:\d{2})', data))

        # Agrupa os dados extraídos em uma tupla
        data_result = (id, titulo, prioridade, estado, criado, hora)
        
        # Escreve os dados extraídos no arquivo CSV
        csv.writer(csvfile, delimiter=',').writerow([
            data_result[0],
            data_result[1],
            data_result[2],
            data_result[3],
            data_result[4],
            data_result[5]
        ])
