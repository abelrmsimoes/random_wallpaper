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
        # Configure a chave de API do Unsplash
        load_dotenv()
        # Obtém o valor da variável de ambiente "API_KEY"
        client_id = os.getenv("API_KEY")

        # Realize uma pesquisa com a API
        url = f"https://api.unsplash.com/photos/random?client_id={client_id}&query={urllib.parse.quote(search_term)}&orientation={orientation_value}"

        response = requests.get(url)
        data = response.json()

        try:
            photo_url = data['urls']['full']
        except KeyError:
            return ValueError("Não foi possível encontrar uma imagem com esses parâmetros.")

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
