import re
import numpy as np

columns = int(input("Size of grid? "))
key = re.sub(r'\s', "", input("Key? (No repeating letters supported) ").upper())
msg = re.sub(r'\s', "", input("Message? ").upper())


mat_data = [[]]

orphaned = len(msg) % columns
if orphaned > 0:
    for i in range(0, columns - orphaned):
        pad_letter = ord('A') + (i % 26)
        msg += chr(pad_letter)

print("\nGrid size:", columns)
print("Key:", key)
print("Message:", msg)

keys = list(map(ord, key))
sorted_keys = sorted(keys)

i = 0
j = 0
for letter_index in range(0, len(msg)):
    #print("i: {}, j: {}".format(i,j))
    if j >= columns:
        j = 0
        i += 1
        mat_data.append([])
    mat_data[i].append(msg[letter_index])
    j += 1

mat = np.array(mat_data)

outout = ""
for n in sorted_keys:
    column = keys.index(n)
    if column < columns:
        for letter in mat[:,column]:
            if letter != "x":
                outout += letter

print("Encoded:", outout)