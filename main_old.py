from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import pygame
import socketio

global sio
sio = socketio.Client()

class Connection:
    def __init__ (self, nom):
        self.nom = nom
        sio.connect('http://10.5.248.209:3000')

    def start(self):
        sio.emit("newPlayer", self.nom)

global c
global root

def play(nombre):
    c = Connection(nombre)
    c.start()

@sio.on("start")
def on_message(player1, player2, points):
    print(player1, player2)

def main():
    root=Tk()
    pygame.mixer.init(44100)

    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_rowconfigure(4, weight=1)
    root.grid_rowconfigure(6, weight=1)
    root.title("TSP Game") #títol de la interfície

    #separadors de files:
    for i in range(1,8,2):
            Label(root, text=" ").grid(row=i, column=0)

    LabelName = Label(root, text="Name: ")
    LabelName.grid(row=0, column=0)
    name = Entry(root, insertofftime=0)
    name.grid(row=1,column=0)


    #creació botó nou joc
    boto_jocnou=Button(root,text="PLAY", cursor="hand2", padx=57, command=lambda:play(name.get()))
    boto_jocnou.grid(row=2,column=0)


    #creació botó esborrar
    boto_borrar=Button(root,text="ERASE", cursor="hand2", padx=54)
    boto_borrar.grid(row=3, column=0)

    #creació frame per els botons fer i desfer
    frame_desfer_refer = Frame(root)
    frame_desfer_refer.grid(row=4,column=0)


    #creació botó desfer
    boto_desfer=Button(frame_desfer_refer, text="UNDO", cursor="hand2", padx=20)
    boto_desfer.pack(side=LEFT)

    #creació botó refer
    boto_refer=Button(frame_desfer_refer, text="REDO", cursor="hand2", padx=20)
    boto_refer.pack(side=RIGHT)


    #TEXTOS - creació del frame i de la llista de solucions
    frm_textos = Frame(root, height=25, padx=10, pady=10)
    frm_textos.grid(row=5, column=0)
    textos=Listbox(frm_textos, height=35, width=30)
    textos.pack()

    Label(root, text="    ").grid(row=8, column=0) #espai de text buit, separador
    canvas=Canvas(root, bg="white")
    canvas.grid(row=1, column=1, columnspan=3, rowspan=8, sticky="NSWE", padx=15, pady=15)

    def clear():
        canvas.delete("all")

    img= ImageTk.PhotoImage(Image.open("title.png"))
    canvas.create_image(800,440,anchor="center",image=img)

    #pissarra.bind("<Button-1>", unio_punts) #se li associa (com a paràmetre) a la pissarra el clic esquerre del ratolí

    #creació botó comprovar
    boto_comprovar=Button(root, text="SUBMIT", cursor="hand2", height = 2, width = 5)
    boto_comprovar.grid(row=6, column=0)


    #creació variable que determinarà la distància (predefinida a 0)
    var = StringVar()
    var.set(0.00)

    #configuracions per poder controlar la mínima minimització de la interfície
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())

    root.mainloop()#bucle de l'arrel de la interfície


main() #invocació a la funció principal 












