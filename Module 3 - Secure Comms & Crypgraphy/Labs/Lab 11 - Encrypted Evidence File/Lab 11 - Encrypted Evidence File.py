#!/usr/bin/env python
# coding: utf-8

# # Lab 11 - Encrypted Evidence File

# In[59]:


import string
from base64 import b64encode, b64decode

secret_encoding = ['step1', 'step2', 'step3']

def step1(s):
	_step1 = str.maketrans("zyxwvutsrqponZYXWVUTSRQPONmlkjihgfedcbaMLKJIHGFEDCBA","mlkjihgfedcbaMLKJIHGFEDCBAzyxwvutsrqponZYXWVUTSRQPON")	# creates a translation table for the shifted alphabet
	translated = s.translate(_step1)
	print("Translated message: ", translated) #prints the translated message
	return translated #returns the translated message

def step2(s): return b64encode(bytes(s, 'utf-8'))

def step3(plaintext, shift=4):
	loweralpha = string.ascii_lowercase #lowercase alphabet
	print("Lowercase alphabet: ", loweralpha) #prints the lowercase alphabet
	shifted_string = loweralpha[shift:] + loweralpha[:shift] #shifted alphabet by 4 positions
	print("Shifted string: ", shifted_string) #prints the shifted string
	converted = str.maketrans(loweralpha, shifted_string) # creates a translation table for the shifted alphabet
	print("Translation table: ", converted) #prints the translation table
	translated = plaintext.translate(converted)
	print("Translated message: ", translated) #prints the translated message
	return translated # translates the message using the translation table

def make_secret(plain, count):
	print(f"Plain message: {plain} and count: {count}") #prints the plain message and count
	a = '2{}'.format(b64encode(plain).decode('utf-8')) #b64encode returns a bytes object, so we need to convert it to a string
	print("b64encode message: ", a) #prints the encoded message
	for count in range(count):
		print("=" * 60) #prints a line of 60 equal signs
		print(f"Iteration {count+1}") #prints the iteration number
		r = random.choice(secret_encoding) #chooses a random encoding step
		print("Random encoding step: ", r) #prints the random encoding step
		si = secret_encoding.index(r) + 1 #index of the encoding step
		print("Index of encoding step: ", si) #prints the index of the encoding step
		_a = globals()[r](a) #applies the encoding step to the message
		if isinstance(_a, bytes):
			_a = _a.decode('utf-8')
		print("Encoded message: ", _a) #prints the encoded message
		a = '{}{}'.format(si, _a) #concatenates the index and the encoded message
		print("Encoded message: ", a) #prints the encoded message
	return a #returns the encoded message

import string
from base64 import b64encode, b64decode

secret_decoding = ['decode_step1', 'decode_step2', 'decode_step3']

def decode_step1(s):
	_step1 = str.maketrans("mlkjihgfedcbaMLKJIHGFEDCBAzyxwvutsrqponZYXWVUTSRQPON", "zyxwvutsrqponZYXWVUTSRQPONmlkjihgfedcbaMLKJIHGFEDCBA")	# creates a translation table for the shifted alphabet
	translated = s.translate(_step1)
	return translated #returns the translated message

def decode_step2(s):
    if isinstance(s, bytes):
        raw = s
    else:
        raw = str(s).encode("utf-8")
    decoded_bytes = b64decode(raw)
    return decoded_bytes.decode("latin-1")  # safe decode

def decode_step3(plaintext, shift=4):
    if isinstance(plaintext, bytes):
        plaintext = plaintext.decode("utf-8")  # convert bytes to string

    loweralpha = string.ascii_lowercase
    shifted_string = loweralpha[(len(loweralpha) - shift):] + loweralpha[:(len(loweralpha) - shift)]
    converted = str.maketrans(loweralpha, shifted_string)
    translated = plaintext.translate(converted)
    return translated


def decode(enc):
    if isinstance(enc, bytes):
        enc = enc.decode("utf-8")
    while True:
        if not enc or enc[0] not in "123":
            print(f"Secret Decripted: {enc}")
            break
        step_index = int(enc[:1]) - 1
        enc = enc[1:]
        step = secret_decoding[step_index]
        enc = globals()[step](enc)

with open("/tmp/intercepted.txt", "r", encoding="utf-8") as f:
    encrypted_secret = f.read().strip() 
decode(encrypted_secret)


# In[ ]:




