from tkinter import Tk, ttk,Label,Entry,Button, Text, filedialog, Scrollbar
import tkinter as tk
from pytube import YouTube, Playlist
import os
import configparser
from urllib.parse import urlparse, parse_qs

from PIL import ImageTk, Image
import io
import requests

from tkfontawesome import icon_to_image
from idlelib.tooltip import Hovertip



# ! playlist cekme
# playlist = Playlist("https://www.youtube.com/playlist?list=PLx0sYbCqOb8TBPRdmBHs5Iftvv9TPboYG")
# playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

# for url in playlist.video_urls:
#     video = YouTube(url)
#     stream = video.streams.first()
#     stream.download()

# ! kalite listeleme
# url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
# yt = YouTube(url)

# # Tüm video kalitesi seçeneklerini listele
# for stream in yt.streams.filter(type="video"):
#     print(stream)

# # Tüm ses kalitesi seçeneklerini listele
# for stream in yt.streams.filter(type="audio"):
#     print(stream)

def download_video(data):

    print("video")
    yt = YouTube(data["url"])
    stream = yt.streams.first()
    stream.download(download_dir)

def download_audio(data):

    yt = YouTube(data["url"])
    stream = yt.streams.filter(only_audio=True).first()
    stream.download(download_dir)
    
    # * file name changle
    default_filename = stream.default_filename
    os.rename(os.path.join(download_dir, default_filename), os.path.join(download_dir, data["title"]))

    # Open file dialog to select download directory
    # download_dir = filedialog.askdirectory()
    # Download audio to selected directory
    # stream.download(output_path=download_dir)

config_file = 'settings.ini'

# * Create settings file if it doesn't exist
if not os.path.exists(config_file):
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'download_dir': os.path.expanduser("~")}
    with open(config_file, 'w') as f:
        config.write(f)

# * Read settings from file
config = configparser.ConfigParser()
config.read(config_file)
download_dir = config['DEFAULT']['download_dir']

# * Function to open file dialog and set download directory
def set_download_dir():
    global download_dir
    download_dir = filedialog.askdirectory()
    config['DEFAULT']['download_dir'] = download_dir
    with open(config_file, 'w') as f:
        config.write(f)

# * Function to open settings window
def open_settings_window():
    # * Create settings window
    settings_window = Tk()
    settings_window.geometry("600x500")
    settings_window.resizable(False, False)
    settings_window.title("Settings")
    settings_window.iconbitmap("favicon.ico")

    # *Create download directory label and button
    download_dir_label = Label(settings_window, text=download_dir)
    download_dir_label.grid(row=0, column=0, padx=5, pady=5)
    set_download_dir_button = Button(settings_window, text="Set Download Directory", command=set_download_dir)
    set_download_dir_button.grid(row=0, column=1, padx=5, pady=5)

    # * Function to save settings and close window
    def save_settings():
        with open(config_file, 'w') as f:
            config.write(f)
        settings_window.destroy()

    # * Create save button
    save_button = Button(settings_window, text="Save", command=save_settings)
    save_button.grid(row=1, column=1, padx=5, pady=5)

    # * Run settings window
    settings_window.mainloop()

# * Function to open settings window
def open_about_window():
    # * Create about window
    about_window = Tk()
    about_window.geometry("300x200")
    about_window.resizable(False, False)
    about_window.title("About")
    about_window.iconbitmap("favicon.ico")

    # * about 
    about_label = Label(
        about_window, 
        text="MedDown \n Downloader \n v1.0"
        )
    about_label.pack(
        fill="x", 
        expand=True
        )

    # * Run about window
    about_window.mainloop()

# * url check
def is_valid_youtube_url(url):
    parsed_url = urlparse(url)
    if parsed_url.netloc != 'www.youtube.com':
        return False


# * sellect media type
def media_download_sellect_check(data):
    if ( data["type"] ):
        download_audio(data)
    else:
        download_video(data)


# * Reading data from file
def dataRead():
    import json
    # * read
    with open('data.json') as f:
        yt_data = json.load(f)
    return yt_data

# * Write modified data to JSON file
def dataWrite(data):
    import json
    # * Write
    with open('data.json', 'w') as file:
        json.dump(data, file)

# * Remow data
def dataRemove(dataUrl):
    import json
    # * read
    with open('data.json') as f:
        yt_data = json.load(f)
    # * remove
    for item in yt_data:
        if item["url"] == dataUrl:
            yt_data.remove(item)
    # * Write
    with open('data.json', 'w') as file:
        json.dump(yt_data, file)

# * content media box create
def contentBox(dataTitle, dataImage, dataUrl, dataLength, dataAuthor, dataType):
    
    import ttkbootstrap as ttk 
    from tkfontawesome import icon_to_image
    from idlelib.tooltip import Hovertip

    def type_selection(dataUrl, dataType) :
        yt_data = dataRead()
        for item in yt_data:
            if item['url'] == dataUrl:
                item['type'] = dataType
                dataWrite(yt_data)
                return 
            
    def title_selection(dataUrl, dataTitle) :
        yt_data = dataRead()
        for item in yt_data:
            if item['url'] == dataUrl:
                item['title'] = dataTitle
                dataWrite(yt_data)
                return 
            
    data = {
        "title" : dataTitle,
        "url": dataUrl,
        "type": dataType,
    }


    content_container = tk.Frame(
        content,
        )
    content_container.pack(
        fill="x", 
        expand=True
        )
        
    yt_url = tk.Label(
        content_container, 
        text=dataUrl,
        )
    yt_url.pack(        
        side="left", 
        fill="both", 
        expand=True
        )
    yt_url.pack_forget()

    content_container_1 = tk.Frame(
        content_container, 
        borderwidth=1, 
        relief="solid",
        width=100,
        height=10,
        )
    content_container_1.pack(
        side="left", 
        fill="both", 
        expand=False
        )

    content_container_2 = tk.Frame(
        content_container, 
        borderwidth=1, 
        relief="solid",
        )
    content_container_2.pack(
        side="left", 
        fill="both", 
        expand=True
        )

    content_container_3 = tk.Frame(
        content_container, 
        borderwidth=1, 
        relief="solid",
        )
    content_container_3.pack(
        side="left", 
        fill="both", 
        expand=False
        )

    image_bytes = io.BytesIO(requests.get(dataImage).content)
    image = Image.open(image_bytes)
    image.thumbnail((100, 100))
    image_tk = ImageTk.PhotoImage(image)

    image_label = Label(
        content_container_1, 
        image=image_tk)
    image_label.image = image_tk
    image_label.pack(
        side="left", 
        fill="none"
        )
    
    def on_title_change(*args):
        title_selection(dataUrl, yt_title_var.get())
    yt_title_var = tk.StringVar(
        value= bytes(dataTitle, "utf-8").decode("raw_unicode_escape").encode("iso-8859-1").decode("utf-8"),
        )

    yt_title_var.trace('w',on_title_change)
    yt_title = Entry(
        content_container_2,
        textvariable=yt_title_var,
        width=48
        )
    yt_title.pack(
        side="left", 
        anchor="nw", 
        fill="x", 
        expand=True
        )

    yt_author = Label(
        content_container_2, 
        text=dataAuthor,
        padx=10, 
        pady=0
        )
    yt_author.place(
        relx=0, 
        rely=0.6
        )
    
    yt_quality = Label(
        content_container_2, 
        text="kalite",
        padx=10, 
        pady=0
        )
    yt_quality.place(
        relx=0.6, 
        rely=0.6
        )

    yt_length = Label(
        content_container_1, 
        text=dataLength,
        padx=5, 
        pady=5, 
        borderwidth=1, 
        relief="solid"
        )
    yt_length.place(
        relx=0.6, 
        rely=0.1
        )
    
    def destroy_button(dataUrl):
        content_container.destroy()
        dataRemove(dataUrl)

        yt_data = dataRead()

        if len(yt_data) > 0:
            media_leng.config(text= "Media : ( " + str(len(yt_data)) + " )" )
        else:
            media_leng.config(text= "Media : ( 0 )" )
            # ? default content
            iconYoutube = icon_to_image(
                "searchengin", 
                fill="#4267B2", 
                scale_to_width=64
                )
            content_null_icon = tk.Label(
                container,
                image=iconYoutube
                )
            content_null_icon.place(relx=0.5, rely=0.5, anchor="center")

            url_text = Label(
                container, 
                text="There is nothing here.",
                )
            url_text.place(relx=0.5, rely=0.6, anchor="center")

    yt_remov = Button(
        content_container_1, 
        text="x",
        command=lambda: destroy_button(dataUrl)
        )
    yt_remov.place(
        relx=0.1, 
        rely=0.1
        )
    
    from tkfontawesome import icon_to_image
    iconDownload2 = icon_to_image(
        "download", 
        fill="#4267B2", 
        scale_to_width=28
        )
    
    def yt_single_download(dataUrl):
        yt_data = dataRead()
        for item in yt_data:
            if item["url"] == dataUrl :
                media_download_sellect_check(item)

    yt_media_download_btn = ttk.Button(
        content_container_3, 
        image=iconDownload2, 
        bootstyle="secondary-outline", 
        command=lambda: yt_single_download(dataUrl)
        )
    yt_media_download_btn.pack(
        side="right",
        padx=10, 
        pady=10
        )
    Hovertip(
        yt_media_download_btn,
        'Download.', 
        hover_delay=1000
        )

    yt_media_download_sellect_data = tk.BooleanVar(
        value=dataType
        )
    yt_media_download_sellect_btn = ttk.Checkbutton(
        content_container_3, 
        text='Video / Sound', bootstyle="secondary-round-toggle", 
        variable=yt_media_download_sellect_data, 
        command=lambda: type_selection(dataUrl, yt_media_download_sellect_data.get())
        )
    yt_media_download_sellect_btn.pack(
        side="right",
        padx=10, 
        pady=10
        )
    Hovertip(
        yt_media_download_sellect_btn,
        'Select media type.', 
        hover_delay=1000
        )


# Function to add URL to list and show preview image
def add_url():
    # url = url_entry.get().strip()
    url = root.clipboard_get().strip()
    
    import json
    # * duplicate check
    def check_duplicate(url, yt_data):
        for item in yt_data:
            if item['url'] == url:
                return True
        return False
    # * JSON read
    with open('data.json') as f:
        yt_data = json.load(f)
    # * check
    if check_duplicate(url, yt_data):
        return
    # * -------------

    if not url and is_valid_youtube_url(url):
        return
    
    # Get preview image from YouTube video
    try:
        
        # status temizleme
        status_label.config(text="")


        # ! pytube title leng ... get problems..
        # yt = YouTube(url)
        # title = yt.title
        # length = yt.length
        # author = yt.author
        # preview_url = yt.thumbnail_url

        import urllib.request
        import re

        # Sayfanın HTML kodunu indirin
        html = urllib.request.urlopen(url)
        video_html = html.read().decode()

        def yt_time(video_html) :
            # Süre bilgisini çıkarmak için uygun kalıp (pattern) oluşturuyoruz
            time_pattern = re.compile(r'itemprop="duration" content="PT(\d+H)?(\d+M)?(\d+S)')

            # Uygun kalıpla eşleşen süre bilgisini alıyoruz
            time_match = time_pattern.search(video_html)

            # Süre bilgisini ekrana yazdırıyoruz
            if time_match:
                time = time_match.group(0)
                matches = re.findall(r'PT(\d+M)?(\d+S)?', time)[0]
                minutes = int(matches[0][:-1]) if matches[0] else 0
                seconds = int(matches[1][:-1]) if matches[1] else 0
                time = str(minutes) + ":" + str(seconds)
            else:
                time = "--:--"
            
            return time
        
        def yt_image(video_html) :
            match = re.search(r'<meta property="og:image" content="(.+?)">', video_html)
            if match:
                image_url = match.group(1)
            else:
                image_url = "https://www.youtube.com/img/desktop/unavailable/unavailable_video_dark_theme.png"
            return image_url

        # * title
        title = re.findall(r'"title":"(.*?)"', video_html)[0]
        # * time
        length = yt_time(video_html)
        # * chanel
        author = re.findall(r'"author":"(.*?)"', video_html)[0]
        # * image
        preview_url = yt_image(video_html)
        # * type
        media_type = media_download_sellect_data.get()
        
        new_data = {
            'title': title,
            'preview_url':  preview_url,
            'url':  url,
            'length': length,
            'author': author,
            'type': media_type,
        }

        contentBox(title, preview_url, url, length, author, media_type)

        yt_data.append(new_data)

        # JSON data add
        with open('data.json', 'w') as f:
            json.dump(yt_data, f)

        if len(yt_data) == 1:
            url_text.destroy()
            content_null_icon.destroy()
        
        media_leng.config(text= "Media : ( " + str(len(yt_data)) + " )" )


    except ValueError:
        # print(ValueError)
        status_label.config(text="Error")
        pass


# * window

import ttkbootstrap as ttk 

root = Tk()
root.geometry("600x500")
# root.minsize(600, 500)
root.resizable(False, False)

# ---------------------

# ? main container
container = tk.Frame(root)
container.pack(fill="both", expand=True)

# ? header
header = tk.Frame(container , background="#D3ECF7", padx=10, pady=10)
header.pack(side="top", fill="both")

# ? content
content = tk.Frame(container, background="#B0A8B9", padx=5, pady=5)
content.pack(fill="both", expand=True)

#----------------------------------
# * Scrollbar
scrollbar = ttk.Scrollbar(content, bootstyle="secondary-round")
scrollbar.pack(side="right", fill="y")

# * Canvas
contentCanvas = ttk.Canvas(content, yscrollcommand=scrollbar.set)
contentCanvas.pack(side="top",fill="both", expand=True)


# * Attach scrollbar to canvas
scrollbar.config(command=contentCanvas.yview)

# * Add content to canvas
content = ttk.Frame(contentCanvas)
content.pack(fill="both", expand=True)
content.bind("<Configure>", lambda e: contentCanvas.configure(scrollregion=contentCanvas.bbox("all")))

contentCanvas.create_window((0, 0), window=content)


# ? footer
footer = tk.Frame(container, background="#D3ECF7", pady=5)
footer.pack(side="bottom", fill="both")

# ---------------------



# * header

import ttkbootstrap as ttk 
from ttkbootstrap.constants import *


# https://fontawesome.com/v5/search?q=add&o=r&m=free
# https://ttkbootstrap.readthedocs.io/en/latest/styleguide/checkbutton/#round-toggle-button
# https://htmlcolorcodes.com/



iconAdd = icon_to_image("plus-circle", fill="#4267B2", scale_to_width=32)
add_url_btn = ttk.Button(header,image=iconAdd, bootstyle="secondary-outline", command=add_url)
add_url_btn.pack(side=LEFT, padx=10)
Hovertip(add_url_btn,'Paste the copied url.', hover_delay=1000)

status_label = tk.Label(header, text="", wraplength=300)
status_label.place(relx=0.5, rely=0.5, anchor="center")

def media_download_all():
    yt_data = dataRead()
    for item in yt_data:
        # print(item)
        media_download_sellect_check(item)

def media_all_sellect():
    yt_data = dataRead()
    for item in yt_data:
        media_type = media_download_sellect_data.get()
        item["type"] = media_type
    dataWrite(yt_data)
    for item in content.winfo_children():
        item.destroy()
    for item in yt_data:
        #* video kalite secme ekle
        contentBox(
            item["title"],
            item["preview_url"],
            item["url"],
            item["length"],
            item["author"],
            item["type"],
            )

iconDownload = icon_to_image("download", fill="#4267B2", scale_to_width=32)
media_download_btn = ttk.Button(header,image=iconDownload, bootstyle="secondary-outline", command=media_download_all)
media_download_btn.pack(side=RIGHT, padx=10)
Hovertip(media_download_btn,'Start download.', hover_delay=1000)

media_download_sellect_data = tk.BooleanVar()
media_download_sellect_btn = ttk.Checkbutton(header, text='Video / Sound', bootstyle="secondary-round-toggle", variable=media_download_sellect_data, command=media_all_sellect)
media_download_sellect_btn.pack(side=RIGHT)
Hovertip(media_download_sellect_btn,'Select media type.', hover_delay=1000)


media_leng = tk.Label(header, text="")
media_leng.place(relx=0.5, rely=0.7, anchor="center")

# * footer

# ? settings button
iconSettings = icon_to_image("cogs", fill="#797D7F", scale_to_width=22)
settings_btn = ttk.Button(footer,image=iconSettings, bootstyle="secondary-outline", command=open_settings_window)
settings_btn.pack(side=RIGHT, padx=5)
Hovertip(settings_btn,'From here, you can make the settings.', hover_delay=1000)

# ? update button
iconUpdate = icon_to_image("sync", fill="#797D7F", scale_to_width=18)
update_btn = ttk.Button(footer,image=iconUpdate, bootstyle="secondary-outline")
update_btn.pack(side=RIGHT, padx=5)
Hovertip(update_btn,'Check for update.', hover_delay=1000)
update_btn.config(state="disabled")

# ? about button
iconInfo = icon_to_image("info-circle", fill="#797D7F", scale_to_width=18)
about_btn = ttk.Button(footer,image=iconInfo, bootstyle="secondary-outline", command=open_about_window)
about_btn.pack(side=RIGHT, padx=5)
Hovertip(about_btn,'Software information.', hover_delay=1000)

# -----

def destroy_all():
    for item in content.winfo_children():
        import json
        # * Write
        with open('data.json', 'w') as file:
            json.dump([], file)
        media_leng.config(text= "Media : ( 0 )" )
        item.destroy()

def download_destroy_clear():

    yt_data = dataRead()
    for item in yt_data:
        if os.path.exists(download_dir + "/" + item["title"]):
            print("clear")
            #clear fuc add..
        # print(download_dir + "/" + item["title"])


# ? download ok clear button
iconClearOk = icon_to_image("trash-restore", fill="#797D7F", scale_to_width=16)
clear_ok_btn = ttk.Button(footer,image=iconClearOk, bootstyle="secondary-outline", command=download_destroy_clear)
clear_ok_btn.pack(side=LEFT, padx=5)
Hovertip(clear_ok_btn,'Clear downloads \nJust downloaded.', hover_delay=1000)
clear_ok_btn.config(state="disabled")

# ? clear all button
iconClear = icon_to_image("trash-alt", fill="#797D7F", scale_to_width=16)
clear_btn = ttk.Button(footer,image=iconClear, bootstyle="secondary-outline", command=destroy_all)
clear_btn.pack(side=LEFT, padx=5)
Hovertip(clear_btn,'Clean all.', hover_delay=1000)

# ? slow download mode button
iconClock = icon_to_image("clock", fill="#797D7F", scale_to_width=18)
slow_download_btn = ttk.Button(footer,image=iconClock, bootstyle="secondary-outline")
slow_download_btn.pack(side=LEFT, padx=5)
Hovertip(slow_download_btn,'Slow download.', hover_delay=1000)
slow_download_btn.config(state="disabled")

#-------------

import json
# * duplicate check
def check_duplicate(url, yt_data):
    for d in yt_data:
        if d['url'] == url:
            return True
    return False
# * JSON read
with open('data.json') as f:
    yt_data = json.load(f)


if len(yt_data) > 0:
    for item in yt_data:
        #* video kalite secme ekle
        contentBox(
            item["title"],
            item["preview_url"],
            item["url"],
            item["length"],
            item["author"],
            item["type"],
            )
    media_leng.config(text= "Media : ( " + str(len(yt_data)) + " )" )
else:
    # ? default content
    iconYoutube = icon_to_image(
        "searchengin", 
        fill="#4267B2", 
        scale_to_width=64
        )
    content_null_icon = ttk.Label(
        container,
        image=iconYoutube
        )
    content_null_icon.place(relx=0.5, rely=0.5, anchor="center")

    url_text = Label(
        container, 
        text="There is nothing here.",
        )
    url_text.place(relx=0.5, rely=0.6, anchor="center")



# * title icon

root.title("MedDown - Downloader")
root.iconbitmap("favicon.ico")

root.mainloop()
