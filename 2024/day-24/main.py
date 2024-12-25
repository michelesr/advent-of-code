from os import getenv
from functools import cache
from copy import deepcopy
from typing import Optional

with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    lines = [line.strip() for line in f.readlines()]


class Circuit:
    def __init__(self):
        self.nodes: set[Node] = set()
        self.initial_nodes: set[Node] = set()
        self.gates: set[Gate] = set()

    def find_node_by_name(self, name) -> Optional["Node"]:
        for node in self.nodes:
            if node.name == name:
                return node

    def get_nodes_starting_with(self, s: str):
        return list(sorted([n for n in self.nodes if n.name.startswith(s)]))

    def get_all_nodes(self):
        return list(sorted(list(self.nodes)))

    def get_out_nodes(self):
        return self.get_nodes_starting_with("z")

    def process_gate(self, gate):
        match gate.op:
            case "XOR":
                gate.out.value = gate.in_a.value ^ gate.in_b.value
            case "OR":
                gate.out.value = gate.in_a.value | gate.in_b.value
            case "AND":
                gate.out.value = gate.in_a.value & gate.in_b.value
        for gate in self.find_gate_by_input(gate.out):
            self.process_gate(gate)

    @cache
    def find_gate_by_input(self, node: "Node"):
        res = set()
        for gate in self.gates:
            if gate.in_a == node or gate.in_b == node:
                res.add(gate)
        return res

    def find_gate_by_output(self, node: "Node"):
        res = set()
        for gate in self.gates:
            if gate.out == node:
                res.add(gate)
        return res

    def run_simulation(self):
        for node in self.initial_nodes:
            gates = self.find_gate_by_input(node)
            for gate in gates:
                self.process_gate(gate)

    def apply_fix(self, x, y):
        x = self.find_node_by_name(x)
        y = self.find_node_by_name(y)
        if not x or not y:
            raise ValueError("Cannot find node")
        a = self.find_gate_by_output(x).pop()
        b = self.find_gate_by_output(y).pop()
        a.out, b.out = b.out, a.out

    def view(self):
        import graphviz
        g = graphviz.Graph('G', filename='graph.gv')
        for node in self.initial_nodes:
            for gate in self.find_gate_by_input(self.find_node_by_name(node.name)):
                gate_s = str(id(gate))
                g.edge(node.name, gate_s, label=node.name)

        for gate in self.gates:
            gate_s = str(id(gate))
            g.node(gate_s, label=gate.op)

            for in_gate in self.find_gate_by_output(gate.in_a):
                in_gate_s = str(id(in_gate))
                g.edge(in_gate_s, gate_s, label=gate.in_a.name)

            for in_gate in self.find_gate_by_output(gate.in_b):
                in_gate_s = str(id(in_gate))
                g.edge(in_gate_s, gate_s, label=gate.in_b.name)

        for node in self.get_out_nodes():
            for gate in self.find_gate_by_output(node):
                gate_s = str(id(gate))
                g.edge(gate_s, gate.out.name, label=gate.out.name)
        g.view()


class Node:
    def __init__(self, name: str, value: int):
        self.value = value
        self.name = name

    def __repr__(self) -> str:
        return f"Node({self.name}: {self.value})"

    def __lt__(self, other):
        return self.name < other.name


class Gate:
    gates = set()

    def __init__(self, in_a: Node, in_b: Node, out: Node, op: str):
        self.in_a = in_a
        self.in_b = in_b
        self.out = out
        self.op = op

    def __repr__(self) -> str:
        return f"Gate({self.in_a} {self.op} {self.in_b} -> {self.out})"


circuit = Circuit()
for line in lines:
    if ":" in line:
        name, value = line.split(": ")
        node = Node(name, int(value))
        circuit.nodes.add(node)
        circuit.initial_nodes.add(node)
    elif "->" in line:
        line = line.replace("-> ", "")
        in_a, op, in_b, out = line.split(" ")

        out_node = circuit.find_node_by_name(out)
        if not out_node:
            out_node = Node(out, 0)
            circuit.nodes.add(out_node)

        in_a_node = circuit.find_node_by_name(in_a)
        if not in_a_node:
            in_a_node = Node(in_a, 0)
            circuit.nodes.add(in_a_node)

        in_b_node = circuit.find_node_by_name(in_b)
        if not in_b_node:
            in_b_node = Node(in_b, 0)
            circuit.nodes.add(in_b_node)

        circuit.gates.add(Gate(in_a_node, in_b_node, out_node, op))

old_circuit = deepcopy(circuit)

circuit.run_simulation()
bits = "".join(str(n.value) for n in circuit.get_out_nodes())[::-1]
print(int(bits, 2))

circuit = old_circuit

# I've looked at the input by eye, and noticed that there are 4 z nodes that
# are not getting input from a XOR: while that's fine for the last z node, the
# others should all be linked to a XOR so fixing those connections is 3 of 4
# pairs (at least in my input)
#
# Last one was trickier... but you could see that there were triples AND XOR OR
# (or mirrored OR XOR AND) on the same level and there was one level with OR
# AND XOR instead, and so the output of AND and XOR had to be switched
#
# If you came here trying to find a solution that runs on your input you'll be
# disappointed, but I preferred to solve this visually rather than programmatically,
# and it took a lot longer than I expected to be honest...
#
# Anyway, Merry Xmas :-)
fixes = [("z08", "thm"), ("z22", "hwq"), ("z29", "gbs"), ("wrm", "wss")]
for x, y in fixes:
    circuit.apply_fix(x, y)

# uncomment this to visualize with graphviz, you can try to add fixes and rerender
# to see if they make sense, and the final assert down there should pass when you got
# the 4 fixes right... (of course my fixes won't work for your input)
# circuit.view()

# check that the sum is ok
circuit.run_simulation()
c = "".join(str(n.value) for n in circuit.get_out_nodes())[::-1]
a = "".join(str(n.value) for n in circuit.get_nodes_starting_with("x"))[::-1]
b = "".join(str(n.value) for n in circuit.get_nodes_starting_with("y"))[::-1]
assert int(c, 2) == int(a, 2) + int(b, 2)

# print the fixed nodes
nodes_to_fix = []
for a, b in fixes:
    nodes_to_fix.append(a)
    nodes_to_fix.append(b)
nodes_to_fix.sort()
print(",".join(nodes_to_fix))
