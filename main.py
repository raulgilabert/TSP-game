from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import pygame
import socketio
import math
import time

global sio
sio = socketio.Client()

class Connection:
    def __init__ (self, name):
        self.name = name
        sio.connect('http://192.168.1.17:3000')

    def start(self):
        sio.emit("newPlayer", self.name)

    def submit(self, dist):
        sio.emit("ready", [self.name, dist])

    def next(self):
        sio.emit("next", self.name)

def play(name):
    global c
    c = Connection(name)
    c.start()

def obtain_center(coords):
    return ((coords[0][0] + coords[1][0])/ 2, (coords[0][1] + coords[1][1])/2)


class Window():
    def __init__(self):
        self.root = Tk()
        pygame.mixer.init(44100)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_rowconfigure(6, weight=1)
        self.root.title("TSP Game")
        self.coords_points = []
        self.centers = []
        self.clicked_points = []
        self.line_id_list = []
        self.points = []
        self.distance = 0.0
        self.first_point = None
        self.redo_list = []


        for i in range(1, 8, 2):
            Label(self.root, text=" ").grid(row=1, column=0)

        label_name = Label(self.root, text="Name: ")
        label_name.grid(row=0, column=0)
        self.name = Entry(self.root, insertofftime=0)
        self.name.grid(row=1, column=0)

        new_game_button = Button(self.root, text="PLAY", cursor="hand2",
                padx=57, command=lambda:play(self.name.get()))
        new_game_button.grid(row = 2, column = 0)

        self.erase_button = Button(self.root, text="ERASE", cursor="hand2", padx=54, command=self.erase)
        self.erase_button.grid(row=3, column=0)

        frame = Frame(self.root)
        frame.grid(row = 4, column = 0)

        self.undo_button = Button(frame, text="UNDO", cursor="hand2", padx=20, command=self.undo)
        self.undo_button.pack(side=LEFT)

        self.redo_button = Button(frame, text="REDO", cursor="hand2", padx=20, command=self.redo)
        self.redo_button.pack(side=RIGHT)

        frame_texts = Frame(self.root, height=35, padx=10, pady=10)
        frame_texts.grid(row=5, column=0)

        self.texts = Listbox(frame_texts, height=35, width=30)
        self.texts.pack()

        Label(self.root, text="    ").grid(row=8, column=0)

        self.canvas = Canvas(self.root, bg="white")
        self.canvas.grid(row=1, column=1, columnspan=3, rowspan=8, sticky="NSWE", padx=15, pady=15)
        self.canvas.bind("<Button-1>", self.link_points)

        #img = ImageTk.PhotoImage(Image.open("title.png"))
        #self.canvas.create_image(800, 440, anchor="center", image=img)

        self.canvas.create_text(800, 440, text="THE GAME")

        check_button = Button(self.root, text="SUBMIT", cursor="hand2",height=2, width=5, command=lambda:c.submit(self.distance))
        check_button.grid(row=6, column=0)

        var = StringVar()
        var.set(0.00)

        self.root.update()
        self.root.minsize(self.root.winfo_width(), self.root.winfo_height())

    def obtain_center_index(self, index):
        return obtain_center(self.coords_points[index])

    def create_line(self, center1, center2):
        actual_id = self.canvas.create_line(center1[0], center1[1], center2[0], center2[1])
        self.canvas.tag_lower(actual_id)
        self.line_id_list.append(actual_id)

    def start(self):
        self.root.mainloop()

    def clear_canvas(self):
        self.canvas.delete("all")

    def render_points(self, points):
        self.points = points

        for point in points:
            x = point[0]*(self.canvas.winfo_width() - 70) + 35
            y = point[1]*(self.canvas.winfo_height() - 70) + 35
            coords = ((x, y), (x + 11*2, y + 11*2))
            self.canvas.create_oval(coords, width = 0, fill = "black", activefill="grey")
            self.coords_points.append(coords)

        for i in self.coords_points:
            self.centers.append(obtain_center(i))

        for point in self.points:
            point[0] = int(point[0]*1000)
            point[1] = int(point[1]*1000)

    def link_points(self, event):
        point_index = -1

        for i,c in enumerate(self.coords_points):
            if event.x>c[0][0] and event.x<c[1][0] and event.y>c[0][1] and event.y<c[1][1]:
                point_index = i
                break
        if point_index == -1:
            return

        actual_point = self.coords_points[point_index]

        self.redo_list.clear()
        self.first_point = None

        if not self.clicked_points:
            self.canvas.create_oval(actual_point[0][0], actual_point[0][1], actual_point[1][0],
                                    actual_point[1][1], width=3, outline="lime", tag="border")
        else:
            if point_index == self.clicked_points[0] and len(self.clicked_points) < len(self.coords_points):
                return
            if point_index in self.clicked_points and self.clicked_points[0] != point_index:
                return
            if point_index == self.clicked_points[-1]:
                return

            last_center = self.obtain_center_index(self.clicked_points[-1])
            actual_center = obtain_center(actual_point)

            self.create_line(actual_center, last_center)
        self.clicked_points.append(point_index)

        print(self.clicked_points)

        if (len(self.clicked_points) > len(self.points)):
            last_point = self.points[self.clicked_points[0]]

            distance = 0

            print("----------------------------------")
            print(self.points)
            print(self.clicked_points)


            for i in self.clicked_points:
                print(last_point, self.clicked_points[i])
                distance += math.sqrt((last_point[0] - self.points[self.clicked_points[i]][0])**2 + (last_point[1] - self.points[self.clicked_points[i]][1])**2)
                print(last_point, self.points[self.clicked_points[i]])
                print(distance)

                last_point = self.points[self.clicked_points[i]]
            self.distance = distance
    def erase(self):
        self.first_point = None
        self.redo_list.clear()

        if self.line_id_list:
            for i in self.line_id_list:
                self.canvas.delete(i)
            self.clicked_points.clear()
            self.line_id_list.clear()
        self.canvas.delete("border")
        self.clicked_points.clear()

    def redo(self):
        if self.first_point is not None:
            self.clicked_points.append(self.first_point)
            point1 = self.coords_points[self.first_point]
            self.canvas.create_oval(point1[0][0], point1[0][1], point1[1][0], point1[1][1], width=3,
                                    outline="lime", tag="border")
            self.first_point = None
        elif self.redo_list:
            last_position = self.redo_list.pop()

            center1 = self.obtain_center_index(last_position[0])
            center2 = self.obtain_center_index(last_position[1])

            self.clicked_points.append(last_position[0])
            self.create_line(center1, center2)
    def undo(self):
            if self.line_id_list:
                last_point = self.coords_points[self.clicked_points[-1]]
                last2_point = self.coords_points[self.clicked_points[-2]]

                last_center = obtain_center(last_point)
                last2_center = obtain_center(last2_point)
                self.redo_list.append((self.clicked_points[-1], self.clicked_points[-2]))
                self.canvas.delete(self.line_id_list.pop())
                self.clicked_points.pop()
            elif len(self.clicked_points) == 1:
                self.first_point = self.clicked_points.pop()
                self.canvas.delete("border")

    def info_winners(self, winner):
        self.coords_points = []
        self.centers = []
        self.clicked_points = []
        self.line_id_list = []
        self.points = []
        self.distance = 0.0
        self.first_point = None
        self.redo_list = []
        self.distance = 0

        self.clear_canvas()

        if winner == self.name.get():
            self.texts.insert(END, "YOU WIN")

            time.sleep(2)
            c.next()
        else:
            self.texts.insert(END, "YOU LOSE")

global window

window = Window()

@sio.on("start")
def on_message(player1, player2, points):
    window.clear_canvas()
    window.render_points(points)

@sio.on("winner")
def on_message(winner):
    window.info_winners(winner)


window.start()
