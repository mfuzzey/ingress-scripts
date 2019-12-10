from PIL import Image

im = Image.open("forum.png")

w,h = im.size
print w,h

y = h / 2

out_h = 100
out = Image.new("RGB", (w, out_h))

for x in xrange(w):
	pix = im.getpixel((x, y))
	if pix[2] < 20:
		c = (255, 255, 255)
	else:	
		c = (0, 0, 0)
		
	for yo in xrange(out_h):
		out.putpixel((w-x-1, yo), c)
		
	#print pix
	
	
out.show()	
