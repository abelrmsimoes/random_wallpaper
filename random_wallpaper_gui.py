import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

from random_wallpaper_api import RandomWallpaperAPI


class RandomWallpaperGUI:
    def __init__(self, master):
        self.master = master
        master.title("Random Wallpaper")
        width = 620
        height = 200
        screenwidth = master.winfo_screenwidth()
        screenheight = master.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height,
                                    (screenwidth - width) / 2, (screenheight - height) / 2)

        master.geometry(alignstr)
        master.resizable(width=False, height=False)

        # Verificar se a pasta não existe e criá-la
        if not os.path.exists(os.path.join(os.path.expanduser("."), "Pictures")):
            os.makedirs(os.path.join(os.path.expanduser("."), "Pictures"))

        search_label = tk.Label(master)
        search_label["justify"] = "center"
        search_label["text"] = "Pesquise o termo de busca:"
        search_label.place(x=10, y=10, width=300, height=30)

        self.search_entry = tk.Entry(master)
        self.search_entry["justify"] = "center"
        self.search_entry.insert(0, "mountains")
        self.search_entry.place(x=10, y=40, width=300, height=25)

        time_label = tk.Label(master)
        time_label["justify"] = "center"
        time_label["text"] = "Tempo em minutos para a atualização:"
        time_label.place(x=10, y=80, width=300, height=30)

        self.time_entry = tk.Entry(master)
        self.time_entry["justify"] = "center"
        self.time_entry.insert(0, "30")
        self.time_entry.place(x=10, y=110, width=300, height=25)

        search_button = tk.Button(master)
        search_button["justify"] = "center"
        search_button["text"] = "Buscar"
        search_button.place(x=10, y=150, width=300, height=30)
        search_button["command"] = self.set_wallpaper

        # Cria um Label para exibir a imagem
        self.image_label = tk.Label(master)
        self.image_label.place(x=320, y=10, width=300, height=180)

        # Carrega a imagem usando a função preview_wallpaper
        self.preview_wallpaper()

        self.api = RandomWallpaperAPI()

    def preview_wallpaper(self):
        # Carrega a imagem do diretório ./Pictures (assumindo que há apenas uma imagem lá)
        picture_dir = "./Pictures"
        picture_files = os.listdir(picture_dir)
        if len(picture_files) > 0:
            picture_file = os.path.join(picture_dir, picture_files[0])
            picture_image = Image.open(picture_file)

            # Redimensiona a imagem para as proporções corretas
            picture_image.thumbnail((300, 180))
            picture_photo = ImageTk.PhotoImage(picture_image)
            self.image_label.config(image=picture_photo)
            self.image_label.image = picture_photo

    def set_wallpaper(self):
        search_term = self.search_entry.get()
        time_interval = int(self.time_entry.get()) * 60 * 1000

        try:
            self.api.set_wallpaper(search_term)
            self.master.after(time_interval, self.set_wallpaper)

            # Atualiza a imagem
            self.preview_wallpaper()
        except ValueError as e:
            message = "Não foi possível encontrar uma imagem adequada. Tente novamente mais tarde."
            messagebox.showerror("Erro", message)
        except Exception as e:
            messagebox.showerror("Erro", str(e))
            # exibe o erro no terminal
            raise e


if __name__ == "__main__":
    root = tk.Tk()
    app = RandomWallpaperGUI(root)
    root.mainloop()