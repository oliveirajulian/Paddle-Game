import os, time
import json
from datetime import datetime


def limpar_tela():
    os.system("cls")
    
def aguarde(segundos):
    time.sleep(segundos)
    
def inicializarBancoDeDados():
    # r - read, w - write, a - append
    try:
        banco = open("log.data","r")
    except:
        print("Banco de Dados Inexistente. Criando...")
        banco = open("log.data","w")
    
from datetime import datetime
import json

import json
from datetime import datetime

def escreverDados(nomeDoJogador, pontos):
    try:
        with open("log.data", "r") as banco:
            dados = json.load(banco)
    except:
        dados = {}

    registro = {
        "nome": nomeDoJogador,
        "pontos": pontos,
        "data": datetime.now().strftime("%d/%m/%Y"),
        "hora": datetime.now().strftime("%H:%M:%S")
    }

    if "todos" not in dados:
        dados["todos"] = []
    dados["todos"].append(registro)

    # Também salvar histórico individual do jogador
    if nomeDoJogador not in dados:
        dados[nomeDoJogador] = []
    dados[nomeDoJogador].append(registro)

    with open("log.data", "w") as banco:
        json.dump(dados, banco, indent=4)




    
