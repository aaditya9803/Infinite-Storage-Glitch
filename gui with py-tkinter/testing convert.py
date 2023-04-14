import numpy as np
with open('power.png', 'rb') as file:
    binary_data = file.read()
binary_array = np.unpackbits(np.array(bytearray(binary_data), dtype=np.uint8))
np.save('binary_array.npy', binary_array)
