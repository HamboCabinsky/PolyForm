from tkinter import filedialog
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageDraw, ImageTk

colorTranslator = {
                    "red" : (255, 0, 0),
                    "orange" : (255, 165, 0),
                    "yellow" : (255, 255, 0),
                    "green" : (0, 255, 0),
                    "blue" : (0, 0, 255),
                    "purple" : (160, 32, 240),
                    "white smoke" : (245, 245, 245),
                    "lavender" : (230, 230, 250),
                    "midnight blue" : (25, 25, 112),
                    "saddle brown" : (139, 69, 19),
                    "pink" : (255, 192, 203),
                    "firebrick" : (178, 34, 34),
                    "VioletRed" : (208, 32, 144),
                    "thistle3" : (205, 181, 205),
                    "cyan" : (0, 255, 255),
                    "goldenrod2" : (238, 180, 34),
                    "yellow green" : (154, 205, 50),
                    "steel blue" : (70, 130, 180),
                    "brown" : (165, 42, 42),
                    "sandy brown" : (244, 164, 96),
                    "HotPink2" : (238, 106, 167),
                    "DarkOrange" : (255, 140, 0),
                    "NavajoWhite4" : (139, 121, 94),
                    "black" : (0, 0, 0)
                    }

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

    def addbgImage(self):
        filenm = filedialog.askopenfilename(filetypes=(("All","*.*"),("png","*.png"),("gif",".gif"),("jpg",".jpg")))
        if filenm:
            self.img = ImageTk.PhotoImage(file=filenm)
            self.bgImage = self.create_image(0,0,image=self.img,anchor=NW)
            self.lower(self.bgImage)

    def export_image(self):
        filenm = filedialog.asksaveasfilename(initialdir = "/", title = "select file", filetypes = (("png","*.png"),("add files","*.*")))
        img = Image.new("RGBA", (self.width, self.height), color = (0,0,0,0))
        d = ImageDraw.Draw(img)
        for s in self.shapes:
            tupled = []
            for pt in self.shapes[s].points:
                tupled += [tuple(pt)]
            d.polygon(tupled, fill=colorTranslator[self.shapes[s].color])
        img.save(filenm+".png",format='png')
            
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
        self.img = None
        self.bgImage = None
        self.width = wid
        self.height = hgt
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
        menu_bar = Menu(self.root)
        image_menu = Menu(menu_bar)
        menu_bar.add_cascade(label="Image", menu=image_menu)
        image_menu.add_command(label="Background Image", command=self.addbgImage)
        image_menu.add_command(label="Export", command=self.export_image)
        self.root.config(menu=menu_bar)
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
