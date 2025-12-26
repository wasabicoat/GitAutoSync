#!/bin/bash
source venv/bin/activate
ctk_path=$(python3 -c 'import customtkinter; print(customtkinter.__path__[0])')
pyinstaller --noconfirm --onedir --windowed --add-data "$ctk_path:customtkinter" --name "GitAutoSync" main.py
