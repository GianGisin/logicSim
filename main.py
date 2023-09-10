from tkinter import Tk, PhotoImage, Menu, Frame, Canvas
from tkinter import ttk, messagebox
from PIL import Image, ImageTk


def draw_gate(x, y):
    radius = 5
    y_offset = 20
    canvas.create_image(x, y, image=gate)
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
    print(f"leftclick with tool {current_tool}")
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
        

root = Tk()

cursor = PhotoImage(file="img/toolbar_icons/pointer.png")
pen = PhotoImage(file="img/toolbar_icons/pen.png")
gate_icon = PhotoImage(file="img/toolbar_icons/gate-icon.png")

img = Image.open("img/gate.png")
img = img.resize((100,75))
gate = ImageTk.PhotoImage(img)

root.iconphoto(False, cursor)
root.title("logicSim")
root.geometry("500x500")
root.option_add('*tearOff', False)

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
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.columnconfigure(0, weight=1)
# mainframe.rowconfigure(0, weight=1)
mainframe.rowconfigure(1, weight=1)

toolbar = ttk.Frame(mainframe, relief="raised", borderwidth=2)
toolbar.grid(column=0, row=0, sticky="new")

canvas = Canvas(mainframe, background="grey75")
canvas.grid(column=0, row=1, sticky="nesw")
canvas.bind("<Button-1>", leftclick_event)

draw_gate(200, 200)
draw_gate(400, 400)

gateselect = ttk.Combobox(toolbar)
gateselect['values'] = ('NOT', 'AND', 'OR', 'XOR', 'NAND', 'NOR', 'XNOR')
gateselect.state(['readonly'])
gateselect.set('NOT')
gateselect.grid(column=4, row=1)


borders = []

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

root.mainloop()