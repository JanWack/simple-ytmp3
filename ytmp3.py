import yt_dlp
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox
from tkinter import filedialog
import threading
import sys

"""
https://www.youtube.com/watch?v=0Yxl-lHsEq8
"""

"""
This is a simple porogram that converts YouTube videos to m4a.
It uses ytl-dlp as its backend. It was originally created to make
it easier for my friends (that doe sknow what a terminal is) to
extraxt the audio from YouTube vides (for personal use only!).

Written by: Johan Bodén, JanWack (GitHub).

Licence: MIT.
"""

# Global list of URL's
URLs = []

# ============= Classes ============= #
class MyLogger:
    """
    Based on the example from yt-dlp's GitHub. For logging errors and warnings.
    """
    def __init__(self): self.log_file = open("log.txt", "w")

    def debug(self, msg):
        if msg.startswith('Warning'): self.warning(msg)
        elif msg.startswith('Error'): self.error(msg)

    def warning(self, msg): print(msg ,file=self.log_file)
    def error(self, msg): print(msg ,file=self.log_file)


class MyPostProcessor(yt_dlp.postprocessor.PostProcessor):
    """
    Based on the example from yt-dlp pypi
    """
    def run(self, info):
        return [], info


class CustomListItem(tk.Frame):
    """
    Custom Frame widget
    """
    def __init__(self, root: tk.Frame, url: str):
        super().__init__(master=root)
        self.info = extract_info(url)
        self.configure(padx=10, pady=10)
        lab = ttk.Label(self, text=self.info['title'] + ' [' + self.info['duration'] + ']')
        remove = ttk.Button(self, text="x", width=2, command=lambda: remove_entry(self, self.info['url']))
        remove.grid(row=0, column=0, sticky='e')
        lab.grid(row=0, column=1, sticky='e', padx=10)
     

# ============= Functions ============= #

def my_hook(d):
    """
    Based on the example from yt-dlp pypi
    """
    if d['status'] == 'finished':
        print('Done downloading, now post-processing ...')


def add_entry(input: ttk.Entry, url: str, list: tk.Frame):
    input.delete(0, tk.END)
    # Check if the input starts with YouTube's address
    if url.startswith("https://www.youtube.com"):
        URLs.append(url)

        info_obj = CustomListItem(list, url)
        info_obj.pack()



def remove_entry(item: CustomListItem, url_to_remove: str):
    try:
        URLs.remove(url_to_remove)
    except ValueError:
        tkinter.messagebox.showwarning(title="ValueError", detail="Could not remove item.", icon='error')
    item.destroy()


def browse_files(path: tk.StringVar) -> bool:
    dest = filedialog.askdirectory(initialdir=".", title="Select destination folder", mustexist=True)
    if path:
        path.set(dest)
        return True
    else: return False


def clear_list():
        URLs.clear()


def begin_download(path: tk.StringVar, prog_label: ttk.Label, progress: ttk.Progressbar, audio_fomrat: tk.StringVar, stop: ttk.Button):
    """
    Starts the download process in a separate thread.
    """
    if not URLs: tkinter.messagebox.showinfo(title="No items", detail="There is nothing to download.", icon='info')
    else:
        if browse_files(path):
            # Show progress bar and stop button
            prog_label.configure(text="Downloading, please wait.")
            progress.grid(row=0, column=1, sticky='ew')
            stop.grid(row=0, column=2, sticky='e', padx=10)

            progress.start(4)
            thread1 = threading.Thread(target=download_items, args=(URLs, path.get(), progress, prog_label, audio_fomrat.get(), stop))
            thread1.start()
        else: return


def download_items(uris: list, path: str, prog: ttk.Progressbar, lab: tk.Label, audio_format: str, stop: ttk.Button):
    """
    Based on the example from yt-dlp's GitHub.
    """
    ydl_opts = {
        'format': audio_format + '/bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': audio_format,
        }],
        'paths' : { 'home' : path },
        'logger': MyLogger(),
        'quiet': True,
        'progress_hooks': [my_hook]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.add_post_processor(MyPostProcessor(), when='pre_process')
        error_code = ydl.download(uris)
    
    prog.stop()
    prog.grid_forget()
    lab.configure(text="No jobs.")
    stop.grid_forget()

    if error_code == 0: tkinter.messagebox.showinfo(title="", message="Download complete.", icon='info')
    else:
        tkinter.messagebox.showinfo(
            title="Error",
            message="Something went wrong.",
            icon='error',
            detail="Things may not work as expected.\nCheck the log file! Error code: " + str(error_code)
        )


def extract_info(url: str) -> dict[str, str]:
    """
    Extracts information from the video's url.
    """
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        info_dict = ydl.sanitize_info(info)
        return {
            'url': url,
            'img': info_dict['thumbnail'],
            'title': info_dict['fulltitle'],
            'duration': info_dict['duration_string']
        }


def stop_download():
     print("Stopping")


def exit_prog(root: tk.Tk):
    root.destroy()
    sys.exit(0)


# ============= Main function ============= #

def app():
    """
    The main function. Initializes the window
    and handles inputs and button presses.
    """

    # Create main window
    root = tk.Tk()

    root.title      ("Simple ytmp3")
    root.geometry   ('600x400')
    root.resizable  (0, 0)

    # Configure the main window
    root.columnconfigure(0, weight=1)
    root.rowconfigure   (1, weight=1)

    # Create frames
    frame0 = tk.Frame(root)
    frame1 = tk.Frame(root)
    frame2 = tk.Frame(root)
    frame3 = tk.Frame(root)
    
    # Configure The frames
    frame0.columnconfigure  (1, weight=1)
    frame0.grid             (row=0, column=0, sticky='ew')
    frame1.columnconfigure  (0, weight=1)
    frame1.rowconfigure     (0, weight=0)
    frame1.rowconfigure     (1, weight=1)
    frame1.rowconfigure     (2, weight=0)
    frame1.grid             (row=1, column=0, sticky='ewns')
    frame2.columnconfigure  (3, weight=1)
    frame2.grid             (row=2, column=0, sticky='ew')
    frame3.columnconfigure  (1, weight=1)
    frame3.grid             (row=3, column=0, sticky='ew')

    # Variables
    url_var             = tk.StringVar(root)
    destination_path    = tk.StringVar(root)
    audio_format        = tk.StringVar(root) # Default is m4a

    # Widgets
    item_list           = tk.Canvas         (frame1)
    scrollable_frame    = tk.Frame          (item_list)
    scroll              = ttk.Scrollbar     (frame1, orient=tk.VERTICAL, command=item_list.yview)
    add_item_text       = ttk.Label         (frame0, text="Video or playlist URL:")
    input               = ttk.Entry         (frame0, textvariable=url_var)
    add_button          = ttk.Button        (frame0, text="+", command=lambda: add_entry(input, url_var.get(), scrollable_frame), width=2)
    clear_button        = ttk.Button        (frame0, text="x", command= lambda: input.delete(0, tk.END), width=2)
    download            = ttk.Button        (frame2, text="Download", command=lambda: begin_download(destination_path, prog_label, progress, audio_format, stop_download))
    mp3_button          = ttk.Radiobutton   (frame2, text="mp3", variable=audio_format, value="mp3")
    m4a_button          = ttk.Radiobutton   (frame2, text="m4a", variable=audio_format, value="m4a")
    clear               = ttk.Button        (frame2, text="Clear list", command=lambda: clear_list(item_list))
    prog_label          = ttk.Label         (frame3, text="No jobs.")
    progress            = ttk.Progressbar   (frame3, orient=tk.HORIZONTAL, mode='indeterminate')
    stop_download       = ttk.Button        (frame3, text="Stop", command=lambda: stop_download())
    sep1                = ttk.Separator     (frame1, orient=tk.HORIZONTAL)
    sep2                = ttk.Separator     (frame1, orient=tk.HORIZONTAL)
    
    # Widget placements
    add_item_text.grid      (row=0, column=0, sticky='w', pady=10, padx=10)
    input.grid              (row=0, column=1, sticky='ew', padx=10, pady=10)
    add_button.grid         (row=0, column=2, sticky='e', padx=0, pady=10)
    clear_button.grid       (row=0, column=3, sticky='e', padx=10, pady=10)
    scroll.grid             (row=1, column=1, sticky='nse', padx=10)
    item_list.grid          (row=1, column=0, sticky='nsew', padx=10)
    download.grid           (row=0, column=0, sticky='w', padx=10, pady=10)
    m4a_button.grid         (row=0, column=1, sticky='w')
    mp3_button.grid         (row=0, column=2, sticky='w', padx=10)
    clear.grid              (row=0, column=4, sticky="e", padx=10, pady=10)
    prog_label.grid         (row=0, column=0, sticky='w', padx=10, pady=10)
    sep1.grid               (row=0, column=0, sticky='ew', padx=10)
    sep2.grid               (row=2, column=0, sticky='ew', padx=10)

    # Set default audio format
    audio_format.set("m4a")

    # Set scroll for the listbox
    item_list.configure(yscrollcommand=scroll.set)
    item_list.create_window((0, 0), window=scrollable_frame, anchor='nw')
    scrollable_frame.bind("<Configure>", lambda e: item_list.configure(scrollregion=item_list.bbox("all")))

    # Callbacks
    def add_entry_button(event): add_entry(input, url_var.get(), scrollable_frame)
    def remove_entry_button(event): remove_entry(item_list)
    def exit_request(): exit_prog(root)

    # Keybindings
    input.bind("<Return>", add_entry_button)
    item_list.bind("<BackSpace>", remove_entry_button)

    # Handle exit
    root.protocol("WM_DELETE_WINDOW", exit_request)

    root.mainloop()


# ============= Entry point ============= #

if __name__=="__main__":
    app()