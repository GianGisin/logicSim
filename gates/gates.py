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
    pass

class Gate:
    pass