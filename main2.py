from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import pygame
import socketio

global sio
sio = socketio.Client()
global name
name = ""

sio.connect("http://10.5.248.209:3000")

def start_connection(player_name):
    name = player_name
    sio.emit("newPlayer", name)


class Window():
    def __init__(self):
        self.root = Tk()
        pygame.mixer.init(44100)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_rowconfigure(6, weight=1)
        self.root.title("TSP Game")

        for i in range(1, 8, 2):
            Label(self.root, text=" ").grid(row=1, column=0)

        label_name = Label(self.root, text="Name: ")
        label_name.grid(row=0, column=0)
        self.name = Entry(self.root, insertofftime=0)
        self.name.grid(row=1, column=0)

        new_game_button = Button(self.root, text="PLAY", cursor="hand2",
                padx=57, command=lambda:start_connection(self.name.get()))
        new_game_button.grid(row = 2, column = 0)

        self.erase_button = Button(self.root, text="ERASE", cursor="hand2", padx=54)
        self.erase_button.grid(row=3, column=0)

        frame = Frame(self.root)
        frame.grid(row = 4, column = 0)

        self.undo_button = Button(frame, text="UNDO", cursor="hand2", padx=20)
        self.undo_button.pack(side=LEFT)

        self.redo_button = Button(frame, text="REDO", cursor="hand2", padx=20)
        self.redo_button.pack(side=RIGHT)

        frame_texts = Frame(self.root, height=35, padx=10, pady=10)
        frame_texts.grid(row=5, column=0)

        texts = Listbox(frame_texts, height=35, width=30)
        texts.pack()

        Label(self.root, text="    ").grid(row=8, column=0)

        self.canvas = Canvas(self.root, bg="white")
        self.canvas.grid(row=1, column=1, columnspan=3, rowspan=8,
                sticky="NSWE", padx=15, pady=15)

        img = ImageTk.PhotoImage(Image.open("title.png"))
        self.canvas.create_image(800, 440, anchor="center", image=img)

        check_button = Button(self.root, text="SUBMIT", cursor="hand2",
                height=2, width=5)
        check_button.grid(row=6, column=0)

        var = StringVar()
        var.set(0.00)

        self.root.update()
        self.root.minsize(self.root.winfo_width(), self.root.winfo_height())

        self.root.mainloop()

    def clear_canvas(self):
        self.canvas.delete("all")




global window
window = Window()


@sio.on("start")
def on_message(player1, player2, points):
    print(player1, player2)

    window.clear_canvas()


