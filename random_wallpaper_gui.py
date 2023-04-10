import configparser
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
        height = 230
        screenwidth = master.winfo_screenwidth()
        screenheight = master.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height,
                                    (screenwidth - width) / 2, (screenheight - height) / 2)

        master.geometry(alignstr)
        master.resizable(width=False, height=False)

        # Definir ícone do programa
        icon = Image.open("icon.ico")
        icon = ImageTk.PhotoImage(icon)
        master.iconphoto(False, icon)

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

        self.orientation_value = tk.StringVar()

        self.orientation_landscape = tk.Radiobutton(
            master, text="Landscape", variable=self.orientation_value, value="landscape")
        self.orientation_landscape.place(x=10, y=150, width=100, height=30)
        self.orientation_landscape.select()

        self.orientation_portrait = tk.Radiobutton(
            master, text="Portrait", variable=self.orientation_value, value="portrait")
        self.orientation_portrait.place(x=110, y=150, width=100, height=30)

        self.orientation_square = tk.Radiobutton(
            master, text="Square", variable=self.orientation_value, value="squarish")
        self.orientation_square.place(x=210, y=150, width=100, height=30)

        search_button = tk.Button(master)
        search_button["justify"] = "center"
        search_button["text"] = "Novo Wallpaper"

        search_button.bind("<Enter>", lambda e: search_button.config(
            bg="light blue", cursor="hand2"))
        search_button.bind("<Leave>", lambda e: search_button.config(
            bg="SystemButtonFace", cursor="arrow"))

        search_button.place(x=10, y=190, width=300, height=30)
        search_button["command"] = self.set_wallpaper

        self.image_label = tk.Label(master)
        self.image_label["justify"] = "center"
        self.image_label.place(x=320, y=10, width=300, height=180)

        self.time_remaining_label = tk.Label(master)
        self.time_remaining_label["justify"] = "center"
        self.time_remaining_label["text"] = "⬅️ Clique em 'Novo Wallpaper' para começar"
        self.time_remaining_label.place(x=320, y=190, width=300, height=30)

        # Carrega a imagem usando a função preview_wallpaper
        self.preview_wallpaper()
        self.api = RandomWallpaperAPI()

        # Carrega o arquivo de configuração caso exista
        self.config = configparser.ConfigParser()
        if os.path.exists("config.ini"):
            self.config.read("config.ini")
            self.search_entry.delete(0, tk.END)
            self.search_entry.insert(0, self.config["RW"]["search_term"])
            self.time_entry.delete(0, tk.END)
            self.time_entry.insert(0, self.config["RW"]["time_interval"])
            self.orientation_value.set(self.config["RW"]["orientation_value"])

    def preview_wallpaper(self):
        # Carrega a imagem do diretório ./Pictures
        picture_dir = "./Pictures"
        picture_files = os.listdir(picture_dir)
        if len(picture_files) > 0:
            # Ordena por imagem mais recente
            picture_files.sort(key=lambda x: os.path.getmtime(
                os.path.join(picture_dir, x)), reverse=True)
            picture_file = os.path.join(picture_dir, picture_files[0])
            picture_image = Image.open(picture_file)

            # Redimensiona a imagem para as proporções corretas
            picture_image.thumbnail((280, 180))
            picture_photo = ImageTk.PhotoImage(picture_image)
            self.image_label.config(image=picture_photo)
            self.image_label.image = picture_photo

        else:
            self.image_label.config(text="Nenhuma imagem encontrada")

    # Atualiza o tempo restante para a próxima atualização
    def update_time_remaining(self, time_remaining):
        self.time_remaining_label["text"] = ""

        hours = time_remaining // 3600
        minutes = (time_remaining % 3600) // 60
        seconds = time_remaining % 60

        time_parts = []
        if hours:
            time_parts.append(
                f"{hours:02d} hora{'s' if hours > 1 else ''}")
        if minutes:
            time_parts.append(
                f"{minutes:02d} minuto{'s' if minutes > 1 else ''}")
        if seconds:
            time_parts.append(
                f"{seconds:02d} segundo{'s' if seconds > 1 else ''}")

        self.time_remaining_label["text"] = "Próxima atualização em " + \
            ", ".join(time_parts)

        if time_remaining > 0:
            self.after_time_remaining = self.master.after(
                1000, self.update_time_remaining, time_remaining - 1)

    def set_wallpaper(self):
        search_term = self.search_entry.get()
        time_interval = int(self.time_entry.get()) * 60 * 1000
        orientation_value = self.orientation_value.get()

        # Cancela o after do wallpaper anterior (se existir)
        if "after_wallpaper" in dir(self):
            root.after_cancel(self.after_wallpaper)

        # Cancela o after do tempo restante anterior (se existir)
        if "after_time_remaining" in dir(self):
            root.after_cancel(self.after_time_remaining)

        # Tenta definir o papel de parede
        try:
            self.api.set_wallpaper(search_term, orientation_value)
            self.after_wallpaper = self.master.after(
                time_interval, self.set_wallpaper)
            self.preview_wallpaper()
            self.update_time_remaining(time_interval // 1000)

            # Salva as configurações
            self.config["RW"] = {
                "search_term": search_term,
                "time_interval": time_interval // 1000 // 60,
                "orientation_value": orientation_value
            }
            with open("config.ini", "w") as configfile:
                self.config.write(configfile)

        except ValueError as e:
            messagebox.showerror("Erro", str(e))
            return


if __name__ == "__main__":
    root = tk.Tk()
    app = RandomWallpaperGUI(root)
    root.mainloop()
