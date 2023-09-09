from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk


def draw_gate(x, y):
    radius = 5
    y_offset = 20
    canvas.create_image(x, y, image=gate)
    canvas.create_oval(x+50-radius, y-radius, x+50+radius, y+radius, fill="red")
    canvas.create_oval(x-50-radius, y-radius+y_offset, x-50+radius, y+radius+y_offset, fill="red")
    canvas.create_oval(x-50-radius, y-radius-y_offset, x-50+radius, y+radius-y_offset, fill="red")

def toolbar_event(*args):
    print("toolbar event")
    if len(args) != 0:
        for border in borders:
            border.configure(background="grey75")
        
        borders[args[0]].configure(background="blue")


class Line:
    x = -1
    y = -1
    
    def reset(self):
        self.x = -1
        self.y = -1

l = Line()

def setPoint(event):
    print(f"x: {event.x}\ny: {event.y}")
    if l.x == -1:
        l.x = event.x
        l.y = event.y
    else:
        canvas.create_line(l.x, l.y, event.x, event.y, width=3)
        l.reset()

root = Tk()

cursor = PhotoImage(file="img/pointer.png")
pen = PhotoImage(file="img/pen.png")
gate_icon = PhotoImage(file="img/gate-icon.png")

img = Image.open("img/gate.png")
img = img.resize((100,75))
gate = ImageTk.PhotoImage(img)

root.iconphoto(False, cursor)
root.title("logicSim")
root.geometry("500x500")
root.option_add('*tearOff', FALSE)
# root.attributes("-alpha", 0.5)
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

toolbar = ttk.Frame(mainframe, relief=RAISED, borderwidth=2)
toolbar.grid(column=0, row=0, sticky="new")

canvas = Canvas(mainframe, background="grey75")
canvas.grid(column=0, row=1, sticky="nesw")
canvas.bind("<Button-1>", setPoint)

draw_gate(200, 200)
draw_gate(400, 400)

gateselect = ttk.Combobox(toolbar)
gateselect['values'] = ('NOT', 'AND', 'OR', 'XOR', 'NAND', 'NOR', 'XNOR')
gateselect.state(['readonly'])
gateselect.set('NOT')
gateselect.grid(column=4, row=1)


borders = []

bborder = Frame(toolbar, background="grey75", bd=2)
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