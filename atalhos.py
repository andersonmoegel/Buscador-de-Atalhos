import os
import concurrent.futures

# Lista de palavras-chave (minúsculas para busca otimizada)
PALAVRAS_CHAVE = {p.lower() for p in [
    "LGPD", "Ronda Senior", "SRVTCP", "Administração de Pessoal",
    "Benefícios e Tarefeiros", "Cargos e Salários", "Controle de Ponto e Refeitório",
    "Jurídico", "Quadro de Vagas e Orçamento", "Recrutamento e Seleção",
    "Segurança e Medicina", "Treinamento e Pesquisa"
]}

# Caminho do usuário e saída
USUARIO_ATUAL = os.getenv("USERPROFILE", "C:\\Users\\Default")
OUTPUT_FILE = r"C:\\Windows\\Temp\\resultado_atalhos.txt"

# Pastas de busca
PASTAS_PARA_BUSCA = [
    USUARIO_ATUAL, "C:\\ProgramData\\Microsoft\\Windows\\Start Menu",
    "D:\\Users", "E:\\Users"
]

def buscar_atalhos_em_pasta(pasta):
    """Busca atalhos (.lnk) em uma pasta e subpastas."""
    encontrados = []
    try:
        for root, _, files in os.walk(pasta, followlinks=True):
            encontrados.extend(
                os.path.join(root, f) for f in files if f.endswith(".lnk") and any(p in f.lower() for p in PALAVRAS_CHAVE)
            )
    except Exception:
        pass  # Ignora erros de acesso
    return encontrados

def salvar_resultado(atalhos):
    """Salva os atalhos encontrados no arquivo, se houver."""
    if atalhos:
        try:
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                f.write("; ".join(atalhos) + ";")
        except Exception:
            pass  # Ignora erros ao salvar

def processar_busca():
    """Executa a busca de forma otimizada usando threads."""
    atalhos_encontrados = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        resultados = executor.map(buscar_atalhos_em_pasta, PASTAS_PARA_BUSCA)
        for resultado in resultados:
            atalhos_encontrados.extend(resultado)
    salvar_resultado(atalhos_encontrados)

if __name__ == "__main__":
    processar_busca()
