![uol-logo](http://i.imgur.com/5cZufN6.jpg)

# UOL Mais Downloader
### Um downloader em massa escrito em Python para vídeos do UOL Mais

## COMO USAR

Atualmente, o UOL Mais Downloader suporta apenas sistemas nos quais o Python 2.7+ esteja disponível para instalação.
Para executar o script, por favor, instale as dependências utilizando:

`pip install beautifulsoup4` ou `easy_install beautifulsoup4`

Após a instalação das dependências, execute simplesmente:

`./downloader.py arquivo.txt local/para/download`

Onde `arquivo.txt` deve ser um arquivo de texto simples contendo uma lista com os links dos vídeos no UOL Mais separados por enter, ou seja, um link por linha.
`local/para/download` deve ser um diretório existente em seu sistema de arquivos.

Para efetuar o download direto deste repositório utilize [este link](https://github.com/alexandreteles/uolmaisdownloader/archive/master.zip).

## TO-DO

1. Aplicação *self-contained*;
2. Instalador para plataformas Windows;
3. Interface gráfica;
4. Servidor web embutido;
5. Wrapper PHP;
7. Melhorar este README

## CHANGELOG

v0.1alpha - Versão Inicial

## SUPORTE

EXCLUSIVAMENTE através das "Issues" aqui no GitHub.
