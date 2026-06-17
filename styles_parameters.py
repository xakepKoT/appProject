from tkinter import *
from tkinter import ttk


def styleF():
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Default.TButton", font=('Arial', 10), foreground='gray', borderwidth=0)
        style.map(
            "Default.TButton",
            background=[
                ('!disabled', 'light gray'),
                ('active', '#e0e0e0'),
                ('pressed', '#c0c0c0')],
            foreground=[
                ('!disabled', 'gray'),
                ('active', 'blue')],

        )
        style.configure('Active.Default.TButton', foreground='black',borderwidth=2)
        style.map(
            "Active.Default.TButton",
            background=[
                ('!disabled', 'light gray'),
                ('active', '#e0e0e0'),
                ('pressed', '#c0c0c0')],
            foreground=[
                ('!disabled', 'black'),
                ('active', 'blue')],
        )
        style.configure(
            "Upper.TFrame",
            background='light gray'
        )
        style.configure(
            "side_interface.TFrame",
            background='#EDEDED'
        )