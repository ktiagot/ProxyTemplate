# Montador de Imagens para PDF A4

Programa em Python para automatizar a montagem de imagens em PDFs A4 com layout 3x3, incluindo margens de sangria para guia de corte. Ideal para criar proxies de cartas ou qualquer material que precise ser impresso e cortado em tamanhos específicos.

## 📋 Funcionalidades

- **Layout 3x3**: Organiza 9 imagens em uma página A4
- **Processamento em lote**: Processa quantas imagens quiser, criando múltiplos PDFs automaticamente
- **Dois modos de processamento**:
  - **Com sangria**: Imagens já incluem a margem extra (6,85 x 9,35 cm - padrão das imagens que você encontra no mpcfill.com e outras proxies online)
  - **Sem sangria**: Imagens estão no tamanho final (6,35 x 8,89 cm) - o programa adiciona a sangria automaticamente
- **Redimensionamento automático**: Ajusta imagens para as dimensões corretas
- **Linhas de guia**: Marca as bordas de corte com linhas vermelhas
- **Interface gráfica**: Seleção fácil de arquivos e pasta de saída via diálogos do Windows
- **Executável standalone**: Pode ser compilado em um único arquivo .exe

## 🚀 Instalação

### Usar o executável (Windows)

1. Baixe o arquivo `MontadorImagens.exe` [aqui](https://github.com/ktiagot/ProxyTemplate/blob/master/dist/MontadorImagens.exe) e clique no terceiro botão <img width="100" height="46" alt="image" src="https://github.com/user-attachments/assets/e89e52cd-40e1-432d-b33b-05e4c6ae318a" />

2. Execute o arquivo diretamente (não precisa do Python instalado)

   
## 📖 Como usar

1. **Execute o programa** (script Python ou executável)

2. **Selecione o modo de processamento**:
   - **Sim**: Se suas imagens já incluem sangria (tamanho 6,85 x 9,35 cm)
   - **Não**: Se suas imagens estão no tamanho final (6,35 x 8,89 cm)

3. **Selecione as imagens**:
   - Escolha quantas imagens quiser (JPG, PNG, BMP, TIFF)
   - O programa criará PDFs automaticamente a cada 9 imagens

4. **Escolha a pasta de saída**:
   - Selecione onde deseja salvar os PDFs gerados

5. **Resultado**:
   - PDFs serão criados com o padrão: `proxies_pagina_01.pdf`, `proxies_pagina_02.pdf`, etc.
   - Cada PDF contém até 9 imagens organizadas em layout 3x3
   - Linhas vermelhas indicam onde cortar

