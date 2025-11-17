# Como criar o executável

## Pré-requisitos

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Método 1: Usando o script de build (Recomendado)

Execute o script de build:
```bash
python build_exe.py
```

O executável será criado em `dist/MontadorImagens.exe`

## Método 2: Usando PyInstaller diretamente

Execute o comando:
```bash
pyinstaller --name=MontadorImagens --onefile --windowed montador_imagens.py
```

## Método 3: Usando o arquivo .spec

Execute:
```bash
pyinstaller MontadorImagens.spec
```

## Opções de personalização

### Adicionar um ícone

1. Crie ou obtenha um arquivo `.ico`
2. Coloque-o na pasta do projeto
3. No arquivo `.spec`, altere:
   ```python
   icon='seu_icone.ico',
   ```
4. Ou use a opção `--icon=seu_icone.ico` no comando PyInstaller

### Incluir arquivos adicionais

Se precisar incluir outros arquivos no executável, adicione em `datas` no arquivo `.spec`:
```python
datas=[('arquivo.txt', '.'), ('pasta', 'pasta')],
```

## Resultado

Após a compilação, você encontrará:
- `dist/MontadorImagens.exe` - O executável final
- `build/` - Arquivos temporários de build (pode ser deletado)
- `MontadorImagens.spec` - Arquivo de configuração (pode ser reutilizado)

## Distribuição

Você pode distribuir apenas o arquivo `MontadorImagens.exe`. Ele contém tudo necessário para executar o programa.

