from tkinter import messagebox
import tkinter as tk
def mybutton(window, text,color,command,width=10, fg='white',):
    button = tk.Button(window,
                       text=text,
                       activeforeground='white',
                       activebackground='black',
                       fg=fg,
                       bg=color,
                       command=command,
                       width=width,
                       font=('Lucida Sans', 15, 'bold','roman',)
                       )
    return button

def myimgLabel(window):
    label = tk.Label(window)
    label.grid(row=0,column=0)
    return label

def mytextLabel (window, text):
    label = tk.Label(window, text=text,bg='#757aa8')
    label.config(font=('sans-serif', 14), justify='left')
    return label

def myentry(window):
    inputtxt = tk.Text(window, height=2,width=15, font=('Arial',15))

    return inputtxt


def msg_box(title, description):
    messagebox.showinfo(title, description)



