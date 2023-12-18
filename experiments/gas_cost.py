def count_zero_bytes(data):
    count = 0
    for i in range(0, len(data), 2):
        byte = data[i:i+2]
        if byte == "00":
            count += 1
    return count


def compute_gas_cost(calldata):
    zero_bytes = count_zero_bytes(calldata)
    non_zero_bytes = (len(calldata)/2) - zero_bytes
    return 16 * non_zero_bytes + 4 * zero_bytes
