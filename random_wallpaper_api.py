import os
import re
import ctypes
import requests
import urllib.parse
from dotenv import load_dotenv


class RandomWallpaperAPI:
    def set_wallpaper(self, search_term, orientation_value):
        self.search_term = search_term
        self.orientation_value = orientation_value

        # Obtém o valor da variável de ambiente "API_KEY" e realiza a pesquisa
        load_dotenv()
        client_id = os.getenv("API_KEY")
        url = f"https://api.unsplash.com/photos/random?client_id={client_id}&query={urllib.parse.quote(search_term)}&orientation={orientation_value}"

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
            photo_description = data['alt_description']
            photo_author = data['user']['name']
        except KeyError:
            raise ValueError(
                "Não foi possível encontrar uma imagem com esses parâmetros.")

        # Definir o caminho completo para a pasta "Pictures" do usuário
        user_pictures_dir = os.path.join(os.path.expanduser("."), "Pictures")

        photo_filename = photo_description + " - " + photo_author + ".jpg"
        photo_path = os.path.join(user_pictures_dir, photo_filename)

        # Mantem apenas as 10 imagens mais recentes na pasta "Pictures" do usuário
        photo_files = os.listdir(user_pictures_dir)
        photo_files.sort(reverse=True)
        for photo_file in photo_files[9:]:
            os.remove(os.path.join(user_pictures_dir, photo_file))

        # Verifica se a imagem já existe na pasta "Pictures" do usuário
        if not os.path.isfile(photo_path):
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
