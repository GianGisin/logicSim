class Connector:
    def __init__(self, name, debug = False) -> None:
        self.targets = []
        self.state = None

        self.name = name
        self.debug = debug

    def connect(self, to) -> None:
        self.targets.append(to)

    def send(self, value: bool) -> None:
        if self.state == value:
            return
        else:
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

        self.Q = Connector('Q')

    def evaluate(self) -> None:
        return