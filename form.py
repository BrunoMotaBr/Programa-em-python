import tkinter as tk
from tkinter import filedialog,messagebox
import sc_to_json as principal
import re
import os

def selecionar_arquivos(nome_dos_arquivos = ""):#Botão para selecionar o arquivo manualmente
    if nome_dos_arquivos == "":
        nome_dos_arquivos = filedialog.askopenfilenames()   
    if nome_dos_arquivos:
        btn_processar.config(state=tk.NORMAL)
        arquivos_selecionados.extend(nome_dos_arquivos)
        text_box.config(state=tk.NORMAL)
        for nome_do_arquivo in nome_dos_arquivos:
            text_box.insert(tk.END, f"{nome_do_arquivo}\n")
        text_box.config(state=tk.DISABLED)

def delete_text(): 
    text_box.config(state=tk.NORMAL)
    text_box.delete("1.0", "end") 
    text_box.config(state=tk.DISABLED)
    btn_processar.config(state=tk.DISABLED)
    arquivos_selecionados.clear()

def on_processar_arquivos():#Retira somente o padrão da string antes de iniciar o processamento
    try:
        resultado = principal.executar_script(arquivos_selecionados)
        if resultado[0]:
            messagebox.showinfo("Sucesso", f"Arquivos processados com sucesso!\n{resultado[1]}")        
        else:
            messagebox.showerror("Erro", "Nenhum arquivo foi selecionado.")
    except TypeError as msg:
        messagebox.showerror("Erro", f"Um dos Arquivos selecionado esta vazio ou fora do padrão esperado!\n{arquivos_selecionados} {msg}")
        delete_text()
    except UnicodeDecodeError:
        messagebox.showerror("Erro", f"Arquivo com extensão fora do esperado selecione arquivos .txt.\n{arquivos_selecionados}")

def busca_arquivos_com_padrao():#Verifica dentro do diretorio se existem arquivos que correspondem ao padrão de nomenclatura esperado caso exista retorna uma lista com todos esses
    pasta_origem = "C:\\Users\\MKT-ASUS_I5\\Desktop\\Programa em python" #Pasta de origem para a busca
    padrao = r"\d{4}-\d{2}\.\d{2}\.\d{2}-\d{5}\.txt"
    arquivos_com_padrao = []
    arquivos_encontrados = os.listdir(pasta_origem)
    for nome_arquivo in arquivos_encontrados:
        if re.match(padrao, nome_arquivo):
            arquivos_com_padrao.append(nome_arquivo)
    if(len(arquivos_com_padrao) > 0):
        messagebox.showinfo("Sucesso", f"Arquivos encontrados {len(arquivos_com_padrao)}")
    else:
        messagebox.showerror("Erro", "Nenhum arquivo foi encontrado.")
    selecionar_arquivos(arquivos_com_padrao)


root = tk.Tk()
root.geometry("400x400")
root.title("Selecionar e Processar Arquivos")

bnt_bucar_auto_arquivos = tk.Button(root, text="Procurar Arquivos", command=busca_arquivos_com_padrao)
bnt_bucar_auto_arquivos.pack(pady=10)
bnt_bucar_auto_arquivos.focus()
root.bind("<Return>", busca_arquivos_com_padrao)


btn_selecionar_arquivos = tk.Button(root, text="Selecionar Arquivos", command=selecionar_arquivos)
btn_selecionar_arquivos.pack(pady=10)

btn_processar = tk.Button(root, text="Processar Arquivos", command=on_processar_arquivos, state=tk.DISABLED)
btn_processar.pack(pady=10)

text_box = tk.Text(root, width=50, height=5, state=tk.DISABLED)
text_box.pack()


tk.Button(root, text="Apagar seleção de arquivos", command=delete_text).pack()


arquivos_selecionados = []

root.mainloop()
