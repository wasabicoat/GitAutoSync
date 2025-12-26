#!/bin/bash
source venv/bin/activate
pyinstaller --noconfirm --onedir --windowed --add-data "/Users/chupawidthwadthanakul/.gemini/antigravity/scratch/GitAutoSync/venv/lib/python3.11/site-packages/customtkinter:customtkinter" --name "GitAutoSync" main.py
