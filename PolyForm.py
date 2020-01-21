from tkinter import filedialog
from tkinter import *
from tkinter import ttk
from math import *
from PIL import Image, ImageDraw, ImageTk
from tkinter.filedialog import askopenfilename

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

class PFDisplay(Canvas):
    def remove_pts(self):
        while len(self.verts):
            self.verts.pop()
        while len(self.vert_ids):
            self.delete(self.vert_ids.pop())
    def shift_vert_col(self):
        if self.col_ind < len(self.colors)-1:
            self.col_ind += 1
        else:
            self.col_ind = 0
        self.vert_color = self.colors[self.col_ind]
    
    def make_point(self, e):
        '''
            Responds to left-click events.
            Adds the x and y coords of the left click event to the verts array then, creates
            a small oval in that location on canvas and adds its id to vert_ids array.
        '''
        self.verts += [[e.x, e.y]]
        size = 3
        self.vert_ids.append(self.create_oval(e.x-size,e.y-size,e.x+size,e.y+size,fill=self.vert_color))

    def make_shape(self, color):
        if len(self.vert_ids) > 2:
            s = Shape(self.verts.copy(), color, self)
            self.shapes[str(s.id)] = s
            self.remove_pts()

    def select(self, e):
        '''
            Responds to right-click events.
            Finds all canvas objects that overlap the location of the right-click event. Then, highlights them with
            a yellow outline and stores their id in PFDisplay's selected array. If an object is already selected and
            right-clicked again, it is deselected and removed from the array. If there are no overlapping objects
            on the canvas, all currently selected objects are deselected.
        '''
        added = False
        ovlap = list(self.find_overlapping(e.x-1, e.y-1, e.x+1, e.y+1))
        while len(ovlap):
            o = ovlap.pop()
            if self.type(o) == "polygon" or self.type(o) == "oval":
                if str(o) not in self.selected:
                    if self.type(o) == "polygon":
                        self.selected[str(o)] = self.shapes[str(o)]
                    if self.type(o) == "oval":
                        self.selected[str(o)] = self.verts[self.vert_ids.index(int(o))]
                    self.itemconfig(o, width=2, outline="gold")
                else:
                    self.itemconfig(o, width=0, outline="")
                    del self.selected[str(o)]
                added = True
        if added == False:
            for sel in self.selected:
                self.itemconfig(int(sel), width=0, outline="")
            self.selected.clear()
            
    def rot_selected(self, direc):
        turn = 0
        if direc == "Left":
            turn = 0.04
        elif direc == "Right":
            turn = -0.04
        for sel in self.selected:
            if self.type(int(sel)) == "polygon":
                self.selected[sel].rotate(turn)
                shape = self.shapes.pop(sel)
                self.shapes[str(shape.id)] = shape
                self.selected.pop(sel)
                self.selected[str(shape.id)] = shape
        for sel in self.selected:
            self.itemconfig(int(sel), width=2, outline="gold")

    def scale_selected(self, opt):
        factor = 1
        if opt == "mag":
            factor = 1.04
        elif opt == "shr":
            factor = 0.96
        for sel in self.selected:
            if self.type(int(sel)) == "polygon":
                self.selected[sel].scale(factor)
                shape = self.shapes.pop(sel)
                self.shapes[str(shape.id)] = shape
                self.selected.pop(sel)
                self.selected[str(shape.id)] = shape
        for sel in self.selected:
            self.itemconfig(int(sel), width=2, outline="gold")

    def move_selected(self, direc):
        '''
            Responds to arrow key events.
             Moves all selected objects on the canvas in the given direction.
            Arrow keys can be held down for continuous movement.
            This funct takes advantage of Shape's built in move method for
            convenience. Point data is updated in this funct directly, however,
            when moving selected vertices(ovals).
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
            if self.type(int(sel)) == "polygon":
                self.selected[sel].move(move_dir[0], move_dir[1])
            elif self.type(int(sel)) == "oval":
                self.move(int(sel), move_dir[0], move_dir[1])
                self.verts[self.vert_ids.index(int(sel))][0] += move_dir[0]
                self.verts[self.vert_ids.index(int(sel))][1] += move_dir[1]

    def lower_selected(self):
        for sel in self.selected:
            self.lower(int(sel))

    def raise_selected(self):
        for sel in self.selected:
            self.lift(int(sel))

    def del_selected(self, e):
        while len(self.selected):
            obj = self.selected.popitem()
            iden = int(obj[0])
            if self.type(iden) == "polygon": 
                del self.shapes[obj[0]]
            if self.type(iden) == "oval":
                indx = self.vert_ids.index(iden)
                self.vert_ids.pop(indx)
                self.verts.pop(indx)
            self.delete(iden)

    def dup_selected(self, e):
        for sel in self.selected:
            if self.type(int(sel)) == "polygon":
                shape = self.selected[sel].duplicate()
                self.shapes[str(shape.id)] = shape

    def addbgImage(self):
        filenm = filedialog.askopenfilename(filetypes=(("All", "*.*"),("png", ".png"),("gif", ".gif"), ("jpg", ".jpg")))
        if filenm:
            self.img = ImageTk.PhotoImage(file=filenm)
            self.bgImage = self.create_image(0,0,image=self.img,anchor=NW)
            self.lower(self.bgImage)

    def export_image(self):
        if self.configured == True:
            filenm = filedialog.asksaveasfilename(initialdir = "/", title = "select file", filetypes = (("png","*.png"),("all files","*.*")))
            img = Image.new('RGBA', (self.width, self.height), color=(0,0,0,0))
            d = ImageDraw.Draw(img)
            for s in self.shapes:
                tupled = []
                for pt in self.shapes[s].points:
                    tupled += [tuple(pt)]
                d.polygon(tupled, fill=colorTranslator[self.shapes[s].color])
            img.save(filenm+".png", format='png')
    
    def get_keys(self, e):
        '''
            Responds to key events (mostly alphabet keys).
            Creates a polygon from the verts currently on canvas. The color of the polygon is
            determined by the key pressed. The z key is reserved for shifting the vertex color,
            if it is pressed a function is called to shift the vert color and the function is
            returned from before shape creation code.
        '''
        if e.char == ',':
            self.rot_selected("Left")
            return
        elif e.char == '.':
            self.rot_selected("Right")
            return
        elif e.char == '-':
            self.scale_selected("shr")
        elif e.char == '=':
            self.scale_selected("mag")
        elif e.char == '[':
            self.lower_selected()
        elif e.char == ']':
            self.raise_selected()
        color = "black"
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
        elif e.char == "z":
            self.shift_vert_col()
        return
    
    def __init__(self, wid, hgt):
        self.root = Tk()
        super().__init__(self.root, width=wid, height=hgt)
        super().pack()
        self.configured = False
        self.img = None
        self.bgImage = None
        self.width = wid
        self.height = hgt
        self.verts = []
        self.vert_ids = []
        self.vert_color = "black"
        self.col_ind = 0
        self.colors = ["black", "red", "orange", "yellow", "green", "blue", "purple", "white"]
        self.shapes = {}
        self.selected = {}
        self.box_anchor = [-1,-1]
        self.select_box = None
        self.select_box_pts = [-1,-1,-1,-1]
        self.root.bind("<Button-1>", self.make_point)
        self.root.bind("<Button-3>", self.select)
        self.root.bind("<Key>", self.get_keys)
        self.root.bind("<Up>", lambda a: self.move_selected("Up"))
        self.root.bind("<Down>", lambda a: self.move_selected("Down"))
        self.root.bind("<Left>", lambda a: self.move_selected("Left"))
        self.root.bind("<Right>", lambda a: self.move_selected("Right"))
        self.root.bind("<BackSpace>", self.del_selected)
        self.root.bind("<Return>", self.dup_selected)
        menu_bar = Menu(self.root)
        image_menu = Menu(menu_bar)
        menu_bar.add_cascade(label="Image", menu=image_menu)
        image_menu.add_command(label="Export", command=self.export_image)
        image_menu.add_command(label="Background Image", command=self.addbgImage)
        self.root.config(menu=menu_bar)
        self.configured = True
        self.root.mainloop()

    
def rotatePoint(point, pivot, rads):
    x = point[0]-pivot[0]
    y = pivot[1]-point[1]
    r = sqrt(pow(x, 2)+pow(y,2))
    ang = atan2(y,x)+rads
    point[0] = pivot[0] + r*cos(ang)
    point[1] = pivot[1] - r*sin(ang)

class Shape:
    def __init__(self, points, color, display):
        self.points = points
        self.color = color
        self.display = display
        self.id = self.display.create_polygon(points, fill=color)
        self.bbox = display.bbox(self.id)
        self.pivot = [(self.bbox[0]+self.bbox[2])//2,(self.bbox[1]+self.bbox[3])//2]
        
    def move(self, xAmt, yAmt):
        self.display.move(self.id, xAmt, yAmt)
        for point in self.points:
            point[0] += xAmt
            point[1] += yAmt
        self.pivot[0] += xAmt
        self.pivot[1] += yAmt
        self.bbox = self.display.bbox(self.id)

    def rotate(self, rads):
        self.display.delete(self.id)
        for point in self.points:
            rotatePoint(point, self.pivot, rads)
        self.id = self.display.create_polygon(self.points, fill=self.color)
        self.bbox = self.display.bbox(self.id)

    def scale(self, factor):
        self.display.delete(self.id)
        for point in self.points:
            point[0] = self.pivot[0] + (point[0]-self.pivot[0])*factor
            point[1] = self.pivot[1] + (point[1]-self.pivot[1])*factor
        self.id = self.display.create_polygon(self.points, fill=self.color)
        self.bbox = self.display.bbox(self.id)

    def duplicate(self):
        points = []
        for point in self.points:
            pt = point.copy()
            points.append(pt)
        return Shape(points, self.color, self.display)
        
    def setPivot(self, pos):
        self.pivot = pos

    def printData(self):
        print("id = ", self.id, " points = ", self.points, " pivot = ", self.pivot)

def main():
    d = PFDisplay(1000,800)

if __name__ == '__main__':
    #main()
    d = PFDisplay(1000,800)
