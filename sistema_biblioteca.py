import datetime

ARQUIVO_LIVROS = "livros.txt"
ARQUIVO_HISTORICO = "historico.txt"
ARQUIVO_USUARIOS = "usuarios.txt"


def obter_input_nao_vazio(mensagem):
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("Entrada inválida. Tente novamente.")

def carregar_arquivo(arquivo_nome):
    try:
        with open(arquivo_nome, "r", encoding="utf-8") as f:
            return f.readlines()
    except FileNotFoundError:
        return []

def salvar_linha(arquivo_nome, linha):
    with open(arquivo_nome, "a", encoding="utf-8") as f:
        f.write(linha + "\n")