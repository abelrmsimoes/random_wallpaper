import os
import configparser
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox, ttk

from random_wallpaper_api import RandomWallpaperAPI


class RandomWallpaperGUI:
    def __init__(self, master):
        self.master = master
        master.title("Random Wallpaper")
        width = 620
        height = 255
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

        self.settings_frame = tk.Frame(master)
        self.settings_frame.place(
            x=0, y=0, width=width * 0.5, height=height * 0.85)
        self.settings_frame["relief"] = "groove"

        self.image_frame = tk.Frame(master)
        self.image_frame.place(
            x=width * 0.5, y=0, width=width * 0.5, height=height * 0.85)
        self.image_frame["relief"] = "groove"

        self.button_frame = tk.Frame(master)
        self.button_frame.place(
            x=0, y=height * 0.85, width=width * 0.5, height=height * 0.15)
        self.button_frame["relief"] = "groove"

        self.timer_frame = tk.Frame(master)
        self.timer_frame.place(
            x=width * 0.5, y=height * 0.85, width=width * 0.5, height=height * 0.15)
        self.timer_frame["relief"] = "groove"

        # Cria duas abas, uma para o Unsplash e outra para o Wallhaven
        self.notebook = ttk.Notebook(self.settings_frame)
        self.notebook.place(x=0, y=0, width=620, height=250)

        self.unsplash_frame = tk.Frame(self.notebook)
        self.unsplash_frame.place(x=0, y=0, width=620, height=250)
        self.unsplash_frame["borderwidth"] = "1px"
        self.unsplash_frame["relief"] = "groove"

        self.wallhaven_frame = tk.Frame(self.notebook)
        self.wallhaven_frame.place(x=0, y=0, width=620, height=250)
        self.wallhaven_frame["borderwidth"] = "1px"
        self.wallhaven_frame["relief"] = "groove"

        self.notebook.add(self.unsplash_frame, text="Unsplash")
        self.notebook.add(self.wallhaven_frame, text="Wallhaven")

        # Verificar se a pasta não existe e criá-la
        if not os.path.exists(os.path.join(os.path.expanduser("."), "Pictures")):
            os.makedirs(os.path.join(os.path.expanduser("."), "Pictures"))

        # region ## Unsplash Frame ##
        search_label_unsplash = tk.Label(self.unsplash_frame)
        search_label_unsplash["justify"] = "center"
        search_label_unsplash["text"] = "Pesquise o termo de busca:"
        search_label_unsplash.place(
            x=5, y=5, width=width * 0.5 - 10, height=20)

        self.search_entry_unsplash = tk.Entry(self.unsplash_frame)
        self.search_entry_unsplash["justify"] = "center"
        self.search_entry_unsplash.insert(0, "space; mountains; forest; rain;")
        self.search_entry_unsplash.place(
            x=5, y=25, width=width * 0.5 - 10, height=25)

        time_label_unsplash = tk.Label(self.unsplash_frame)
        time_label_unsplash["justify"] = "center"
        time_label_unsplash["text"] = "Tempo em minutos para a atualização:"
        time_label_unsplash.place(x=5, y=60, width=width * 0.5 - 10, height=20)

        self.time_entry_unsplash = tk.Entry(self.unsplash_frame)
        self.time_entry_unsplash["justify"] = "center"
        self.time_entry_unsplash.insert(0, "30")
        self.time_entry_unsplash.place(
            x=5, y=80, width=width * 0.5 - 10, height=25)

        self.orientation_unsplash = tk.StringVar()
        self.orientation_unsplash.set("landscape")
        self.orientation_unsplash_label = tk.Label(self.unsplash_frame)
        self.orientation_unsplash_label["justify"] = "center"
        self.orientation_unsplash_label["text"] = "Orientação da imagem:"
        self.orientation_unsplash_label.place(
            x=5, y=115, width=width * 0.5 - 10, height=20)

        # Radiobuttons para escolher a orientação lado a lado
        self.orientation_unsplash_landscape = tk.Radiobutton(
            self.unsplash_frame, text="Landscape", variable=self.orientation_unsplash, value="landscape")
        self.orientation_unsplash_landscape.place(
            x=5, y=135, width=100, height=20)

        self.orientation_unsplash_portrait = tk.Radiobutton(
            self.unsplash_frame, text="Portrait", variable=self.orientation_unsplash, value="portrait")
        self.orientation_unsplash_portrait.place(
            x=105, y=135, width=100, height=20)

        self.orientation_unsplash_squarish = tk.Radiobutton(
            self.unsplash_frame, text="Squarish", variable=self.orientation_unsplash, value="squarish")
        self.orientation_unsplash_squarish.place(
            x=205, y=135, width=100, height=20)

        self.featured_unsplash = tk.IntVar()
        self.featured_unsplash.set(0)
        self.featured_unsplash_check = tk.Checkbutton(
            self.unsplash_frame, text="Somente imagens em destaque", variable=self.featured_unsplash)
        self.featured_unsplash_check.place(
            x=5, y=165, width=width * 0.5 - 10, height=20)
        # endregion

        # region ## Wallhaven Frame ##
        search_label_wallhaven = tk.Label(self.wallhaven_frame)
        search_label_wallhaven["justify"] = "center"
        search_label_wallhaven["text"] = "Pesquise o termo de busca:"
        search_label_wallhaven.place(
            x=5, y=5, width=width * 0.5 - 10, height=20)

        self.search_entry_wallhaven = tk.Entry(self.wallhaven_frame)
        self.search_entry_wallhaven["justify"] = "center"
        self.search_entry_wallhaven.insert(
            0, "space; mountains; forest; rain;")
        self.search_entry_wallhaven.place(
            x=5, y=25, width=width * 0.5 - 10, height=25)

        time_label_wallhaven = tk.Label(self.wallhaven_frame)
        time_label_wallhaven["justify"] = "center"
        time_label_wallhaven["text"] = "Tempo em minutos para a atualização:"
        time_label_wallhaven.place(
            x=5, y=60, width=width * 0.5 - 10, height=20)

        self.time_entry_wallhaven = tk.Entry(self.wallhaven_frame)
        self.time_entry_wallhaven["justify"] = "center"
        self.time_entry_wallhaven.insert(0, "30")
        self.time_entry_wallhaven.place(
            x=5, y=80, width=width * 0.5 - 10, height=25)

        self.aspect_ratio_wallhaven = tk.StringVar()
        self.aspect_ratio_wallhaven.set("16x9")
        self.aspect_ratio_wallhaven_label = tk.Label(self.wallhaven_frame)
        self.aspect_ratio_wallhaven_label["justify"] = "center"
        self.aspect_ratio_wallhaven_label["text"] = "Proporção da imagem:"
        self.aspect_ratio_wallhaven_label.place(
            x=5, y=115, width=width * 0.5 - 10, height=20)

        self.aspect_ratio_wallhaven_16x9 = tk.Radiobutton(
            self.wallhaven_frame, text="16x9", variable=self.aspect_ratio_wallhaven, value="16x9")
        self.aspect_ratio_wallhaven_16x9.place(
            x=5, y=135, width=100, height=20)

        self.aspect_ratio_wallhaven_9x16 = tk.Radiobutton(
            self.wallhaven_frame, text="9x16", variable=self.aspect_ratio_wallhaven, value="9x16")
        self.aspect_ratio_wallhaven_9x16.place(
            x=105, y=135, width=100, height=20)

        self.aspect_ratio_wallhaven_1x1 = tk.Radiobutton(
            self.wallhaven_frame, text="1x1", variable=self.aspect_ratio_wallhaven, value="1x1")
        self.aspect_ratio_wallhaven_1x1.place(
            x=205, y=135, width=100, height=20)

        self.nsfw_wallhaven = tk.IntVar()
        self.nsfw_wallhaven.set(0)
        self.nsfw_wallhaven_check = tk.Checkbutton(
            self.wallhaven_frame, text="Ativar imagens NSFW", variable=self.nsfw_wallhaven)
        self.nsfw_wallhaven_check.place(
            x=5, y=165, width=width * 0.5 - 10, height=20)

        # endregion

        ## Button Frame ##
        search_button = tk.Button(self.button_frame)
        search_button["justify"] = "center"
        search_button["text"] = "Novo Wallpaper"
        search_button.place(x=5, y=5, width=width * 0.5 - 10,
                            height=height * 0.15 - 10)
        search_button.bind("<Enter>", lambda e: search_button.config(
            bg="light blue", cursor="hand2"))
        search_button.bind("<Leave>", lambda e: search_button.config(
            bg="SystemButtonFace", cursor="arrow"))
        search_button["command"] = self.set_wallpaper

        ## Image Frame ##
        self.image_label = tk.Label(self.image_frame)
        self.image_label["justify"] = "center"
        self.image_label.place(width=width * 0.5, height=height * 0.85)

        ## Timer Frame ##
        self.time_remaining_label = tk.Label(self.timer_frame)
        self.time_remaining_label["justify"] = "center"
        self.time_remaining_label.place(
            width=width * 0.5, height=height * 0.15)
        self.time_remaining_label["wraplength"] = width * 0.5 - 10
        self.time_remaining_label["text"] = "⬅️ Clique em 'Novo Wallpaper' para começar"

        # Carrega a imagem usando a função preview_wallpaper
        self.preview_wallpaper()
        self.api = RandomWallpaperAPI()

        # Carrega o arquivo de configuração caso exista
        self.config = configparser.ConfigParser()
        if os.path.exists("config.ini"):
            try:
                self.config.read("config.ini")

                if self.config.has_section("RandomWallpaper"):
                    for index in range(self.notebook.index("end")):
                        tab_name = self.notebook.tab(index, "text")
                        if tab_name == self.config["RandomWallpaper"]["visible_tab"]:
                            self.notebook.select(index)

                # Carrega as configurações da seção Unsplash
                if self.config.has_section("Unsplash"):
                    self.search_entry_unsplash.delete(0, tk.END)
                    self.search_entry_unsplash.insert(
                        0, self.config["Unsplash"]["search_term"])
                    self.time_entry_unsplash.delete(0, tk.END)
                    self.time_entry_unsplash.insert(
                        0, self.config["Unsplash"]["time_interval"])
                    self.orientation_unsplash.set(
                        self.config["Unsplash"]["orientation_value"])
                    self.featured_unsplash.set(
                        self.config["Unsplash"]["featured_value"])

                # Carrega as configurações da seção Wallhaven
                if self.config.has_section("Wallhaven"):
                    self.search_entry_wallhaven.delete(0, tk.END)
                    self.search_entry_wallhaven.insert(
                        0, self.config["Wallhaven"]["search_term"])
                    self.time_entry_wallhaven.delete(0, tk.END)
                    self.time_entry_wallhaven.insert(
                        0, self.config["Wallhaven"]["time_interval"])
                    self.aspect_ratio_wallhaven.set(
                        self.config["Wallhaven"]["ratio_value"])
                    self.nsfw_wallhaven.set(
                        self.config["Wallhaven"]["nsfw_value"])

            except:
                messagebox.showwarning(
                    "Atenção", "Erro ao carregar o arquivo de configuração")
                try:
                    os.remove("config.ini")
                except:
                    pass

    def preview_wallpaper(self):
        # Carrega a imagem do diretório ./Pictures
        picture_dir = "./Pictures"
        picture_files = os.listdir(picture_dir)
        if len(picture_files) > 0:
            # Ordena por imagem mais recente
            picture_files.sort(key=lambda x: os.path.getmtime(
                os.path.join(picture_dir, x)), reverse=True)
            try:
                picture_file = os.path.join(picture_dir, picture_files[0])
                picture_image = Image.open(picture_file)

                # Redimensiona a imagem para as proporções corretas
                picture_image.thumbnail((280, 180), Image.Resampling.LANCZOS)
                picture_photo = ImageTk.PhotoImage(picture_image)
                self.image_label.config(image=picture_photo)
                self.image_label.image = picture_photo
            except:
                os.remove(picture_file)

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

        if len(time_parts) > 0:
            self.time_remaining_label["text"] = "Próxima atualização em " + \
                ", ".join(time_parts)

        if time_remaining > 0:
            self.after_time_remaining = self.master.after(
                1000, self.update_time_remaining, time_remaining - 1)

    def set_wallpaper(self):

        self.config["RandomWallpaper"] = {
            "visible_tab": self.notebook.tab(self.notebook.select(), "text"),
        }

        # Cancela o after do wallpaper anterior (se existir)
        if "after_wallpaper" in dir(self):
            root.after_cancel(self.after_wallpaper)

        # Cancela o after do tempo restante anterior (se existir)
        if "after_time_remaining" in dir(self):
            root.after_cancel(self.after_time_remaining)

        try:
            if self.notebook.tab(self.notebook.select(), "text") == "Unsplash":
                search_term = self.search_entry_unsplash.get()
                time_interval = int(self.time_entry_unsplash.get()) * 60 * 1000
                orientation_value = self.orientation_unsplash.get()
                featured_image = self.featured_unsplash.get()

                # Tenta definir o papel de parede
                self.api.set_unsplash_wallpaper(
                    search_term, orientation_value, featured_image)
                self.after_wallpaper = self.master.after(
                    time_interval, self.set_wallpaper)

                # Salva as configurações
                self.config["Unsplash"] = {
                    "search_term": search_term,
                    "time_interval": time_interval // 1000 // 60,
                    "orientation_value": orientation_value,
                    "featured_value": featured_image
                }
                with open("config.ini", "w") as configfile:
                    self.config.write(configfile)

            if self.notebook.tab(self.notebook.select(), "text") == "Wallhaven":
                search_term = self.search_entry_wallhaven.get()
                time_interval = int(
                    self.time_entry_wallhaven.get()) * 60 * 1000
                ratio_value = self.aspect_ratio_wallhaven.get()
                nsfw_value = self.nsfw_wallhaven.get()

                # Tenta definir o papel de parede
                self.api.set_wallhaven_wallpaper(
                    search_term, ratio_value, nsfw_value)
                self.after_wallpaper = self.master.after(
                    time_interval, self.set_wallpaper)

                self.config["Wallhaven"] = {
                    "search_term": search_term,
                    "time_interval": time_interval // 1000 // 60,
                    "ratio_value": ratio_value,
                    "nsfw_value": nsfw_value
                }
                with open("config.ini", "w") as configfile:
                    self.config.write(configfile)

            self.update_time_remaining(time_interval // 1000)
            self.preview_wallpaper()

        except ValueError as e:
            messagebox.showerror("Erro", str(e))
            return


if __name__ == "__main__":
    root = tk.Tk()
    app = RandomWallpaperGUI(root)
    root.mainloop()
