"""Test language selector"""
import tkinter as tk
from tkinter import ttk
from src.components.language_selector import LanguageSelectorComponent
from src.utils.config import SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE

root = tk.Tk()
root.title("Test Language Selector")
root.geometry("600x300")

def on_change(code, name):
    print(f"Selected: {code} - {name}")

lang_selector = LanguageSelectorComponent(
    root,
    SUPPORTED_LANGUAGES,
    DEFAULT_LANGUAGE,
    on_language_change=on_change
)
lang_selector.frame.pack(fill=tk.X, padx=20, pady=20)

ttk.Label(root, text="Click the button to test the language selector").pack(pady=20)

root.mainloop()
