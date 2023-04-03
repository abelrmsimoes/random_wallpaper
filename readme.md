# Random Wallpaper

Este é um programa que permite definir uma imagem aleatória como papel de parede em um intervalo de tempo configurável. Ele usa a API do Unsplash para obter imagens aleatórias de alta qualidade.

## Como executar o programa

Antes de executar o programa, é necessário criar um arquivo `.env` na raiz do projeto e definir a variável de ambiente `API_KEY` com uma chave de API válida do Unsplash.

Para executar o programa, é necessário ter o Python instalado. Você pode instalar as dependências necessárias com o seguinte comando:

```bash
pip install -r requirements.txt
```

Em seguida, execute o seguinte comando para iniciar o programa:

```bash
python random_wallpaper_gui.py
```

O programa exibirá uma janela com opções de pesquisa e intervalo de tempo. Clique no botão "Buscar" para definir uma nova imagem como papel de parede. O programa atualizará automaticamente o papel de parede no intervalo de tempo especificado.
