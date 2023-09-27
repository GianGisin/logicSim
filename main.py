from enum import Enum
import sys
import math
from gates import gates
from gates.gates import GateType
from tkinter import Tk, PhotoImage, Menu, Frame, Canvas, messagebox
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

RULE_DRAW_DIRECT_LINES = True
RULE_TOOLBAR_BUTTON_STYLE = "image"

# gates to simulate will be stored in dict together with their tkinter ID
gate_sim = {}


class Tool(Enum):
    POINTER = 0
    PEN = 1
    GATE = 2
    BIN = 3
    LAMP = 4
    SWITCH = 5


def clear_canvas():
    if len(canvas.find_all()) != 0:
        if messagebox.askokcancel(message="Are you sure you want to clear the canvas?"):
            gate_sim.clear()
            canvas.delete("all")
            l.clear()
            gate_tags.clear()


def draw_circle(x, y, r, fill="red", outline="red", tags=[]):
    return canvas.create_oval(
        x - r, y - r, x + r, y + r, fill=fill, outline=outline, tags=tags
    )


def draw_gate(x: int, y: int, gate_type: GateType):
    y_offset = 20
    x_offset = math.floor(IMAGE_SCALED_WIDTH / 2)

    q_pos = (x + x_offset, y)
    a_pos = (x - x_offset, y - y_offset)
    b_pos = (x - x_offset, y + y_offset)

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

    # add new gate to the simulation dict
    gate_sim.update({gate_id: gates.gate_from_type(gate_type)})
    print(gate_sim)


def toggle_lamp(id):
    # toggle switch state
    if "lamp_on" in canvas.gettags(id):
        # change the image to off
        canvas.itemconfigure(id, image=lamp_off)
        # change the tag from "lamp_on" to "lamp_off"
        canvas.dtag(id, "lamp_on")
        canvas.addtag_withtag("lamp_off", id)
    else:
        # change the image to on
        canvas.itemconfigure(id, image=lamp_on)
        # change the tag from "lamp_off" to "lamp_on"
        canvas.dtag(id, "lamp_off")
        canvas.addtag_withtag("lamp_on", id)


def draw_lamp(x: int, y: int):
    lamp_id = canvas.create_image(x, y, image=lamp_off)
    canvas.addtag_withtag(f"lamp{lamp_id}", lamp_id)
    canvas.addtag_withtag(f"A", lamp_id)
    canvas.addtag_withtag("lamp_off", lamp_id)
    canvas.tag_bind(lamp_id, "<Button-1>", lambda e: leftclick_on_lamp(lamp_id))
    sim_lamp = gates.Lamp(on_update=lambda: toggle_lamp(lamp_id), init_state=False)
    gate_sim.update({lamp_id: sim_lamp})


def draw_switch(x: int, y: int):
    switch_id = canvas.create_image(x, y, image=switch_off)
    canvas.addtag_withtag(f"switch{switch_id}", switch_id)
    canvas.addtag_withtag(f"Q", switch_id)
    canvas.addtag_withtag("switch_off", switch_id)
    canvas.tag_bind(switch_id, "<Button-1>", lambda e: leftclick_on_switch(switch_id))
    sim_switch = gates.Switch(init_state=False)
    gate_sim.update({switch_id: sim_switch})


current_tool = 0


def toolbar_event(tool_num):
    global current_tool
    for border in borders:
        border.configure(background="grey75")

    current_tool = Tool(tool_num)
    if current_tool == Tool.PEN:
        l.clear()
        gate_tags.clear()
    borders[tool_num].configure(background="blue")
    print(f"Toolbar event, tool {current_tool} selected. input: {tool_num}")


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
        gate_tags.append([canvas.gettags(id)[0], canvas.gettags(id)[1]])
        # check whether there are two points
        if len(l) >= 4:
            # check if desired connection is Q->A or Q->B
            conn = {gate_tags[0][1], gate_tags[1][1]}
            if len(conn) == 2 and "Q" in conn:
                if gate_tags[0][0] != gate_tags[1][0]:
                    # draw the connection
                    dx = l[2] - l[0]

                    line_id = None

                    if RULE_DRAW_DIRECT_LINES:
                        line_id = canvas.create_line(l[0], l[1], l[2], l[3], width=3)
                    else:
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
                    canvas.tag_bind(
                        line_id, "<Button-1>", lambda e: leftclick_on_line(line_id)
                    )

                    # get id out of gate tag
                    id1 = int(
                        gate_tags[0][0]
                        .replace("gate", "")
                        .replace("switch", "")
                        .replace("lamp", "")
                    )
                    id2 = int(
                        gate_tags[1][0]
                        .replace("gate", "")
                        .replace("switch", "")
                        .replace("lamp", "")
                    )
                    LUI = ""
                    if gate_tags[0][1] == "Q":
                        # connection id1 -> id2
                        canvas.addtag_withtag(gate_tags[0][0], line_id)
                        canvas.addtag_withtag(gate_tags[1][0], line_id)
                        if gate_tags[1][1] == "A":
                            # connection id1(Q) -> id2("A")
                            LUI = f"{id2}A"
                            gate_sim[id1].Q.connect(gate_sim[id2].A, key=LUI)
                        elif gate_tags[1][1] == "B":
                            # connection id1(Q) -> id2("B")
                            LUI = f"{id2}B"
                            gate_sim[id1].Q.connect(gate_sim[id2].B, key=LUI)
                    elif gate_tags[1][1] == "Q":
                        # connection id2 -> id1
                        canvas.addtag_withtag(gate_tags[1][0], line_id)
                        canvas.addtag_withtag(gate_tags[0][0], line_id)
                        if gate_tags[0][1] == "A":
                            # connection id2(Q) -> id1("A")
                            LUI = f"{id1}A"
                            gate_sim[id2].Q.connect(gate_sim[id1].A, key=LUI)
                        elif gate_tags[0][1] == "B":
                            # connection id2(Q) -> id1("B")
                            LUI = f"{id1}B"
                            gate_sim[id2].Q.connect(gate_sim[id1].B, key=LUI)
                    canvas.addtag_withtag(LUI, line_id)
                    print(
                        f"making connection between\n    |gate{id1} ({gate_tags[0][1]})\n    |gate{id2} ({gate_tags[1][1]})\n    |tags {canvas.gettags(line_id)}"
                    )

                else:
                    messagebox.showwarning(
                        message="Cannot connect input and output belonging to the same gate."
                    )
            else:
                messagebox.showwarning(
                    message="Cannot connect two inputs or two outputs."
                )
            l.clear()
            gate_tags.clear()


def leftclick_on_line(id):
    print(
        f" leftclick_on_line: Click on line with id {id} and coords {canvas.coords(id)} and tags {canvas.gettags(id)}"
    )
    match current_tool:
        case Tool.BIN:
            # delete connection from simulation
            # get ID of output gate
            # as the order of the tags is established in leftclick_on_circ, we can assume
            # that the first tag is the id of the output gate
            QID = int(canvas.gettags(id)[0].replace("gate", "").replace("switch", ""))
            LUI = canvas.gettags(id)[2]
            print(f"Deleting connection at gateid {QID} with identifier {LUI}")
            # delete line from canvas
            gate_sim[QID].Q.disconnect(LUI)
            canvas.delete(id)


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

            # TODO:
            # - delete gate from simulation


def leftclick_on_lamp(id):
    print(
        f"Click on lamp with id {id} and coords {canvas.coords(id)} and tags {canvas.gettags(id)}"
    )
    match current_tool:
        case Tool.PEN:
            leftclick_on_circ(id)
        case Tool.BIN:
            tags = canvas.gettags(id)
            canvas.delete(tags[0])


def leftclick_on_switch(id):
    print(
        f"Click on switch with id {id} and coords {canvas.coords(id)} and tags {canvas.gettags(id)}"
    )
    match current_tool:
        case Tool.PEN:
            leftclick_on_circ(id)

        case Tool.POINTER:
            # toggle switch state
            if "switch_on" in canvas.gettags(id):
                # change the image to off
                canvas.itemconfigure(id, image=switch_off)
                # change the tag from "switch_on" to "switch_off"
                canvas.dtag(id, "switch_on")
                canvas.addtag_withtag("switch_off", id)
                gate_sim[id].Q.send(False)
            else:
                # change the image to on
                canvas.itemconfigure(id, image=switch_on)
                # change the tag from "switch_off" to "switch_on"
                canvas.dtag(id, "switch_off")
                canvas.addtag_withtag("switch_on", id)
                gate_sim[id].Q.send(True)

        case Tool.BIN:
            tags = canvas.gettags(id)
            canvas.delete(tags[0])


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
root.iconphoto(True, gate_icon)
root.title("logicSim")
root.geometry("1000x700+0+0")
root.option_add("*tearOff", False)
root.bind("<Control-g>", lambda e: print(gate_sim))
root.bind("<Control-c>", lambda e: sys.exit(0))
root.bind("<Control-Delete>", lambda e: clear_canvas())
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# initialize menubar
m = Menu(root)
m_edit = Menu(m)
m_debug = Menu(m)
m.add_cascade(menu=m_edit, label="Edit")
m.add_cascade(menu=m_debug, label="Debug")
m_edit.add_command(
    label="Clear Canvas", command=clear_canvas, accelerator="Ctrl-Delete"
)
m_edit.add_command(label="--- placeholder ---")
m_debug.add_command(
    label="Print simulation list", command=lambda: print(gate_sim), accelerator="Ctrl-g"
)
m_debug.add_command(label="--- placeholder ---")
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
button_text = ["cursor", "pen", "gate", "delete", "lamp", "switch"]
button_images = [cursor, pen, gate_icon, waste_bin, lamp, switch]

# initialize toolbar buttons
for i in range(len(button_text)):
    border = Frame(toolbar, background="grey75", bd=2)
    border.grid(column=i + 1, row=1)
    borders.append(border)
    button = ttk.Button(
        border,
        image=button_images[i],
        text=button_text[i],
        compound=RULE_TOOLBAR_BUTTON_STYLE,
        command=lambda i=i: toolbar_event(i),
    )
    button.pack()

# start event loop
root.mainloop()
