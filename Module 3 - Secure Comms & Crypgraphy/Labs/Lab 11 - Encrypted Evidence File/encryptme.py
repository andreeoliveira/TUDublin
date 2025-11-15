# This is the program we believe was used to encode the intercepted message.
# some of the retrieved program was damaged (show as &&&&)
# Can you use this to figure out how it was encoded and decode it? 
# Good Luck

import string
import random
from base64 import b64encode, b64decode

secret = '&&&&&&&&&&&&&&' # We don't know the original message or length

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

if __name__ == '__main__':
	# secret = b"\x00"*4 + b"\x01"*4 #secret 8 bytes long
	secret = b"helloboy" #secret 8 bytes long
	count = 3
	print(make_secret(secret, count=count)) #prints the encoded message




def decrypt_secret(encoded):
	print("Encoded message: ", encoded) #prints the encoded message
