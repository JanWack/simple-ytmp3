# 🎧 Simple-ytmp3: A Youtube to MP3 Program
A simple program that converts YouTube videos and playlists to m4a/mp3 files.

Based on [yt-dlp](https://github.com/yt-dlp/yt-dlp)!

## Preview of the program
![Alt text](./preview.png?raw=true "Optional Title")

## 📚 Features
- Converts videos and playlists
- Can convert multiple videos. Just add the URL's to the download list.
- High quality audio (if available)
- Simple UI
- Works on Windows and Linux (Ubuntu, but other distros will probably work fine as well)

## 📲 Prerequisites
Make sure you have installed:
1. python3
2. python3-venv (python3.12-venv)
3. puthon3-kt
4. ffmpeg

### Linux (Debian)
- The packages above can all be installed via apt

### Windows
- ffmpeg can be installed with winget
- Python can be insatlled in a bunch of ways (ex: installer, winget, MC-store)

## ⬇️ Installation
### 1. Clone the repositiry
```bash
git clone https://github.com/JanWack/simple-ytmp3.git
cd simple-ytmp3
```

### 2. Run the install.sh script to install dependencies
You may need to run chmod first.
```bash
chmod -x install.sh
./install.sh
```
You can use Git Bash if you are on Windows for example.

⚠️**OBS**: The install script will create an **executable** file of the program, but you can also just run the python script manually (see next step).

### 3. Run the program
1. You can run the created executable file (probably located in "./dist/ytmp3"),
2. Or you can run the python script with:
```bash
python3 ytmp3.py
```
❗️**NOTE**: The install.sh script creates a virtual environment and installs all dependencies there. To run the script manually you need to activate it:
```bash
source bin/activate
```
Or alternatively, install all dependencies outside of the virtual environemnt (see requirements.txt)

## 📝 Licence
MIT License. Improve it!

