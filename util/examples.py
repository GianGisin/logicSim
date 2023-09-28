from gates.gates import GateType


class ExDraw:
    examples = ["half adder", "full adder"]

    def __init__(self, ds, dl, dg, c, cc) -> None:
        self.ds = ds
        self.dl = dl
        self.dg = dg
        self.c = c
        self.cc = cc

    def cn(self, id1, id2):
        self.c(id1, eg=True)
        self.c(id2, eg=True)

    def draw_example(self, name: str):
        if name == "half adder":
            self.cc(forced=True)
            self.ds(100, 100)
            self.ds(100, 400)
            self.dl(600, 95)
            self.dl(600, 395)
            self.dg(350, 100, GateType.XOR)
            self.dg(350, 400, GateType.AND)
            self.c(1, eg=True)
            self.c(7, eg=True)
            self.c(1, eg=True)
            self.c(11, eg=True)
            self.c(2, eg=True)
            self.c(8, eg=True)
            self.c(2, eg=True)
            self.c(12, eg=True)
            self.c(6, eg=True)
            self.c(3, eg=True)
            self.c(10, eg=True)
            self.c(4, eg=True)
        if name == "full adder":
            self.cc(forced=True)
            self.ds(100, 100)
            self.ds(100, 300)
            self.ds(100, 500)
            self.dl(900, 195)
            self.dl(900, 395)
            self.dg(300, 100, GateType.XOR)
            self.dg(400, 500, GateType.AND)
            self.dg(500, 200, GateType.XOR)
            self.dg(500, 300, GateType.AND)
            self.dg(700, 400, GateType.OR)
            self.cn(1, 8)
            self.cn(1, 12)
            self.cn(2, 9)
            self.cn(2, 13)
            self.cn(3, 17)
            self.cn(3, 21)
            self.cn(7, 16)
            self.cn(7, 20)
            self.cn(15, 4)
            self.cn(19, 24)
            self.cn(11, 25)
            self.cn(23, 5)
