@echo off
cd /d "%~dp0"
pip install pronotepy opencv-python-headless -q
pythonw main.py
