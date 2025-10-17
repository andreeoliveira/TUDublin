#!/usr/bin/env python
# coding: utf-8

# In[23]:


from PIL import Image
import math

input_file = "/tmp/aes.bmp.enc"
# Read the entire file as binary data
with open(input_file, 'rb') as f:
    bmp_bytes = f.read()

#header size as per challenge hint 
header_size = 14 
#Skipping header and getting only the bitmap body
bmp_body = bmp_bytes[header_size:]

# Creating 16-byte blocks
block_size = 16
blocks = []
for i in range(0, len(bmp_body), block_size):
    block = bmp_body[i:i+block_size]
    blocks.append(block)

total_blocks = len(blocks)

# redefining image size
side_length = int(math.sqrt(total_blocks))
width = side_length
height = side_length

img = Image.new('RGB', (width, height))

#iterating over the blocks and assigning a grayscale color
for i, block in enumerate(blocks):
    # Calculate pixel position
    x = i % width
    #BMP files store image data bottom-to-top
    y = height - 1 - (i // width)
    color = (block[0], block[0], block[0])
    img.putpixel((x, y), color)

output_file = "/tmp/scrambled_flag.png"
img.save(output_file)
print(f"Saved as: {output_file}")


# In[ ]:





# In[ ]:




