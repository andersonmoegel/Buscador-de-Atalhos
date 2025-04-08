# Shortcut Search Script Documentation

This script searches for `.lnk` shortcut files in specific folders, checks if keywords are present in the filenames, and saves the results in an output file. The search is optimized using multiple threads.

## Features

1. **Search for shortcuts in specified folders**: The script searches for `.lnk` files in the folders and subfolders listed in `PASTAS_PARA_BUSCA`.
2. **Filtering shortcuts with keywords**: The script filters shortcuts by checking if the filename contains any of the specified keywords in `PALAVRAS_CHAVE`.
3. **Optimized execution with multithreading**: Uses the `concurrent.futures` module for concurrent searching in different folders.
4. **Logging results**: Found shortcuts are saved in a log file at `C:\Windows\Temp\resultado_atalhos.txt`.

## Code Structure

### 1. Importing Libraries

```python
import os
import concurrent.futures
```

Used for file and directory handling and optimized searching:
- **`os`**: For manipulating file and directory paths.
- **`concurrent.futures`**: To optimize the search using multiple threads.

### 2. Configuration Variables

#### List of keywords for filtering

```python
PALAVRAS_CHAVE = {p.lower() for p in [
    "LGPD", "Ronda Senior", "SRVTCP", "Administração de Pessoal",
    "Benefícios e Tarefeiros", "Cargos e Salários", "Controle de Ponto e Refeitório",
    "Jurídico", "Quadro de Vagas e Orçamento", "Recrutamento e Seleção",
    "Segurança e Medicina", "Treinamento e Pesquisa"
]}
```

This set contains lowercase keywords used to filter shortcuts by filename.

#### User path and output

```python
USUARIO_ATUAL = os.getenv("USERPROFILE", "C:\Users\Default")
OUTPUT_FILE = r"C:\Windows\Temp\resultado_atalhos.txt"
```

- **`USUARIO_ATUAL`**: Gets the current user's profile path (default: `C:\Users\Default`).
- **`OUTPUT_FILE`**: Path to the output file where results are saved.

#### Search folders

```python
PASTAS_PARA_BUSCA = [
    USUARIO_ATUAL, "C:\ProgramData\Microsoft\Windows\Start Menu",
    "D:\Users", "E:\Users"
]
```

These folders will be searched recursively for `.lnk` files.

### 3. Functions

#### `buscar_atalhos_em_pasta(pasta)`

```python
def buscar_atalhos_em_pasta(pasta):
    """Searches for `.lnk` shortcuts in a folder and its subfolders."""
    encontrados = []
    try:
        for root, _, files in os.walk(pasta, followlinks=True):
            encontrados.extend(
                os.path.join(root, f) for f in files if f.endswith(".lnk") and any(p in f.lower() for p in PALAVRAS_CHAVE)
            )
    except Exception:
        pass
    return encontrados
```

Searches for `.lnk` files in a directory and checks if filenames match any keyword.

#### `salvar_resultado(atalhos)`

```python
def salvar_resultado(atalhos):
    """Saves found shortcuts to the output file."""
    if atalhos:
        try:
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                f.write("; ".join(atalhos) + ";")
        except Exception:
            pass
```

Saves the list of found shortcuts to the output file.

#### `processar_busca()`

```python
def processar_busca():
    """Runs the search using multithreading."""
    atalhos_encontrados = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        resultados = executor.map(buscar_atalhos_em_pasta, PASTAS_PARA_BUSCA)
        for resultado in resultados:
            atalhos_encontrados.extend(resultado)
    salvar_resultado(atalhos_encontrados)
```

Searches all configured folders concurrently and saves the results.

### 4. Script Execution

```python
if __name__ == "__main__":
    processar_busca()
```

Ensures the script only runs when executed directly.

## Usage

1. **Run the script**: Execute in a Python environment. It will search and log results to the output file.
2. **Check the output**: The file `resultado_atalhos.txt` in `C:\Windows\Temp\` will contain the results.

## Possible Improvements

- **Better error logging**: The script could log errors (e.g., permission issues) for debugging.
- **Additional filters**: Filter by creation or modification date could be added.

## Conclusion

This script efficiently searches for shortcut files in the system and filters them using specific keywords. Multithreading improves performance when searching multiple folders.
