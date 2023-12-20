from sys import argv
from queue import Queue
from copy import deepcopy
from math import lcm

from enum import Enum
from typing import Optional


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


class Module:
    module_type: ModuleType
    name: str
    outputs: list[str]

    def __init__(self, module_type: ModuleType, name: str, outputs: list[str]):
        self.module_type = module_type
        self.name = name
        self.outputs = outputs

    def propagate(self, input: str, pulse: Pulse, queue: Queue):
        for out in self.outputs:
            queue.put((pulse, self.name, out))


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

        super().propagate(input, pulse, queue)


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

        super().propagate(input, pulse, queue)


def press_button(
    modules: dict[str, Module], track: Optional[str] = None
) -> tuple[int, int, bool]:
    low_pulses_n = 0
    high_pulses_n = 0
    found = False
    pulses = Queue()
    pulses.put((Pulse.LOW, "button", "broadcaster"))
    while not pulses.empty():
        pulse, src, dest = pulses.get()

        if track and pulse == Pulse.LOW and src == track:
            found = True

        if pulse == Pulse.LOW:
            low_pulses_n += 1
        elif pulse == Pulse.HIGH:
            high_pulses_n += 1
        else:
            raise ValueError("Invalid pulse type")

        if dest in modules:
            modules[dest].propagate(src, pulse, pulses)
    return (low_pulses_n, high_pulses_n, found)


def find_period(modules: dict[str, Module], src: str) -> int:
    modules = deepcopy(modules)
    i = 0
    while True:
        i += 1
        _, _, found = press_button(modules, src)
        if found:
            return i


def verify_path(path: list[str], graph: dict[str, list[str]]) -> bool:
    current = path[0]
    for node in path[1:]:
        if node not in graph[current]:
            return False
        current = node
    return True


with open(argv[1]) as f:
    lines = [line.strip() for line in f.readlines()]

modules = {}

for line in lines:
    name, out = line.split(" -> ")
    out = out.split(", ")
    if name == ModuleType.BROADCASTER.value:
        modules[name] = Module(ModuleType.BROADCASTER, name, out)

    elif ModuleType.FLIP_FLOP.value in name:
        name = name[1:]
        modules[name] = FlifFlopModule(ModuleType.FLIP_FLOP, name, out)
    elif ModuleType.CONJUNCTION.value in name:
        name = name[1:]
        modules[name] = ConjuctionModule(ModuleType.CONJUNCTION, name, out)

for x in [m for m in modules.values() if m.module_type == ModuleType.CONJUNCTION]:
    x.init_inputs(modules)

old_modules = deepcopy(modules)
pulses = Queue()

res = [0, 0]
for i in range(1000):
    a, b, _ = press_button(modules)
    res[0] += a
    res[1] += b
print(res[0] * res[1])

# visualization using graphviz: helpful to understand the problem
#
# import graphviz
# g = graphviz.Graph('G', filename='out.gv')
# for k, v in modules.items():
#     for out in v.outputs:
#         g.edge(k, out)
#
# g.view()

# these paths leads to xn and so rx
paths = [
    ["pk", "gp", "xf"],
    ["vk", "fb", "fz"],
    ["km", "jl", "mp"],
    ["xt", "jn", "hn"],
]

# verify them and abort it the paths are not correct
graph = {k: v.outputs for k, v in modules.items()}
assert all([verify_path(path, graph) for path in paths])

# rx needs a LOW signal from xn
# xn needs (xf, fz, mp, hn) to be all HIGH to send LOW to rx
# (xf, fz, mp, hn) are inverter modules so they need to receive LOW from (gp, fb, jl, jn) to send HIGH
#
# find_period() will be used to find the period (in number of cycles) when these component receive LOW

modules = old_modules
sources = ("gp", "fb", "jl", "jn")

# the lcm of all periods is the number of cycles when they all receive LOW
# and so they send HIGH to the xn component that sends LOW to rx
print(lcm(*[find_period(modules, src) for src in sources]))
