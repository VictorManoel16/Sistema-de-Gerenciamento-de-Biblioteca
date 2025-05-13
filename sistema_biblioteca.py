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

       def cadastrar_usuario():
    print("\n--- Cadastro de Usuário ---")
    nome = obter_input_nao_vazio("Nome: ")
    cpf = obter_input_nao_vazio("CPF: ")
    usuarios = carregar_arquivo(ARQUIVO_USUARIOS)
    for usuario in usuarios:
        if cpf in usuario:
            print("Usuário já cadastrado.")
            return
    salvar_linha(ARQUIVO_USUARIOS, f"{nome}|{cpf}")
    print(" Usuário cadastrado com sucesso!")

def obter_usuario_por_cpf(cpf):
    usuarios = carregar_arquivo(ARQUIVO_USUARIOS)
    for usuario in usuarios:
        nome_u, cpf_u = usuario.strip().split("|")
        if cpf_u == cpf:
            return nome_u
    return None
 