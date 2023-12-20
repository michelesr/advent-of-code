from sys import argv
from queue import Queue

from enum import Enum


class Pulse(Enum):
    LOW = False
    HIGH = True


class FlifFlopState(Enum):
    ON = True
    OFF = False


class ModuleType(Enum):
    BROADCASTER = "broadcaster"
    FLIP_FLOP = "%"
    CONJUNCTION = "&"
    UNTYPED = None


class Module:
    module_type: ModuleType
    name: str
    outputs: list[str]

    def __init__(self, module_type: ModuleType, name: str, outputs: list[str]):
        self.module_type = module_type
        self.name = name
        self.outputs = outputs

    def propagate(self, input: str, pulse: Pulse, queue: Queue):
        pass


class FlifFlopModule(Module):
    state = FlifFlopState.OFF

    def propagate(self, input: str, pulse: Pulse, queue: Queue):
        if pulse == Pulse.HIGH:
            return
        else:
            self.state = FlifFlopState(not self.state.value)

        if self.state == FlifFlopState.ON:
            pulse = Pulse.HIGH
        else:
            pulse = Pulse.LOW

        for out in self.outputs:
            queue.put((pulse, self.name, out))


class ConjuctionModule(Module):
    inputs: dict[str, Pulse]

    def __init__(self, module_type: ModuleType, name: str, outputs: list[str]):
        self.inputs = {}
        super().__init__(module_type, name, outputs)

    def init_inputs(self, modules: dict[str, Module]):
        for name, module in modules.items():
            if self.name in module.outputs:
                self.inputs[name] = Pulse.LOW

    def propagate(self, input: str, pulse: Pulse, queue: Queue):
        self.inputs[input] = pulse
        if all([i.value for i in self.inputs.values()]):
            pulse = Pulse.LOW
        else:
            pulse = Pulse.HIGH

        for out in self.outputs:
            queue.put((pulse, self.name, out))


class Broadcaster(Module):
    def propagate(self, input: str, pulse: Pulse, queue: Queue):
        for out in self.outputs:
            queue.put((pulse, self.name, out))


with open(argv[1]) as f:
    lines = [line.strip() for line in f.readlines()]

modules = {}

for line in lines:
    name, out = line.split(" -> ")
    out = out.split(", ")
    if name == ModuleType.BROADCASTER.value:
        modules[name] = Broadcaster(ModuleType.BROADCASTER, name, out)

    elif ModuleType.FLIP_FLOP.value in name:
        name = name[1:]
        modules[name] = FlifFlopModule(ModuleType.FLIP_FLOP, name, out)
    elif ModuleType.CONJUNCTION.value in name:
        name = name[1:]
        modules[name] = ConjuctionModule(ModuleType.CONJUNCTION, name, out)

for x in [m for m in modules.values() if m.module_type == ModuleType.CONJUNCTION]:
    x.init_inputs(modules)


def press_button(modules: dict[str, Module]) -> tuple[int, int]:
    low_pulses_n = 0
    high_pulses_n = 0
    pulses = Queue()
    pulses.put((Pulse.LOW, "button", "broadcaster"))
    while not pulses.empty():
        pulse, src, dest = pulses.get()

        if pulse == Pulse.LOW:
            low_pulses_n += 1
        elif pulse == Pulse.HIGH:
            high_pulses_n += 1
        else:
            raise ValueError("Invalid pulse type")

        if dest in modules:
            modules[dest].propagate(src, pulse, pulses)
    return (low_pulses_n, high_pulses_n)


pulses = Queue()

# press the button
res = [0, 0]
for i in range(1000):
    a, b = press_button(modules)
    res[0] += a
    res[1] += b

print(res[0] * res[1])
