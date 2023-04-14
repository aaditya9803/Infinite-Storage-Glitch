import heapq
import collections

# Step 1: Read in the binary data
with open('binary_array.npy', 'rb') as f:
    data = f.read()
bits = ''.join(bin(byte)[2:].zfill(8) for byte in data)

# Step 2: Count the frequency of each bit
freq = collections.Counter(bits)

# Step 3: Build a Huffman tree
heap = [[f, [b, '']] for b, f in freq.items()]
heapq.heapify(heap)
while len(heap) > 1:
    lo = heapq.heappop(heap)
    hi = heapq.heappop(heap)
    for pair in lo[1:]:
        pair[1] = '0' + pair[1]
    for pair in hi[1:]:
        pair[1] = '1' + pair[1]
    heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    
# Step 4: Generate Huffman codes
codes = dict(heap[0][1:])

# Step 5: Encode the binary data
encoded = ''.join(codes[b] for b in bits)

# Step 6: Output the Huffman-encoded data and metadata
with open('compressed.bin', 'wb') as f:
    # Write original length of the binary data (needed for decoding)
    f.write(len(bits).to_bytes(4, byteorder='big'))
    
    # Write Huffman tree structure (needed for decoding)
    for b, code in sorted(codes.items()):
        f.write(ord(b).to_bytes(1, byteorder='big'))
        f.write(len(code).to_bytes(1, byteorder='big'))
        f.write(int(code, 2).to_bytes((len(code) + 7) // 8, byteorder='big'))

    # Write Huffman-encoded data
    while len(encoded) % 8 != 0:
        encoded += '0'
    f.write(int(encoded, 2).to_bytes(len(encoded) // 8, byteorder='big'))
