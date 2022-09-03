import re

message = re.sub(r'\s', "", input("Message: ").upper())

key = re.sub(r'\s', "", input("Key: ").upper())

def encode(msg, key):
    output = ""
    offset = ord('A')
    for i in range(0, len(msg)):
        if re.search(r'[A-Z]', msg[i]):
            key_letter = key[i % len(key)]
            new_letter_code = offset + (ord(msg[i]) + ord(key_letter) - 2*offset) % 26
            output += chr(new_letter_code)
        else:
            output += msg[i]
    return output

print("------OUTPUT------")
print("key:", key)
print("message:", message)
print("encoded:", encode(message, key))