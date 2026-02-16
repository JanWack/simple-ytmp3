#!/usr/bin/bash

echo ""
echo "Needed dependencies:"
echo ""
echo "  python/python3"
echo "  python3-venv"
echo "  python3-tk"
echo "  ffmpeg"
echo ""

read -p 'Continue[ENTER] or quit[q]: ' -s -n 1 key
if [[ $key = "" ]]; then
    echo 'running'
else
    exit 0
fi

# ffmpeg Check
if ! command -v ffmpeg &> /dev/null; then
    echo "ffmpeg not found."
    exit 1
fi

# Create venv
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "Python not found?"
    exit 1
fi
$PYTHON_CMD -m venv venv

# Activate depending on platform
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

echo " === Virtual environment created === "

# Pip Setup
pip install --upgrade pip

echo " === Installing dependencies === "

# Install project deps if present
if [[ -f requirements.txt ]]; then
    pip install -r requirements.txt
fi

echo " === Building Executable === "

pyinstaller --onefile ytmp3.py