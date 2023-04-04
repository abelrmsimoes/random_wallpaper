import os
import re
import ctypes
import requests
import urllib.parse
from dotenv import load_dotenv


class RandomWallpaperAPI:
    def __init__(self, search_term="mountains", orientation_value="landscape"):
        self.search_term = search_term
        self.orientation_value = orientation_value

    def set_wallpaper(self, search_term, orientation_value):
        # Obtém o valor da variável de ambiente "API_KEY" e realiza a pesquisa
        load_dotenv()
        client_id = os.getenv("API_KEY")
        url = f"https://apaaaaai.unsplash.com/photos/random?client_id={client_id}&query={urllib.parse.quote(search_term)}&orientation={orientation_value}"

        # Verifica se existe conexão com a internet
        try:
            response = requests.get(url)
            data = response.json()
        except requests.exceptions.ConnectionError:
            raise ValueError(
                "Não foi possível realizar a pesquisa. Verifique sua conexão com a internet.")

        # Verifica se a pesquisa retornou uma imagem
        try:
            photo_url = data['urls']['full']
        except KeyError:
            raise ValueError(
                "Não foi possível encontrar uma imagem com esses parâmetros.")

        # Definir o caminho completo para a pasta "Pictures" do usuário
        user_pictures_dir = os.path.join(os.path.expanduser("."), "Pictures")

        # Definir o caminho completo para o arquivo de imagem
        photo_filename = os.path.splitext(photo_url.split("/")[-1])[0]
        photo_filename = re.sub(r'[^a-zA-Z0-9-]', '', photo_filename)
        photo_filename = photo_filename + ".jpg"
        photo_path = os.path.join(user_pictures_dir, photo_filename)

        # Limpar o conteúdo da pasta Pictures antes de baixar a nova imagem
        for file in os.listdir(user_pictures_dir):
            if file.endswith(".jpg"):
                os.remove(os.path.join(user_pictures_dir, file))

        # Baixar a imagem e salvá-la na pasta "Pictures" do usuário
        response = requests.get(photo_url)
        with open(photo_path, "wb") as photo_file:
            photo_file.write(response.content)

        # Definir a imagem como papel de parede
        SPI_SETDESKWALLPAPER = 20
        ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER, 0, os.path.abspath(photo_path), 0)


if __name__ == '__main__':
    rw = RandomWallpaperAPI()
