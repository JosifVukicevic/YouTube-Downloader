from pytube import YouTube
import os
from moviepy.video.io.VideoFileClip import VideoFileClip
import tkinter as tk
from tkinter import filedialog

class YoutubeDownloader:
    def __init__(self, master):
        self.master = master
        master.title("Youtube preuzimanje i konvertovanje")
        master.geometry("600x300")

        # postavi ikonicu
        img = tk.PhotoImage(file="download.png")
        master.iconphoto(False, img)

        # postavi naslov i odvojene okvire za URL i dugme
        self.title_label = tk.Label(master, text="Youtube preuzimanje i konvertovanje", font=("Helvetica", 16))
        self.title_label.pack(pady=10)

        self.url_frame = tk.Frame(master)
        self.url_frame.pack()

        self.url_label = tk.Label(self.url_frame, text="Unesite URL YouTube videa:")
        self.url_label.pack(side=tk.LEFT)

        self.url_entry = tk.Entry(self.url_frame, width=30)
        self.url_entry.pack(side=tk.LEFT)

        self.download_button = tk.Button(master, text="Preuzmi i konvertuj", command=self.download)
        self.download_button.pack(pady=10)

        self.status_label = tk.Label(master, text="")
        self.status_label.pack()

    def download(self):
        url = self.url_entry.get()

        try:
            yt = YouTube(url)
            ys = yt.streams.get_highest_resolution()
        except:
            self.status_label.config(text="Došlo je do greške prilikom preuzimanja videa. Provjerite URL adresu.")
            return

        folder = "mp4"
        if not os.path.exists(folder):
            os.makedirs(folder)
        self.status_label.config(text="Preuzimanje započelo...")
        try:
            ys.download(folder)
        except:
            self.status_label.config(text="Došlo je do greške prilikom preuzimanja videa.")
            return

        input_file = os.path.join(folder, ys.default_filename)
        output_file = os.path.join("mp3", f"{yt.title}.mp3")
        try:
            with VideoFileClip(input_file) as video:
                audio = video.audio
                self.status_label.config(text="Konvertovanje započelo...")
                audio.write_audiofile(output_file)
        except:
            self.status_label.config(text="Došlo je do greške prilikom konvertovanja videa.")
            return

        os.remove(input_file)
        self.status_label.config(text=f"Završeno! Preuzeti audio zapis je sačuvan u folderu 'mp3' kao '{yt.title}.mp3'.")

root = tk.Tk()
my_gui = YoutubeDownloader(root)

# centriraj prozor na ekranu
window_width = root.winfo_reqwidth()
window_height = root.winfo_reqheight()
position_right = int(root.winfo_screenwidth()/2 - window_width/2)
position_down = int(root.winfo_screenheight()/2 - window_height/2)
root.geometry("+{}+{}".format(position_right, position_down))

root.mainloop()
