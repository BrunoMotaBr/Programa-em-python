import os
import re
from datetime import datetime

def verifica_padrao(string, padrao): #Verifica se o nome do arquivo corresponde ao esperado
    if re.match(padrao, string):     #pelo script
        return True
    else:
        return False

def retira_nome_do_arquivo_sem_perder_o_caminho(filename):#Retira o padrao contendo pedido, cliente, iso_date, date_obj, data
    regex = re.compile(r"\d{4}-\d{2}\.\d{2}\.\d{2}-\d{5}\.txt")
    match = regex.search(filename)
    if match:
        nomeSemOCaminho = match.group()
        filename_without_extension = os.path.splitext(nomeSemOCaminho)[0]
        return filename_without_extension

#def verificar_pedido_existente(lista_pedidos, numero_pedido):      **Implementar
 #   for pedido in lista_pedidos:
  #      if pedido['pedido'] == numero_pedido:
   #         return True
    #return False

def parse_filename(filename):
    #Verifica o arquivo possui mais caracters do que devia
    if(len(filename) > 23):
        nomeSemOCaminho = retira_nome_do_arquivo_sem_perder_o_caminho(filename)+".txt"
    else:
        nomeSemOCaminho = filename
    try:
        filename_without_extension = os.path.splitext(nomeSemOCaminho)[0]
        parts = filename_without_extension.split('-')

        if len(parts) != 3:
            raise ValueError("Invalid filename format (expected pedido-data-cliente)")

        pedido = int(parts[0])
        data = str(parts[1])
        date_obj = datetime.strptime(data, '%d.%m.%y')
        iso_date = date_obj.date().isoformat()
        cliente = int(parts[2])

        return {"pedido": pedido, "data": iso_date, "cliente": cliente}
    except (ValueError, IndexError):
        print("Error parsing filename:", filename)
        return None

def read_lines(filepath):
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
        return lines
    except FileNotFoundError:
        print("File not found:", filepath)
        return []

def produce_json(line):
    
    try:
        stripped_line = line.strip().split('|')
        product_data = {
            "codigo": int(stripped_line[0]),
            "preco": float(stripped_line[3]),
            "quantidade": float(stripped_line[4])
        }
        return product_data
    except ValueError:
        return ValueError