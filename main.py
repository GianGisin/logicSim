from tkinter import *
from tkinter import ttk, messagebox

def toolbar_event(*args):
    print("toolbar event")
    if len(args) != 0:
        match args[0]:
            case 0:
                bborder.configure(highlightbackground="blue")
                cborder.configure(highlightbackground="white")
            case 1:
                bborder.configure(highlightbackground="white")
                cborder.configure(highlightbackground="blue")
                

root = Tk()

cursor = PhotoImage(file="img/pointer.png")
pen = PhotoImage(file="img/pen.png")

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

canvas = Canvas(mainframe, background="red")
canvas.grid(column=0, row=1, sticky="nesw")

gateselect = ttk.Combobox(toolbar)
gateselect['values'] = ('NOT', 'AND', 'OR', 'XOR', 'NAND', 'NOR', 'XNOR')
gateselect.state(['readonly'])
gateselect.set('NOT')
gateselect.grid(column=3, row=1)


bborder = Frame(toolbar, highlightbackground="white", highlightthickness=2, bd=0)
bborder.grid(column=1, row=1)
b = Button(bborder, image=cursor, text="cursor", command=lambda: toolbar_event(0))
b.pack()

cborder = Frame(toolbar, highlightbackground="white", highlightthickness=2, bd=0)
cborder.grid(column=2, row=1)
c = Button(cborder, image=pen, text="pen", command=lambda: toolbar_event(1), background="blue")
c.pack()

root.mainloop()