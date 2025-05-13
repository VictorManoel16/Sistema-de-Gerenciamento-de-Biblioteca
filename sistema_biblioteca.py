ARQUIVO_LIVROS = "livros.txt"

def carregar_livros():
    livros = []
    try:
        with open(ARQUIVO_LIVROS, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                partes = linha.strip().split("|")
                if len(partes) == 3:
                    titulo, autor, status = partes
                    livros.append({"titulo": titulo, "autor": autor, "status": status})