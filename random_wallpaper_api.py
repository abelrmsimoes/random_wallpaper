import os
import ctypes
import random
import requests
import urllib.parse
from dotenv import load_dotenv


class RandomWallpaperAPI:
    def set_unsplash_wallpaper(self, search_term, orientation_value, featured_image):
        self.search_term = search_term
        self.orientation_value = orientation_value
        self.featured_image = featured_image

        # Obtém o valor da variável de ambiente "API_KEY" e realiza a pesquisa
        load_dotenv()
        api_key = os.getenv("UNSPLASH_KEY")
        url = f"https://api.unsplash.com/photos/random?client_id={api_key}&query={urllib.parse.quote(search_term)}&orientation={orientation_value}&featured={featured_image}"

        # Verifica se existe conexão com a internet
        try:
            response = requests.get(url, allow_redirects=True)
            if response.status_code != 200:
                for i in range(3):
                    response = requests.get(url, allow_redirects=True)
                    if response.status_code == 200:
                        break
                    else:
                        continue
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
        photo_files.sort(key=lambda x: os.path.getmtime(
            os.path.join(user_pictures_dir, x)), reverse=True)
        for photo_file in photo_files[9:]:
            os.remove(os.path.join(user_pictures_dir, photo_file))

        if not os.path.isfile(photo_path):
            response = requests.get(photo_url, allow_redirects=True)
            # se o status for diferente de 200, tenta novamente por 3 vezes
            if response.status_code != 200:
                for i in range(3):
                    response = requests.get(photo_url, allow_redirects=True)
                    if response.status_code == 200:
                        break
                    else:
                        continue
            with open(photo_path, "wb") as photo_file:
                photo_file.write(response.content)

        win32_set_wallpaper(photo_path)

    # Função para buscar imagens da api do Wallhaven
    def set_wallhaven_wallpaper(self, search_term, ratio_value, nsfw_value):
        self.search_term = search_term
        self.ratio_value = ratio_value
        self.nsfw_value = nsfw_value

        load_dotenv()
        api_key = os.getenv("WALLHAVEN_KEY")

        array_term = list(filter(None, search_term.split(";")))
        search_term = random.choice(array_term)

        if nsfw_value == "true":
            purity = "111"
        else:
            purity = "100"

        url = f"https://wallhaven.cc/api/v1/search?apikey={api_key}&q={urllib.parse.quote(search_term)}&ratios={ratio_value}&purity={purity}&sorting=random"

        # Verifica se existe conexão com a internet
        try:
            response = requests.get(url, allow_redirects=True)
            # se o status for diferente de 200, tenta novamente por 3 vezes
            if response.status_code != 200:
                for i in range(3):
                    response = requests.get(url, allow_redirects=True)
                    if response.status_code == 200:
                        break
                    else:
                        continue
            data = response.json()
        except requests.exceptions.ConnectionError:
            raise ValueError(
                "Não foi possível realizar a pesquisa. Verifique sua conexão com a internet.")

        # Verifica se a pesquisa retornou uma imagem
        try:
            photo_url = data['data'][0]['path']
            photo_filename = data['data'][0]['path'].split('/')[-1]
        except KeyError:
            raise ValueError(
                "Não foi possível encontrar uma imagem com esses parâmetros.")

        # Definir o caminho completo para a pasta "Pictures" do usuário
        user_pictures_dir = os.path.join(os.path.expanduser("."), "Pictures")

        photo_path = os.path.join(user_pictures_dir, photo_filename)

        # Mantem apenas as 10 imagens mais recentes na pasta "Pictures" do usuário
        photo_files = os.listdir(user_pictures_dir)
        photo_files.sort(key=lambda x: os.path.getmtime(
            os.path.join(user_pictures_dir, x)), reverse=True)
        for photo_file in photo_files[9:]:
            os.remove(os.path.join(user_pictures_dir, photo_file))

        response = requests.get(photo_url, allow_redirects=True)
        # se o status for diferente de 200, tenta novamente por 3 vezes
        if response.status_code != 200:
            for i in range(3):
                response = requests.get(photo_url, allow_redirects=True)
                if response.status_code == 200:
                    break
                else:
                    continue

        with open(photo_path, "wb") as photo_file:
            photo_file.write(response.content)

        win32_set_wallpaper(photo_path)


def win32_set_wallpaper(image_path):
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER, 0, os.path.abspath(image_path), 0)


if __name__ == '__main__':
    rw = RandomWallpaperAPI()
