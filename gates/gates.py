class Connector:
    def __init__(self, name, debug = False) -> None:
        self.targets = []
        self.state = None

        self.name = name
        self.debug = debug

    def connect(self, to) -> None:
        self.targets.append(to)

    def send(self, value) -> None:
        if self.state == value:
            return
        else:
            if self.debug:
                print("Connector now has value: " + str(value) + " compared to before: " + str(self.state))
                
            self.state = value

            for target in self.targets:
                target.trigger(value)
        

class Input:
    def __init__(self, name, parent, debug = False) -> None:
        self.value = None
        self.parent = parent

    def trigger(self, value) -> None: 
        if self.value == value:
            return
        else:
            self.value = value
            self.parent.evaluate()


class Gate:
    def __init__(self) -> None:
        self.A = Input('A', self)
        self.B = Input('B', self)

        self.Q = Connector('Q', debug=True)

    def evaluate(self) -> None:
        return

class Not_Gate:
    def __init__(self) -> None:
        self.A = Input('A', self)
        self.Q = Connector('Q')

    def evaluate(self) -> None:
        self.Q.send(not self.A.value)

class And_Gate(Gate):
    def __init__(self) -> None:
        super().__init__()

    def evaluate(self) -> None:
        self.Q.send(self.A.value and self.B.value)


class Or_Gate(Gate):
    def __init__(self) -> None:
        super().__init__()

    def evaluate(self) -> None:
        self.Q.send(self.A.value or self.B.value)


class Xor_Gate(Gate):
    def __init__(self) -> None:
        super().__init__()

    def evaluate(self) -> None:
        self.Q.send(self.A.value != self.B.value)


class Nor_Gate(Gate):
    def __init__(self) -> None:
        super().__init__()

    def evaluate(self) -> None:
        self.Q.send(not(self.A.value or self.B.value))


class Nand_Gate(Gate):
    def __init__(self) -> None:
        super().__init__()

    def evaluate(self) -> None:
        self.Q.send(not(self.A.value and self.B.value))