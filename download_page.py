import subprocess
from tkinter import Listbox, Toplevel, Label, END, messagebox, filedialog
from customtkinter import CTkButton, CTkEntry
from api import search


# Function to download audio from YouTube using yt-dlp
def download_audio(url, path):
    print(f"Starting download for {url}...")
    subprocess.run([
        'yt-dlp',
        '-f', 'bestaudio',
        '-o', f'{path}/%(title)s.%(ext)s',
        '--extract-audio',
        '--audio-format', 'mp3',
        '--add-metadata',
        url
    ])


# Decorator function to print start and end of download
def download_decorator(func):
    def wrapper(*args, **kwargs):
        print("Starting download...")
        result = func(*args, **kwargs)
        print("Download finished!")
        return result

    return wrapper


# Function to download a song
@download_decorator
def download_song(root):
    # Initialize variables and GUI elements
    results = []
    listbox = Listbox()

    # Function to handle song selection from listbox
    def on_song_select(event):
        print("Song selected...")
        nonlocal results
        widget = event.widget
        selection = widget.curselection()
        video_id = results[selection[0]]['videoId']
        print(f"Selected video ID: {video_id}")
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        print(f"Video URL: {video_url}")
        download_path = filedialog.askdirectory(
            initialdir=get_last_used_directory())
        set_last_used_directory(download_path)
        print(f"Download path: {download_path}")
        download_audio(video_url, download_path)
        download_window.destroy()
        messagebox.showinfo("Download Complete", "The song has been downloaded successfully!")

    # Function to submit search query and display results
    def submit(event=None):
        nonlocal results
        nonlocal listbox
        query = entry.get()
        results = search(query)
        listbox.delete(0, END)
        for result in results[:5]:
            listbox.insert(END, result['title'])

    # Creating GUI for downloading a song
    download_window = Toplevel(root)
    download_window.geometry("500x500")
    Label(download_window, text="Enter a song title: ").pack()
    entry = CTkEntry(download_window, width=200, height=25)
    entry.place(x=0, y=0)
    entry.pack()
    entry.bind('<Return>', submit)
    listbox = Listbox(download_window, width=60)
    listbox.pack()
    listbox.bind('<<ListboxSelect>>', on_song_select)
    CTkButton(download_window, text="Submit", command=submit).pack()


# Function to get the last used directory
def get_last_used_directory():
    try:
        with open('last_used_directory.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None


# Function to set the last used directory
def set_last_used_directory(directory):
    with open('last_used_directory.txt', 'w') as file:
        file.write(directory)
