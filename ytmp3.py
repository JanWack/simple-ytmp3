import yt_dlp
from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox
from tkinter import filedialog
import threading
import sys

"""
This is a simple porogram that converts YouTube videos to m4a.
It uses ytl-dlp as its backend. It was created to make it easier
for my friends (that doe sknow what a terminal is) to extraxt the
audio from YouTube vides (for personal use only!).

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

    root = Tk()
    root.title("Easy ytmp3")
    root.geometry('800x600')

    url_var = tkinter.StringVar()
    destination_path = tkinter.StringVar(value="")

    def exit_prog():
        root.destroy()
        sys.exit(0)

    menubar = Menu(root)

    help = Menu(menubar, tearoff=0)
    menubar.add_cascade(label ='Help', menu = help)
    def about_on_click():
        tkinter.messagebox.showinfo(
            title="About Easy ytmp3.",
            detail="Download songs from YouTube!\n\n" \
            "OBS! This program does not check for valid URL's. Use at your own risk." \
            "\n\nBased on yt-dlp.\nWritten by Johan Bodén (JanWack - Github)", icon='question')
    help.add_command(label ='About', command = about_on_click)

    root.config(menu=menubar)

    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=0)
    root.grid_rowconfigure(1, weight=0)
    root.grid_rowconfigure(2, weight=0)
    root.grid_rowconfigure(3, weight=1)
    root.grid_rowconfigure(4, weight=0)

    frame1 = Frame(root)
    frame1.grid(row=0, column=0, sticky='ew')
    frame1.grid_columnconfigure(0, weight=0)
    frame1.grid_columnconfigure(1, weight=1)
    frame2 = Frame(root)
    frame2.grid(row=1, column=0, sticky='ew')
    frame2.grid_columnconfigure(0, weight=0)
    frame2.grid_columnconfigure(1, weight=1)
    frame3 = Frame(root)
    frame3.grid(row=2, column=0, sticky='ew')
    frame3.grid_columnconfigure(0, weight=0)
    frame3.grid_columnconfigure(1, weight=1)
    frame3.grid_columnconfigure(2, weight=0)
    frame4 = Frame(root)
    frame4.grid(row=3, column=0, sticky='ew')
    frame4.grid_columnconfigure(0, weight=1)
    frame4.grid_columnconfigure(1, weight=0)
    frame5 = Frame(root)
    frame5.grid(row=4, column=0, sticky='ew')
    frame5.grid_columnconfigure(0, weight=0)
    frame5.grid_columnconfigure(1, weight=1)

    def browse_files():
        path = filedialog.askdirectory(initialdir=".", title="Select destination folder", mustexist=True)
        path_name.configure(text=path)
        destination_path.set(path)

    choose_file_location = Button(frame1, text="Path", command=browse_files)
    path_name = Label(frame1, text="")
    choose_file_location.grid(row=0, column=0, sticky='w',padx=10, pady=10)
    path_name.grid(row=0, column=1, sticky='w', padx=10, pady=10)

    def add_entry():
        str_url = url_var.get()
        input.delete(0, tkinter.END)
        if str_url.startswith("http"):
            URLs.append(str_url)
            url_list.insert(url_list.size(), str_url)

    add_item_text = Label(frame2, text="Add URL (video/playlist):")
    input = Entry(frame2, textvariable=url_var)
    add_button = Button(frame2, text="Add", command=add_entry)
    clear_button = Button(frame2, text="Clear", command= lambda: input.delete(0, tkinter.END))
    add_item_text.grid(row=1, column=0, sticky='w', pady=10, padx=10)
    input.grid(row=1, column=1, sticky='ew', padx=10, pady=10)
    add_button.grid(row=1, column=2, sticky='e', padx=0, pady=10)
    clear_button.grid(row=1, column=3, sticky='e', padx=10, pady=10)

    def begin_download():
        if not URLs:
            tkinter.messagebox.showinfo(title="No items", detail="There is nothing to download.", icon='info')
        elif destination_path.get() == "":
            tkinter.messagebox.showinfo(title="No destination path", detail="There is no destination path selected.", icon='warning')
        else:
            prog_label.grid(row=4, column=0, sticky='w', padx=10, pady=10)
            progress.grid(row=4, column=1, sticky='w', padx=10, pady=10)
            progress.start(4)
            thread1 = threading.Thread(target=download_items, args=(URLs, destination_path.get(), progress, prog_label))
            thread1.start()

    def clear_list():
        url_list.delete(0, url_list.size())
        URLs.clear()

    url_list = Listbox(frame4, bg="grey", selectmode='single', height=20)
    download = Button(frame3, text="Download listed items", command=begin_download)
    bindings = Label(frame3, text="Enter: add item\tBackspace: remove item")
    clear = Button(frame3, text="Clear list", command=clear_list)
    download.grid(row=2, column=0, sticky='w', padx=10, pady=10)
    bindings.grid(row=2, column=1, sticky='e', padx=10, pady=10)
    clear.grid(row=2, column=2, sticky="e", padx=10, pady=10)
    url_list.grid(row=3, column=0, sticky='nsew', padx=10, pady=10)

    scroll = Scrollbar(frame4, orient=tkinter.VERTICAL, command=url_list.yview)
    url_list['yscrollcommand'] = scroll.set
    scroll.grid(row=3, column=1, sticky='ns', padx=10, pady=10)

    prog_label = Label(frame5, text="Downloading:")
    progress = Progressbar(frame5, orient=HORIZONTAL, mode='indeterminate', length=400)


    def add_entry_button(event):
        add_entry()
    
    def remove_entry(event):
        selected_indx = url_list.curselection()
        if selected_indx:
            selected = url_list.selection_get()
            url_list.delete(selected_indx)
            URLs.remove(selected)

    input.bind("<Return>", add_entry_button)
    url_list.bind("<BackSpace>", remove_entry)
    root.protocol("WM_DELETE_WINDOW", exit_prog)
    root.mainloop()


def download_items(uris: list, path: str, prog: Progressbar, lab: Label):
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
        'format': 'm4a/bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }],
        'paths' : {
            'home' : path
        },
        'logger': MyLogger(),
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(uris)
    
    lab.grid_forget()
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