# Documentação do Script de Busca de Atalhos

Este script é responsável por buscar atalhos no formato `.lnk` em pastas específicas, verificar se as palavras-chave estão presentes nos nomes dos arquivos, e salvar os resultados encontrados em um arquivo de saída. A busca é otimizada utilizando múltiplas threads.

## Funcionalidades

1. **Busca de atalhos nas pastas especificadas**: O script busca arquivos `.lnk` nas pastas e subpastas especificadas na lista `PASTAS_PARA_BUSCA`.
2. **Filtragem de atalhos com palavras-chave**: A busca filtra os atalhos para verificar se o nome do arquivo contém alguma das palavras-chave especificadas na lista `PALAVRAS_CHAVE`.
3. **Execução otimizada com múltiplas threads**: A busca é feita de maneira otimizada utilizando o módulo `concurrent.futures` para realizar buscas simultâneas em diferentes pastas.
4. **Registro de resultados**: Os atalhos encontrados são salvos em um arquivo de log, localizado em `C:\\Windows\\Temp\\resultado_atalhos.txt`.

## Estrutura do Código

### 1. Importação de Bibliotecas

```python
import os
import concurrent.futures
```

Essas bibliotecas são usadas para manipulação de arquivos e diretórios, além de realizar a busca de forma otimizada:
- **`os`**: Para manipulação de caminhos de arquivos e diretórios.
- **`concurrent.futures`**: Para otimizar a busca utilizando múltiplas threads.

### 2. Variáveis de Configuração

#### Lista de palavras-chave para busca

```python
PALAVRAS_CHAVE = {p.lower() for p in [
    "LGPD", "Ronda Senior", "SRVTCP", "Administração de Pessoal",
    "Benefícios e Tarefeiros", "Cargos e Salários", "Controle de Ponto e Refeitório",
    "Jurídico", "Quadro de Vagas e Orçamento", "Recrutamento e Seleção",
    "Segurança e Medicina", "Treinamento e Pesquisa"
]}
```

A lista `PALAVRAS_CHAVE` contém as palavras-chave (em minúsculas) que serão usadas para filtrar os atalhos durante a busca. A busca será feita nos nomes dos arquivos, verificando se algum termo da lista aparece no nome do atalho.

#### Caminho do usuário e saída

```python
USUARIO_ATUAL = os.getenv("USERPROFILE", "C:\\Users\\Default")
OUTPUT_FILE = r"C:\\Windows\\Temp\\resultado_atalhos.txt"
```

- **`USUARIO_ATUAL`**: Obtém o caminho do perfil do usuário atual no sistema (padrão: `C:\\Users\\Default`).
- **`OUTPUT_FILE`**: Caminho do arquivo de saída onde os atalhos encontrados serão registrados.

#### Pastas de busca

```python
PASTAS_PARA_BUSCA = [
    USUARIO_ATUAL, "C:\\ProgramData\\Microsoft\\Windows\\Start Menu",
    "D:\\Users", "E:\\Users"
]
```

A lista `PASTAS_PARA_BUSCA` contém as pastas onde o script irá procurar pelos atalhos. Ela inclui o diretório do usuário atual e outros diretórios de usuários e menu de inicialização do Windows.

### 3. Funções

#### `buscar_atalhos_em_pasta(pasta)`

```python
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
```

Esta função percorre uma pasta e suas subpastas, procurando por arquivos com extensão `.lnk`. Para cada atalho encontrado, o script verifica se o nome do arquivo contém alguma das palavras-chave na lista `PALAVRAS_CHAVE`. Se sim, o atalho é adicionado à lista de resultados.

#### `salvar_resultado(atalhos)`

```python
def salvar_resultado(atalhos):
    """Salva os atalhos encontrados no arquivo, se houver."""
    if atalhos:
        try:
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                f.write("; ".join(atalhos) + ";")
        except Exception:
            pass  # Ignora erros ao salvar
```

Esta função recebe a lista de atalhos encontrados e os grava no arquivo de saída `resultado_atalhos.txt`. Os atalhos são salvos como uma string, separados por ponto e vírgula.

#### `processar_busca()`

```python
def processar_busca():
    """Executa a busca de forma otimizada usando threads."""
    atalhos_encontrados = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        resultados = executor.map(buscar_atalhos_em_pasta, PASTAS_PARA_BUSCA)
        for resultado in resultados:
            atalhos_encontrados.extend(resultado)
    salvar_resultado(atalhos_encontrados)
```

Esta função realiza a busca de atalhos nas pastas definidas em `PASTAS_PARA_BUSCA`. Ela utiliza um pool de threads, permitindo que várias pastas sejam processadas simultaneamente, o que melhora o desempenho. Após obter os resultados, ela chama a função `salvar_resultado()` para gravar os atalhos encontrados no arquivo de saída.

### 4. Execução do Script

```python
if __name__ == "__main__":
    processar_busca()
```

Esta linha garante que o script será executado apenas quando for chamado diretamente (não quando importado como módulo). Ela chama a função `processar_busca()` para iniciar a busca e salvar os resultados.

## Uso

1. **Executar o script**: Para rodar o script, basta executá-lo em um ambiente Python. Ele irá buscar os atalhos nas pastas especificadas e gravar os resultados no arquivo de saída.
2. **Verificar o arquivo de resultado**: Após a execução, o arquivo de saída `resultado_atalhos.txt`, localizado em `C:\\Windows\\Temp\\`, pode ser verificado para visualizar os atalhos encontrados.

## Possíveis Melhorias

- **Aprimoramento na gestão de erros**: O script poderia registrar detalhes dos erros (ex.: erros de acesso a pastas) em um arquivo de log para facilitar o diagnóstico de problemas.
- **Filtros adicionais**: A busca poderia ser aprimorada com filtros adicionais, como data de criação ou modificação dos atalhos.

## Conclusão

Este script proporciona uma forma eficiente e otimizada de buscar atalhos no sistema, filtrando-os de acordo com palavras-chave específicas. A utilização de múltiplas threads ajuda a melhorar o desempenho da busca em várias pastas simultaneamente.
