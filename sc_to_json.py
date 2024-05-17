import json
import os
import sc_to_json_functions as scf

def executar_script(argumentos):
    if len(argumentos) >= 1:
        #Carrega arquivo json e retorna um array
        with open("Json\\pedidos.json", 'r') as file:
                jsonAtual = json.load(file)
        contador = 0
        for filepath in argumentos:
            if not os.path.isfile(filepath):
                print(f"Error: File not found. {filepath} does not exist.")
                continue

            lines = scf.read_lines(filepath)
            filename_data = scf.parse_filename(filepath)
            if filename_data is None:
                continue

            products = []
            try:
                for line in lines:
                    product_data = scf.produce_json(line)
                    products.append(product_data)

                final_json = {
                    "pedido": filename_data["pedido"],
                    "data": filename_data["data"],
                    "cliente": filename_data["cliente"],
                    "produtos": products
                }
                jsonAtual.append(final_json) #Adiciona o novo objeto json a lista já existente.
            except ValueError:
                return ValueError
            
            with open(f"Json\\pedidos.json", 'w') as outfile:
                #Acessa arquivo json e reescreve com as informações atualizadas.
                jsonAtual.reverse() # <= Realiza a reordenação do arquivo json para que o mais recente fique acima.
                json.dump(jsonAtual, outfile, indent=4)

        return [True, f"JSON(s) written to pedidos.json in directory Json."]
    else:
        return [False, "Error: Expected at least 1 argument. 0 given.\nFinishing process."]
