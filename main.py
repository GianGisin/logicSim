from enum import Enum
from tkinter import Tk, PhotoImage, Menu, Frame, Canvas
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

GATE_NAMES = ('NOT', 'AND', 'OR', 'XOR', 'NAND', 'NOR', 'XNOR')

class GateType(Enum):
    NOT = 0
    AND = 1
    OR = 2
    XOR = 3
    NAND = 4
    NOR = 5
    XNOR = 6


def draw_gate(x: int, y: int, gate_type: GateType):
    radius = 5
    y_offset = 20
    canvas.create_image(x, y, image=gate_images[gate_type.value])
    canvas.create_oval(x+50-radius, y-radius, x+50+radius, y+radius, fill="red")
    canvas.create_oval(x-50-radius, y-radius+y_offset, x-50+radius, y+radius+y_offset, fill="red")
    canvas.create_oval(x-50-radius, y-radius-y_offset, x-50+radius, y+radius-y_offset, fill="red")

current_tool = 0

def TODO(st):
    print(f"TODO {st}")

def toolbar_event(*args):
    global current_tool
    if len(args) != 0:
        for border in borders:
            border.configure(background="grey75")
        
        current_tool = args[0]
        borders[args[0]].configure(background="blue")
        print(f"toolbar event, tool {current_tool} selected.")


class Line:
    x = -1
    y = -1
    
    def reset(self):
        self.x = -1
        self.y = -1

l = Line()

def leftclick_event(event):
    print(f"leftclick with tool {current_tool}\n")
    match current_tool:
        case 0:
            # pointer tool selected
            TODO("handle pointer click")
        case 1:
            # draw tool selected
            print(f"x: {event.x}\ny: {event.y}")
            if l.x == -1:
                l.x = event.x
                l.y = event.y
            else:
                canvas.create_line(l.x, l.y, event.x, event.y, width=3)
                l.reset()
            
        case 2:
            # gate tool selected
            TODO("handle gate click")
            # check selected tool from gateselect

            current_selection = gateselect.get()
            print(current_selection + "\n")
            match current_selection:
                case 'NOT':
                    pass
                case 'AND': 
                    pass
                case 'OR': 
                    pass
                case 'XOR': 
                    pass
                case 'NAND': 
                    pass
                case 'NOR': 
                    pass
                case 'XNOR': 
                    pass
        
def combobox_event(event):
    gateselect.selection_clear()

# initialize main window
root = Tk()

cursor = PhotoImage(file="img/toolbar_icons/pointer.png")
pen = PhotoImage(file="img/toolbar_icons/pen.png")
gate_icon = PhotoImage(file="img/toolbar_icons/gate-icon.png")

gate_images = []

# load all gate images into list, after resizing them
for gate in GATE_NAMES:
    path_string = "img/gate_img/GATE_" + gate + ".png"
    print(path_string)
    img = Image.open(path_string)
    img = img.resize((100,75))
    gate_images.append(ImageTk.PhotoImage(img)) 

# initialize main window
root.iconphoto(False, cursor)
root.title("logicSim")
root.geometry("500x500")
root.option_add('*tearOff', False)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# initialize menubar
m = Menu(root)
m_edit = Menu(m)
m_save = Menu(m)
m.add_cascade(menu=m_edit, label="Edit")
m.add_cascade(menu=m_save, label="Save")
m_edit.add_command(label="Paste")
m_edit.add_command(label="Find...")
m_save.add_command(label="Paste")
m_save.add_command(label="Find...")
root['menu'] = m

mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0, sticky="nsew")
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(1, weight=1)

# initialize toolbar
toolbar = ttk.Frame(mainframe, relief="raised", borderwidth=2)
toolbar.grid(column=0, row=0, sticky="new")

# initialize canvas
canvas = Canvas(mainframe, background="grey75")
canvas.grid(column=0, row=1, sticky="nesw")
canvas.bind("<Button-1>", leftclick_event)

draw_gate(200, 200, GateType.AND)
draw_gate(400, 400, GateType.OR)

gateselect = ttk.Combobox(toolbar)
gateselect['values'] = GATE_NAMES
gateselect.state(['readonly'])
gateselect.set('NOT')
gateselect.grid(column=4, row=1)
gateselect.bind('<<ComboboxSelected>>', combobox_event)

borders = []

# create toolbar buttons and borders to show selected tool
bborder = Frame(toolbar, background="blue", bd=2)
bborder.grid(column=1, row=1)
borders.append(bborder)
b = ttk.Button(bborder, image=cursor, text="cursor", command=lambda: toolbar_event(0))
b.pack()

cborder = Frame(toolbar, background="grey75", bd=2)
cborder.grid(column=2, row=1)
borders.append(cborder)
c = ttk.Button(cborder, image=pen, text="pen", command=lambda: toolbar_event(1))
c.pack()

dborder = Frame(toolbar, background="grey75", bd=2)
dborder.grid(column=3, row=1)
borders.append(dborder)
d = ttk.Button(dborder, image=gate_icon, text="gate", command=lambda: toolbar_event(2))
d.pack()

# start event loop
root.mainloop()