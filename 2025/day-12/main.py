from dataclasses import dataclass
from os import getenv


@dataclass
class Plane:
    width: int
    height: int
    presents: list[int]

    @property
    def area(self) -> int:
        return self.width * self.height

    def fits(self, blocks) -> bool:
        return self.area >= sum(n * blocks[i] for i, n in enumerate(self.presents))


def count_blocks(shape) -> int:
    return sum(line.count("#") for line in shape)


with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    shapes = []
    planes = []
    current_shape = []
    for line in f:
        if not line.strip():
            continue
        elif line.strip()[-1] == ":":
            if current_shape:
                shapes.append(current_shape)
            current_shape = []
        elif "x" in line:
            parts = line.split(": ")
            width, height = [int(n) for n in parts[0].split("x")]
            presents = [int(n) for n in parts[1].split()]
            planes.append(Plane(width=width, height=height, presents=presents))
        else:
            current_shape.append(line.strip())
    shapes.append(current_shape)

blocks = [count_blocks(shape) for shape in shapes]

# NOTE: this doesn't give the correct anwser on example_input.txt
# because the input is not shaped the same way
print(sum(int(plane.fits(blocks)) for plane in planes))
