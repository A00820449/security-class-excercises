import re

def encode(msg, key):
    output = []
    msg_ints = list(map(ord, msg))
    key_ints = list(map(ord, key))
    for i in range(0, len(msg_ints)):
        output.append(msg_ints[i] ^ key_ints[i % len(key_ints)])
    return output

def print_binaries(arr, end='\n'):
    if len(arr) > 0:
        print("{:b}".format(arr[0]), end='')
    for i in range(1, len(arr)):
        print("{:b} ".format(arr[i]), end='')
    print("", end=end)

def print_printable_chars(arr, end='\n'):
    output = ""
    for i in arr:
        if i >= ord(' ') and i <= ord('~'):
            output += chr(i)
        else:
            output += "·"
    print(output, end=end)

def main():
    key = re.sub(r'\s', "", input("Key? ").upper())
    msg = re.sub(r'\s', "", input("Message? ").upper())
    encoded = encode(msg, key)

    print("------OUTPUT------")
    print("Key:", key)
    print("Message:", msg)
    print("Encoded binary: ", end="")
    print_binaries(encoded)
    print("In readable characters: ", end='')
    print_printable_chars(encoded)

if __name__ == "__main__":
    main()
