def process_marker(input):
    return process(input, 4)


def process_msg(input):
    return process(input, 14)


def process(input, n):
    i = 0
    while True:
        s = input[i : i + n]
        if len(set(s)) == len(s):
            return i + n
        i += 1


with open("input", "r") as file:
    input = file.read()
print(process_marker(input))
print(process_msg(input))
