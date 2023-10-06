from enum import Enum
from abc import ABC, abstractmethod


class Connector:
    counter = 0

    def __init__(self, name, debug=False) -> None:
        self.targets = {}
        self.state = None

        self.name = name
        self.debug = debug

    def disconnect(self, key) -> bool:
        target = self.targets.get(key, False)
        if target:
            target.trigger(False)
            self.targets.pop(key)
            return True
        else:
            print("Target {key} not found in targets")
            return False

    def connect(self, to, key=False) -> None:
        if key:
            self.targets.update({key: to})
        else:
            self.targets.update({self.counter: to})
            self.counter += 1
        to.trigger(self.state)
        print(f"Q.targets: {self.targets}")

    def send(self, value) -> None:
        if self.state == value:
            return
        else:
            if self.debug:
                print(
                    "Connector now has value: "
                    + str(value)
                    + " compared to before: "
                    + str(self.state)
                )

            self.state = value

            for _, target in self.targets.items():
                target.trigger(value)


class Input:
    def __init__(self, name, parent, debug=False) -> None:
        self.value = False
        self.parent = parent
        self.name = name

    def trigger(self, value) -> None:
        if self.value == value:
            return
        else:
            self.value = value
            self.parent.evaluate()

    def __repr__(self) -> str:
        return f"Input {self.name}"


class Switch:
    def __init__(self, init_state=False) -> None:
        self.Q = Connector("Q", debug=True)
        self.Q.state = init_state

    def get_state(self):
        return self.Q.state

    def __repr__(self) -> str:
        return f"[Switch] connected to {self.Q.targets}"


class Lamp:
    def __init__(self, on_update=None, init_state=False) -> None:
        self.A = Input("lamp A", self)
        self.A.value = init_state
        self.func = on_update

    def evaluate(self) -> None:
        # temporary
        print(f"Lamp state is now {self.A.value}")
        # call function passed into constructor
        # check whether value has changed
        if self.A.value != None:
            self.func()

    def __repr__(self) -> str:
        return f"[Lamp] with state {self.A.value}"


class Gate(ABC):
    def __init__(self) -> None:
        self.A = Input("A", self)
        self.B = Input("B", self)

        self.Q = Connector("Q", debug=True)
        # evaluate on init
        self.evaluate()

    @abstractmethod
    def evaluate(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Gate connected to {self.Q.targets}"


class NotGate:
    def __init__(self) -> None:
        self.A = Input("A", self)
        self.Q = Connector("Q")
        self.evaluate()

    def evaluate(self) -> None:
        self.Q.send(not self.A.value)

    def __repr__(self) -> str:
        return f"Gate connected to {self.Q.targets}"


class AndGate(Gate):
    def __init__(self) -> None:
        super().__init__()

    def evaluate(self) -> None:
        self.Q.send(self.A.value and self.B.value)


class OrGate(Gate):
    def __init__(self) -> None:
        super().__init__()

    def evaluate(self) -> None:
        self.Q.send(self.A.value or self.B.value)


class XorGate(Gate):
    def __init__(self) -> None:
        super().__init__()

    def evaluate(self) -> None:
        self.Q.send(self.A.value != self.B.value)


class NorGate(Gate):
    def __init__(self) -> None:
        super().__init__()

    def evaluate(self) -> None:
        self.Q.send(not (self.A.value or self.B.value))


class XnorGate(Gate):
    def __init__(self) -> None:
        super().__init__()

    def evaluate(self) -> None:
        self.Q.send(not (self.A.value != self.B.value))


class NandGate(Gate):
    def __init__(self) -> None:
        super().__init__()

    def evaluate(self) -> None:
        self.Q.send(not (self.A.value and self.B.value))


class GateType(Enum):
    NOT = 0
    AND = 1
    OR = 2
    XOR = 3
    NAND = 4
    NOR = 5
    XNOR = 6


def gate_from_type(gate_type: GateType):
    match gate_type:
        case GateType.NOT:
            return NotGate()
        case GateType.AND:
            return AndGate()
        case GateType.OR:
            return OrGate()
        case GateType.XOR:
            return XorGate()
        case GateType.NAND:
            return NandGate()
        case GateType.NOR:
            return NorGate()
        case GateType.XNOR:
            return XnorGate()
