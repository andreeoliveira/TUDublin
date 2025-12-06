#!/usr/bin/env python3
"""
LFSR PNG Decoder
Decrypts an encrypted PNG file by brute-forcing two LFSR seeds.
"""

INPUT_FILE = "flag.enc"
OUTPUT_FILE = "flag_decrypted.png"

PNG_HEADER_BYTES = bytes([0x89, 0x50, 0x4E, 0x47])

# Extract tap positions from mask
def extract_taps(length, mask):
    taps = []
    for x in range(length):
        if (mask >> x) & 1 == 1:
            taps.append(x)
    return taps

# Get encrypted PNG
def get_encrypted_png(filename):
    with open(filename, 'rb') as f:
        return f.read()


l1, m1 = 12, 0b010000100000  # 12-bit: Taps at positions 2 and 7
l2, m2 = 19, 0b0000100000100000000  # 19-bit: Taps at positions 5 and 11

enc = get_encrypted_png(INPUT_FILE)
length = len(enc)

taps1 = extract_taps(l1, m1)
taps2 = extract_taps(l2, m2)
tap1_0, tap1_1 = taps1[0], taps1[1]
tap2_0, tap2_1 = taps2[0], taps2[1]
len1_minus_1 = l1 - 1
len2_minus_1 = l2 - 1

max_i = 1 << l1
max_j = 1 << l2

for i in range(tap1_0, max_i):
    if i % 1000 == 0:
        print(f"Trying r1 seed: {i}/{max_i}", end='', flush=True)
    
    for j in range(tap2_0, max_j):
        v1, v2 = i, j
        bytes_out = bytearray()
        
        for level in range(length):
            res = 0
            for k in range(8):
                xor1 = ((v1 >> tap1_0) ^ (v1 >> tap1_1)) & 1
                v1 = (v1 >> 1) ^ (xor1 << len1_minus_1)
                bit1 = v1 & 1
                
                xor2 = ((v2 >> tap2_0) ^ (v2 >> tap2_1)) & 1
                v2 = (v2 >> 1) ^ (xor2 << len2_minus_1)
                bit2 = v2 & 1
                
                res += (1 << k) * (bit1 + bit2)
            
            value = (res % 255) & 0xFF
            
            if level < 4:
                if value ^ enc[level] != PNG_HEADER_BYTES[level]:
                    break
            
            if level == 3:
                bytes_out.extend(PNG_HEADER_BYTES)
            
            if level > 3:
                bytes_out.append(value ^ enc[level])
        else:
            if len(bytes_out) >= 4:
                print(f"\n[+] SUCCESS! Found seeds: r1 seed: {i} and r2 seed: {j}")
                with open(OUTPUT_FILE, 'wb') as f:
                    f.write(bytes(bytes_out))
                
                print(f"Decrypted PNG saved to: {OUTPUT_FILE}")
                exit(0)

print("Could not find correct seeds.")