from PIL import Image

#im = Image.open("line.png")
im = Image.open("vert.png")
#channel = 2
channel = 0
w,h = im.size
print w,h

y = h / 2

out_h = 100
out = Image.new("RGB", (w, out_h))

#https://en.wikipedia.org/wiki/Code_128
codes = {
	">" : "11011011000",
	"7": "11101101110",
	"a": ("10010110000"),
	"b": ("10010000110"),
	"c": ("10000101100"),
	"d": ("10000100110"),
	"e": ("10110010000"),
	"f": ("10110000100"),
	"g": ("10011010000"),
	"h": ("10011000010"),
	"i": ("10000110100"),
	"j": ("10000110010"),
	"k": ("11000010010"),
	"l": ("11001010000"),
	"m": ("11110111010"),
	"n": ("11000010100"),
	"o": ("10001111010"),
	"p": ("10100111100"),
	"q": ("10010111100"),
	"r": ("10010011110"),
	"s": ("10111100100"),
	"t": ("10011110100"),
	"u": ("10011110010"),
	"v": ("11110100100"),
	"w": ("11110010100"),
	"x": ("11110010010"),
	"y": ("11011011110"),
	"z": ("11011110110"),
		
	"StartA": ("11010000100"),
	"StartB": ("11010010000"),
	"StartC": ("11010011100"),
	"Stop": ("11000111010"),
	"RStop": ("11010111000"),
	"Stop Patt" : ("1100011101011"),
}

#11010011100 10110010000 11110010100 10011000010 10011110100 10011000010 10010011110 11000010010 10100111100 10001111010 11000010100 10110010000 10000110100 1
#start		e		w	h		t	h		r	k		p	o		n	e		i

#11010011100   
#      11010011100  10000110100
#vbits 00010011110  1000011010010000101100100011110101100001010010110010000100111101001001100001010010011110100101100001001001111011011011000110001110101

                    #11010011100
#vbits inverted 111011000010111100101101111010011011100001010011110101101001101111011000010110110011110101101100001011010011110110110000100100100111001110001010

bits = []
for x in xrange(w):
	pix = im.getpixel((x, y))
	if pix[channel] < 20:
		c = (255, 255, 255)
		b = "1"
	else:	
		c = (0, 0, 0)
		b = "0"
	
	if (x % 4 == 0):
		bits.append(b)	
	for yo in xrange(out_h):
		out.putpixel((w-x-1, yo), c)
		
	print pix
	
bits = "".join(bits)
print len(bits), bits
#bits = bits[::-1]

hbits = "110100111001011001000011110010100100110000101001111010010011000010100100111101100001001010100111100100011110101100001010010110010000100001101001"
vbits = "000100111101000011010010000101100100011110101100001010010110010000100111101001001100001010010011110100101100001001001111011011011000110001110101"
vbits_bar = "111011000010111100101101111010011011100001010011110101101001101111011000010110110011110101101100001011010011110110110000100100100111001110001010"
bits = hbits + vbits[1:]
#bits = vbits_bar[1:]
#bits = vbits
#print len(bits), bits
word = ""
while bits:
	found = None
	for name, val in codes.iteritems():
		if bits[:len(val)] == val:
			found = name
			bits = bits[len(val):]
			break
	if found:
		print "Found: ", found
		if len(found) == 1:
			word += found
	else:
		print "skipped:", bits[:11]
		bits = bits[11:]
#out.show()	

print "word = '%s' len=%d" % (word, len(word))

def caeser(cipher, d):
	def get_shift(d):
		while(True):
			yield d
			#yield(0)
			#yield(7)
			#yield(0)
			#yield(2)
		
	clear = ""
	shift = get_shift(d)
	for c in cipher:
		n = shift.next()
		ch = chr(((ord(c) - ord("a") + n) % 26) + ord("a"))
		clear += ch
	print clear, len(clear)

extra ="whkneehrr" 
for x in xrange(26):
	print x, caeser(extra, x+1)

"""   
#Horiz => ewhthrkponei   (12)
#Vert => iconethrar	 (10)

ewhthrkpo neiiconethrar
phonetic whrkeethrar ion


ewhthrkponeiriconethrar


ciphernotation whkerhr re

23 = 14 + 9

rotationcipher  + whkneehrr  
aaa#aakeyword##aa


1 C
2 D
3 E
4 F
5 G
6 A
7 B

7->B
2-D

???

aaa#aakeyword##aa

whhke
thephone + wirk?
entropi + whhke
hipower + thkne
in power + ehthk
interop +  ewhhk
herewith + kpon   kpon07herewith02

IP network + ehh

ip02network07
ip07network02
ehh07network02ip

powernet + hhki
#xxx##keyword###xx

ewh07thrkpone02

ewh07kipthorne02
ewh07kortiphen02
#11011001100
ewh07thrkponei02
3 FQ 5 YURIOLW 4 JBQ --
# Start A 11010000100
# Start B 11010010000
# Start C 11010011100
# Stop 11000111010
# Reverse Stop 11010111000
# Stop pattern 1100011101011


10000110100

Having 23 letters is the right path. The format of the passcode is  where a is a letter, # is a digit and keyword is a special word.

11011011000 11000111010 1
"""
