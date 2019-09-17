from tkinter import *
from tkinter import ttk

class Display(Canvas):
    '''
        This display class inherits from canvas and adds functionality
        to make points and shapes and respond to key events
    '''
    def remove_pts(self):
        while len(self.verts):
            self.verts.pop()
        while len(self.vert_ids):
            self.delete(self.vert_ids.pop())
            
    def make_point(self, e):
        '''
            Responds to left-click events
        '''
        self.verts += [[e.x, e.y]]
        size = 3
        self.vert_ids.append(self.create_oval(e.x-size,e.y-size,e.x+size,e.y+size,fill="black"))

    def make_shape(self, color):
        if len(self.vert_ids) > 2:
            s = Shape(self.verts.copy(), color, self)
            self.shapes[s.id] = s
            self.remove_pts()

    def select(self, e):
        '''
            Responds to right-click events
        '''
        added = False
        ovlap = list(self.find_overlapping(e.x-1,e.y-1,e.x+1,e.y+1))
        while len(ovlap):
            o = ovlap.pop()
            if self.type(o) == "polygon" or self.type(o) == "oval":
                if o not in self.selected:
                    if self.type(o) == "polygon":
                         self.selected[o] = self.shapes[o]
                    elif self.type(o) == "oval":
                        self.selected[o] = self.verts[self.vert_ids.index(o)]
                    self.itemconfig(o, width=2, outline="gold")
                else:
                    self.itemconfig(o, width=0, outline="")
                    self.selected.pop(o)
                added = True
        if added == False:
            for sel in self.selected:
                self.itemconfig(sel, width=0, outline="")
            self.selected.clear()
        print(self.selected)

    def move_selected(self, direc):
        '''
            Responds to arrow key events
        '''
        move_dir = [0,0]
        if direc == "Up":
            move_dir[1] = -2
        elif direc == "Down":
            move_dir[1] = 2
        elif direc == "Left":
            move_dir[0] = -2
        elif direc == "Right":
            move_dir[0] = 2
        for sel in self.selected:
            if self.type(sel) == "polygon":
                self.selected[sel].move(move_dir[0], move_dir[1])

    def get_keys(self, e):
        if e.char == 'r':
            self.make_shape("red")
        elif e.char == 'o':
            self.make_shape("orange")
        elif e.char == 'y':
            self.make_shape("yellow")
        elif e.char == 'g':
            self.make_shape("green")
        elif e.char == 'b':
            self.make_shape("blue")
        elif e.char == 'p':
            self.make_shape("purple")
        elif e.char == 'w':
            self.make_shape("white smoke")
        elif e.char == 'l':
            self.make_shape("lavender")
        elif e.char == 'm':
            self.make_shape("midnight blue")
        elif e.char == 's':
            self.make_shape("saddle brown")
        elif e.char == 'k':
            self.make_shape("pink")
        elif e.char == 'f':
            self.make_shape("firebrick")
        elif e.char == 'v':
            self.make_shape("VioletRed")
        elif e.char == 't':
            self.make_shape("thistle3")
        elif e.char == 'c':
            self.make_shape("cyan")
        elif e.char == 'e':
            self.make_shape("goldenrod2")
        elif e.char == 'u':
            self.make_shape("yellow green")
        elif e.char == 'i':
            self.make_shape("steel blue")
        elif e.char == 'a':
            self.make_shape("brown")
        elif e.char == 'd':
            self.make_shape("sandy brown")
        elif e.char == 'h':
            self.make_shape("HotPink2")
        elif e.char == 'j':
            self.make_shape("DarkOrange")
        elif e.char == 'n':
            self.make_shape("NavajoWhite4")
        elif e.char == 'q':
            self.make_shape("black")
    
    def __init__(self, wid, hgt):
        self.root = Tk()
        super().__init__(self.root, width=wid, height=hgt)
        super().pack()
        self.verts = []
        self.vert_ids = []
        self.shapes = {}
        self.selected = {}
        self.root.bind("<Button-1>", self.make_point)
        self.root.bind("<Button-3>", self.select)
        self.root.bind("<Key>", self.get_keys)
        self.root.bind("<Up>", lambda up: self.move_selected("Up"))
        self.root.bind("<Down>", lambda down: self.move_selected("Down"))
        self.root.bind("<Left>", lambda left: self.move_selected("Left"))
        self.root.bind("<Right>", lambda up: self.move_selected("Right"))
        self.root.mainloop()

class Shape:
    def __init__(self, points, color, display):
        self.points = points
        self.color = color
        self.display = display
        self.id = self.display.create_polygon(points, fill=color)
    def move(self, xAmt, yAmt):
        self.display.move(self.id, xAmt, yAmt)
        for point in self.points:
            point[0] += xAmt
            point[1] += yAmt
        
if __name__ == '__main__':
    d = Display(1000,800)
