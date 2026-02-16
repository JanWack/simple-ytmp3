import yt_dlp
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox
from tkinter import filedialog
import threading
import sys

"""
This is a simple porogram that converts YouTube videos to m4a.
It uses ytl-dlp as its backend. It was originally created to make
it easier for my friends (that doe sknow what a terminal is) to
extraxt the audio from YouTube vides (for personal use only!).

Written by: Johan Bodén, JanWack (GitHub)

Licence: MIT
"""

class MyLogger:
    """
    Based on the example from yt-dlp
    """
    def __init__(self):
        self.log_file = open("log.txt", "w")

    def debug(self, msg):
        if msg.startswith('Warning'):
            self.warning(msg)
        elif msg.startswith('Error'):
            self.error(msg)

    def warning(self, msg):
        print(msg ,file=self.log_file)

    def error(self, msg):
        print(msg ,file=self.log_file)


def app():
    """
    The main function. Not really good code-quality by having
    everything in one file hehe.
    """
    URLs = []

    root = tk.Tk()
    root.title("Easy ytmp3")
    root.geometry('600x400')
    root.resizable(0, 0)

    url_var = tk.StringVar(root)
    destination_path = tk.StringVar(root)
    audio_format = tk.StringVar(root, "m4a") # Default is m4a

    def exit_prog():
        root.destroy()
        sys.exit(0)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=0)
    root.rowconfigure(1, weight=1)
    root.rowconfigure(2, weight=0)
    root.rowconfigure(3, weight=0)

    frame0 = tk.Frame(root)
    frame0.columnconfigure(0, weight=0)
    frame0.columnconfigure(1, weight=1)
    frame0.grid(row=0, column=0, sticky='ew')

    frame1 = tk.Frame(root)
    frame1.columnconfigure(0, weight=1)
    frame1.columnconfigure(1, weight=0)
    frame1.rowconfigure(0, weight=1)
    frame1.grid(row=1, column=0, sticky='ewns')

    frame2 = tk.Frame(root)
    frame2.columnconfigure(0, weight=0)
    frame2.columnconfigure(1, weight=0)
    frame2.columnconfigure(2, weight=0)
    frame2.columnconfigure(3, weight=1)
    frame2.columnconfigure(4, weight=0)
    frame2.grid(row=2, column=0, sticky='ew')

    frame3 = tk.Frame(root)
    frame3.columnconfigure(0, weight=0)
    frame3.columnconfigure(1, weight=1)
    frame3.grid(row=3, column=0, sticky='ew')

    def browse_files() -> bool:
        path = filedialog.askdirectory(initialdir=".", title="Select destination folder", mustexist=True)
        if path:
            destination_path.set(path)
            return True
        else:
            return False

    def add_entry():
        str_url = url_var.get()
        input.delete(0, tkinter.END)
        if str_url.startswith("http"):
            URLs.append(str_url)
            url_list.insert(url_list.size(), str_url)

    add_item_text = ttk.Label(frame0, text="Add URL (video or playlist):")
    input = ttk.Entry(frame0, textvariable=url_var)
    add_button = ttk.Button(frame0, text="+", command=add_entry, width=2)
    clear_button = ttk.Button(frame0, text="x", command= lambda: input.delete(0, tkinter.END), width=2)
    add_item_text.grid(row=0, column=0, sticky='w', pady=10, padx=10)
    input.grid(row=0, column=1, sticky='ew', padx=10, pady=10)
    add_button.grid(row=0, column=2, sticky='e', padx=0, pady=10)
    clear_button.grid(row=0, column=3, sticky='e', padx=10, pady=10)

    def begin_download():
        if not URLs:
            tkinter.messagebox.showinfo(title="No items", detail="There is nothing to download.", icon='info')
        else:
            if browse_files():
                prog_label.configure(text="Downloading, please wait.")
                progress.grid(row=0, column=1, sticky='ew')
                progress.start(4)
                thread1 = threading.Thread(target=download_items, args=(URLs, destination_path.get(), progress, prog_label, audio_format.get()))
                thread1.start()
            else:
                return

    def clear_list():
        url_list.delete(0, url_list.size())
        URLs.clear()

    def remove_entry():
        selected_indx = url_list.curselection()
        if selected_indx:
            selected = url_list.selection_get()
            url_list.delete(selected_indx)
            URLs.remove(selected)

    url_list = tk.Listbox(frame1, bg="grey", selectmode='single')
    scroll = ttk.Scrollbar(frame1, orient=tkinter.VERTICAL, command=url_list.yview)
    url_list['yscrollcommand'] = scroll.set
    scroll.grid(row=0, column=1, sticky='nse', padx=10)
    url_list.grid(row=0, column=0, sticky='nsew', padx=10)

    download = ttk.Button(frame2, text="Download", command=begin_download)
    mp3_button = ttk.Radiobutton(frame2, text="mp3", variable=audio_format, value="mp3")
    m4a_button = ttk.Radiobutton(frame2, text="m4a", variable=audio_format, value="m4a")

    audio_format.set("m4a")

    remove_entry_button = ttk.Button(frame2, text="Remove item", command=remove_entry)
    clear = ttk.Button(frame2, text="Clear list", command=clear_list)
    download.grid(row=0, column=0, sticky='w', padx=10, pady=10)
    m4a_button.grid(row=0, column=1, sticky='w')
    mp3_button.grid(row=0, column=2, sticky='w', padx=10)
    remove_entry_button.grid(row=0, column=3, sticky='e')
    clear.grid(row=0, column=4, sticky="e", padx=10, pady=10)


    prog_label = ttk.Label(frame3, text="No jobs")
    progress = ttk.Progressbar(frame3, orient=tk.HORIZONTAL, mode='indeterminate')
    prog_label.grid(row=0, column=0, sticky='w', padx=10, pady=5)


    def add_entry_button(event):
        add_entry()
    
    def remove_entry_button(event):
        remove_entry()

    input.bind("<Return>", add_entry_button)
    url_list.bind("<BackSpace>", remove_entry_button)
    root.protocol("WM_DELETE_WINDOW", exit_prog)
    root.mainloop()


def download_items(uris: list, path: str, prog: ttk.Progressbar, lab: tk.Label, audio_format: str):
    """
    Based on the exmaple from yt-dlp
    
    :param uris: A list of URL's
    :type uris: [str]
    :param path: Save destination
    :type path: str
    :param prog: A reference to the progress bar
    :type prog: Progressbar
    :param lab: A reference to the progress bar label
    :type lab: Label
    """
    ydl_opts = {
        'format': audio_format + '/bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': audio_format,
        }],
        'paths' : {
            'home' : path
        },
        'logger': MyLogger(),
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(uris)
    
    lab.configure(text="No jobs")
    prog.stop()
    prog.grid_forget()

    if error_code == 0:
        tkinter.messagebox.showinfo(title="", message="Download complete.", icon='info')
    else:
        tkinter.messagebox.showinfo(
            title="Error",
            message="Something went wrong.",
            icon='error',
            detail="Things may not work as expected.\nCheck the log file! Error code: " + str(error_code))


if __name__=="__main__":
    app()