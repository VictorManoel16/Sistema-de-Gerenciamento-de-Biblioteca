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

# ================= LIVROS =================

def carregar_livros():
    livros = []
    linhas = carregar_arquivo(ARQUIVO_LIVROS)
    for linha in linhas:
        partes = linha.strip().split("|")
        if len(partes) == 4:
            titulo, autor, status, data_devolucao = partes
            livros.append({"titulo": titulo, "autor": autor, "status": status, "data_devolucao": data_devolucao})
    return livros

def salvar_livros(livros):
    with open(ARQUIVO_LIVROS, "w", encoding="utf-8") as f:
        for livro in livros:
            linha = f"{livro['titulo']}|{livro['autor']}|{livro['status']}|{livro['data_devolucao']}"
            f.write(linha + "\n")

def encontrar_livro_por_titulo(livros, titulo_busca):
    for livro in livros:
        if livro['titulo'].lower() == titulo_busca:
            return livro
    return None

# ================= OPERAÇÕES =================

def cadastrar_livro(livros):
    titulo = obter_input_nao_vazio("Título do livro: ")
    autor = obter_input_nao_vazio("Autor do livro: ")
    for l in livros:
        if l['titulo'].lower() == titulo.lower():
            print("Livro já cadastrado.")
            return
    livros.append({"titulo": titulo, "autor": autor, "status": "disponível", "data_devolucao": "-"})
    print("✅ Livro cadastrado com sucesso!")

def listar_livros(livros):
    if not livros:
        print("Nenhum livro cadastrado.")
        return
    print("\nLista de livros:")
    for i, livro in enumerate(livros, 1):
        print(f"{i}. {livro['titulo']} - {livro['autor']} ({livro['status']})", end="")
        if livro['status'] == "emprestado":
            print(f" | Devolução até: {livro['data_devolucao']}")
        else:
            print()

def buscar_livro(livros):
    termo = obter_input_nao_vazio("Digite parte do título: ").lower()
    encontrados = [l for l in livros if termo in l['titulo'].lower()]
    if encontrados:
        for livro in encontrados:
            print(f"- {livro['titulo']} - {livro['autor']} ({livro['status']})")
    else:
        print("🔍 Nenhum livro encontrado.")

def registrar_historico(acao, titulo, usuario):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linha = f"[{timestamp}] - {acao} - {titulo} - {usuario}"
    salvar_linha(ARQUIVO_HISTORICO, linha)

def emprestar_livro(livros):
    cpf = obter_input_nao_vazio("CPF do usuário: ")
    usuario = obter_usuario_por_cpf(cpf)
    if not usuario:
        print("Usuário não encontrado.")
        return

    titulo = obter_input_nao_vazio("Título do livro a emprestar: ").lower()
    livro = encontrar_livro_por_titulo(livros, titulo)

    if not livro:
        print("Livro não encontrado.")
    elif livro['status'] == "emprestado":
        print("Livro já está emprestado.")
    else:
        dias_emprestimo = 7
        data_devolucao = datetime.date.today() + datetime.timedelta(days=dias_emprestimo)
        livro['status'] = "emprestado"
        livro['data_devolucao'] = data_devolucao.strftime("%Y-%m-%d")
        registrar_historico("EMPRESTADO", livro['titulo'], usuario)
        print(f" Livro emprestado. Devolução até {livro['data_devolucao']}.")

def devolver_livro(livros):
    cpf = obter_input_nao_vazio("CPF do usuário: ")
    usuario = obter_usuario_por_cpf(cpf)
    if not usuario:
        print("Usuário não encontrado.")
        return

    titulo = obter_input_nao_vazio("Título do livro a devolver: ").lower()
    livro = encontrar_livro_por_titulo(livros, titulo)

    if not livro:
        print("Livro não encontrado.")
    elif livro['status'] == "disponível":
        print("Este livro já está disponível.")
    else:
        livro['status'] = "disponível"
        livro['data_devolucao'] = "-"
        registrar_historico("DEVOLVIDO", livro['titulo'], usuario)
        print("✅ Livro devolvido com sucesso.")

def mostrar_historico():
    print("\n--- Histórico ---")
    linhas = carregar_arquivo(ARQUIVO_HISTORICO)
    if linhas:
        for linha in linhas:
            print(linha.strip())
    else:
        print("Nenhum registro no histórico.")

def verificar_atrasos(livros):
    hoje = datetime.date.today()
    atrasados = [l for l in livros if l['status'] == "emprestado" and l['data_devolucao'] != "-" and datetime.date.fromisoformat(l['data_devolucao']) < hoje]
    if atrasados:
        print("\n📌 Livros em atraso:")
        for l in atrasados:
            print(f"- {l['titulo']} - Devolução era até {l['data_devolucao']}")
    else:
        print("\n✅ Nenhum livro atrasado no momento.")

# ================= MENU =================

def exibir_menu():
    print("\n--- Sistema de Biblioteca ---")
    print("1. Cadastrar livro")
    print("2. Listar livros")
    print("3. Buscar livro por título")
    print("4. Emprestar livro")
    print("5. Devolver livro")
    print("6. Ver histórico")
    print("7. Ver livros atrasados")
    print("8. Cadastrar usuário")
    print("9. Sair")

def main():
    livros = carregar_livros()
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        match opcao:
            case "1":
                cadastrar_livro(livros)
            case "2":
                listar_livros(livros)
            case "3":
                buscar_livro(livros)
            case "4":
                emprestar_livro(livros)
            case "5":
                devolver_livro(livros)
            case "6":
                mostrar_historico()
            case "7":
                verificar_atrasos(livros)
            case "8":
                cadastrar_usuario()
            case "9":
                salvar_livros(livros)
                print("📁 Dados salvos. Encerrando o sistema.")
                break
            case _:
                print(" Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()