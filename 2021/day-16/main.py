from os import getenv


def hex_to_bin(hex_string):
    return bin(int(hex_string, 16))[2:].zfill(len(hex_string) * 4)


def parse_packet(binary_string, index):
    # Read the version (3 bits)
    version = int(binary_string[index : index + 3], 2)
    index += 3

    # Read the type ID (3 bits)
    type_id = int(binary_string[index : index + 3], 2)
    index += 3

    # Initialize the version sum with the current packet's version
    version_sum = version
    value = None

    if type_id == 4:
        # Literal value packet
        literal_value = ""
        while True:
            # Read the next 5 bits
            group = binary_string[index : index + 5]
            index += 5
            literal_value += group[1:]  # Append the last 4 bits
            if group[0] == "0":  # Last group
                break
        value = int(
            literal_value, 2
        )  # Convert the literal value from binary to decimal
    else:
        # Operator packet
        length_type_id = binary_string[index]
        index += 1

        sub_values = []

        if length_type_id == "0":
            # Next 15 bits are the total length of the sub-packets
            total_length = int(binary_string[index : index + 15], 2)
            index += 15
            end_index = index + total_length

            while index < end_index:
                sub_version_sum, sub_value, index = parse_packet(binary_string, index)
                version_sum += sub_version_sum
                sub_values.append(sub_value)
        else:
            # Next 11 bits are the number of sub-packets
            number_of_sub_packets = int(binary_string[index : index + 11], 2)
            index += 11

            for _ in range(number_of_sub_packets):
                sub_version_sum, sub_value, index = parse_packet(binary_string, index)
                version_sum += sub_version_sum
                sub_values.append(sub_value)

        # Calculate the value based on the type ID
        if type_id == 0:  # Sum
            value = sum(sub_values)
        elif type_id == 1:  # Product
            value = 1
            for v in sub_values:
                value *= v
        elif type_id == 2:  # Minimum
            value = min(sub_values)
        elif type_id == 3:  # Maximum
            value = max(sub_values)
        elif type_id == 5:  # Greater than
            value = 1 if sub_values[0] > sub_values[1] else 0
        elif type_id == 6:  # Less than
            value = 1 if sub_values[0] < sub_values[1] else 0
        elif type_id == 7:  # Equal to
            value = 1 if sub_values[0] == sub_values[1] else 0

    return version_sum, value, index


def solve(hex_string):
    binary_string = hex_to_bin(hex_string)
    version_sum, value, _ = parse_packet(binary_string, 0)
    return version_sum, value


with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    hex_input = f.read().strip()

version_sum, value = solve(hex_input)
print(version_sum)
print(value)
