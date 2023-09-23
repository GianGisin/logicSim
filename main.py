from enum import Enum
import math
from tkinter import Tk, PhotoImage, Menu, Frame, Canvas
from tkinter import ttk
from PIL import Image, ImageTk

GATE_NAMES = ("NOT", "AND", "OR", "XOR", "NAND", "NOR", "XNOR")

CIRCLE_RADIUS = 5

IMAGE_WIDTH = 200
IMAGE_HEIGHT = 150
IMAGE_RATIO = IMAGE_HEIGHT / IMAGE_WIDTH
IMAGE_SCALE_FACTOR = 0.5
IMAGE_SCALED_WIDTH = math.floor(IMAGE_WIDTH * IMAGE_SCALE_FACTOR)
IMAGE_SCALED_HEIGHT = math.floor(IMAGE_HEIGHT * IMAGE_SCALE_FACTOR)

LAMP_IMAGE_SIDE = 50


class IO:
    def __init__(self, id, powered=False) -> None:
        self.id = id
        self.powered = powered


class GateType(Enum):
    NOT = 0
    AND = 1
    OR = 2
    XOR = 3
    NAND = 4
    NOR = 5
    XNOR = 6


class Tool(Enum):
    POINTER = 0
    PEN = 1
    GATE = 2
    BIN = 3
    LAMP = 4
    SWITCH = 5


def draw_circle(x, y, r, fill="red", outline="red", tags=[]):
    return canvas.create_oval(
        x - r, y - r, x + r, y + r, fill=fill, outline=outline, tags=tags
    )


def draw_gate(x: int, y: int, gate_type: GateType):
    y_offset = 20
    x_offset = math.floor(IMAGE_SCALED_WIDTH / 2)

    q_pos = (x + x_offset, y)
    a_pos = (x - x_offset, y + y_offset)
    b_pos = (x - x_offset, y - y_offset)

    gate_id = canvas.create_image(x, y, image=gate_images[gate_type.value])
    canvas.addtag_withtag(f"gate{gate_id}", gate_id)

    q_circ = draw_circle(
        q_pos[0], q_pos[1], CIRCLE_RADIUS, tags=(f"gate{gate_id}", "Q")
    )
    a_circ = draw_circle(
        a_pos[0], a_pos[1], CIRCLE_RADIUS, tags=(f"gate{gate_id}", "A")
    )

    canvas.tag_bind(gate_id, "<Button-1>", lambda e: leftclick_on_gate(gate_id))
    canvas.tag_bind(q_circ, "<Button-1>", lambda e: leftclick_on_circ(q_circ))
    canvas.tag_bind(a_circ, "<Button-1>", lambda e: leftclick_on_circ(a_circ))

    if gate_type != GateType.NOT:
        b_circ = draw_circle(
            b_pos[0], b_pos[1], CIRCLE_RADIUS, tags=(f"gate{gate_id}", "B")
        )
        canvas.tag_bind(b_circ, "<Button-1>", lambda e: leftclick_on_circ(b_circ))


def draw_lamp(x: int, y: int):
    lamp_id = canvas.create_image(x, y, image=lamp_off)
    canvas.addtag_withtag("lamp_off", lamp_id)
    canvas.tag_bind(lamp_id, "<Button-1>", lambda e: leftclick_on_lamp(lamp_id))


def draw_switch(x: int, y: int):
    switch_id = canvas.create_image(x, y, image=switch_off)
    canvas.addtag_withtag("switch_off", switch_id)
    canvas.tag_bind(switch_id, "<Button-1>", lambda e: leftclick_on_switch(switch_id))


current_tool = 0


def toolbar_event(*args):
    global current_tool
    if len(args) != 0:
        for border in borders:
            border.configure(background="grey75")

        current_tool = Tool(args[0])
        borders[args[0]].configure(background="blue")
        print(f"Toolbar event, tool {current_tool} selected.")


l = []
gate_tags = []


def leftclick_on_circ(id):
    current_coords = canvas.coords(id)
    print(
        f"Click on circle with id {id} and coords {current_coords} and tags {canvas.gettags(id)}"
    )
    if current_tool == Tool.PEN:
        # TODO more checks needed so no loops can be drawn
        l.extend([current_coords[0] + CIRCLE_RADIUS, current_coords[1] + CIRCLE_RADIUS])
        gate_tags.append(canvas.gettags(id)[0])
        if len(l) >= 4:
            # draw the connection
            dx = l[2] - l[0]
            print("drawing line")
            line_id = canvas.create_line(
                [
                    l[0],
                    l[1],
                    l[0] + math.floor(dx / 2),
                    l[1],
                    l[0] + math.floor(dx / 2),
                    l[1],
                    l[0] + math.floor(dx / 2),
                    l[3],
                    l[0] + math.floor(dx / 2),
                    l[3],
                    l[2],
                    l[3],
                ],
                width=3,
            )
            canvas.tag_bind(line_id, "<Button-1>", lambda e: leftclick_on_line(line_id))
            canvas.addtag_withtag(gate_tags[0], line_id)
            canvas.addtag_withtag(gate_tags[1], line_id)
            l.clear()
            gate_tags.clear()
            print(f"line now has tags: {canvas.gettags(id)}")


def leftclick_on_line(id):
    print(
        f"Click on line with id {id} and coords {canvas.coords(id)} and tags {canvas.gettags(id)}"
    )
    match current_tool:
        case Tool.BIN:
            canvas.delete(id)
            # TODO: delete connection from simulation


def leftclick_on_gate(id):
    print(
        f"Click on gate with id {id} and coords {canvas.coords(id)} and tags {canvas.gettags(id)}"
    )
    match current_tool:
        case Tool.POINTER:
            # possibly drag to move
            pass
        case Tool.BIN:
            # delete gate
            # get gate tags
            print("at delete")
            tags = canvas.gettags(id)
            print(f"deleting objects with tag {tags[0]}")
            print(f"all objects with tag {tags[0]}: {canvas.find_withtag(tags[0])}")
            canvas.delete(tags[0])
            canvas.delete(tags[0])

            # TODO:
            # - delete gate from simulation
            # - delete connected lines


def leftclick_on_lamp(id):
    print(
        f"Click on lamp with id {id} and coords {canvas.coords(id)} and tags {canvas.gettags(id)}"
    )
    if current_tool == Tool.BIN:
        canvas.delete(id)
        # TODO: delete all attached lines


def leftclick_on_switch(id):
    print(
        f"Click on switch with id {id} and coords {canvas.coords(id)} and tags {canvas.gettags(id)}"
    )
    if current_tool == Tool.POINTER:
        # toggle switch state
        if "switch_on" in canvas.gettags(id):
            # change the image to on
            canvas.itemconfigure(id, image=switch_off)
            # change the tag from "switch_off" to "switch_on"
            canvas.dtag(id, "switch_on")
            canvas.addtag_withtag("switch_off", id)
        else:
            # change the image to on
            canvas.itemconfigure(id, image=switch_on)
            # change the tag from "switch_off" to "switch_on"
            canvas.dtag(id, "switch_off")
            canvas.addtag_withtag("switch_on", id)

    if current_tool == Tool.BIN:
        canvas.delete(id)
        # TODO: delete all attached lines


def leftclick_event(event):
    if current_tool == Tool.GATE:
        # gate tool selected
        draw_gate(event.x, event.y, GateType[gateselect.get()])
    if current_tool == Tool.LAMP:
        draw_lamp(event.x, event.y)
    if current_tool == Tool.SWITCH:
        draw_switch(event.x, event.y)


def combobox_event(event):
    gateselect.selection_clear()


# initialize main window
root = Tk()

# load toolbar icons
cursor = PhotoImage(file="img/toolbar_icons/pointer.png")
pen = PhotoImage(file="img/toolbar_icons/pen.png")
gate_icon = PhotoImage(file="img/toolbar_icons/gate-icon.png")
waste_bin = PhotoImage(file="img/toolbar_icons/bin.png")
lamp = PhotoImage(file="img/toolbar_icons/lamp.png")
switch = PhotoImage(file="img/toolbar_icons/switch.png")

gate_images = []

# load all gate images into list, after resizing them
for gate in GATE_NAMES:
    path_string = "img/gate_img/GATE_" + gate + ".png"
    print(path_string)
    img = Image.open(path_string)
    img = img.resize((IMAGE_SCALED_WIDTH, IMAGE_SCALED_HEIGHT))
    gate_images.append(ImageTk.PhotoImage(img))

# load lamp state images, use nearest neighbour interpolation for resizing
lamp_on = Image.open("img/gate_img/LAMP_ON.png").resize(
    (LAMP_IMAGE_SIDE, LAMP_IMAGE_SIDE), Image.NEAREST
)
lamp_on = ImageTk.PhotoImage(lamp_on)

lamp_off = Image.open("img/gate_img/LAMP_OFF.png").resize(
    (LAMP_IMAGE_SIDE, LAMP_IMAGE_SIDE), Image.NEAREST
)
lamp_off = ImageTk.PhotoImage(lamp_off)

# load switch images, use nearest neighbour interpolation for resizing
switch_on = Image.open("img/gate_img/SWITCH_ON.png").resize((72, 48), Image.NEAREST)
switch_off = switch_on.rotate(180, Image.NEAREST)
switch_off = ImageTk.PhotoImage(switch_off)
switch_on = ImageTk.PhotoImage(switch_on)

# initialize main window
root.iconphoto(False, cursor)
root.title("logicSim")
root.geometry("500x500")
root.option_add("*tearOff", False)
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
root["menu"] = m

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

# initialize gate selection box
gateselect = ttk.Combobox(toolbar)
gateselect["values"] = GATE_NAMES
gateselect.state(["readonly"])
gateselect.set("NOT")
gateselect.grid(column=7, row=1)
gateselect.bind("<<ComboboxSelected>>", combobox_event)

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

eborder = Frame(toolbar, background="grey75", bd=2)
eborder.grid(column=4, row=1)
borders.append(eborder)
e = ttk.Button(eborder, image=waste_bin, text="bin", command=lambda: toolbar_event(3))
e.pack()

fborder = Frame(toolbar, background="grey75", bd=2)
fborder.grid(column=5, row=1)
borders.append(fborder)
f = ttk.Button(fborder, image=lamp, text="bin", command=lambda: toolbar_event(4))
f.pack()

gborder = Frame(toolbar, background="grey75", bd=2)
gborder.grid(column=6, row=1)
borders.append(gborder)
g = ttk.Button(gborder, image=switch, text="bin", command=lambda: toolbar_event(5))
g.pack()

# start event loop
root.mainloop()
