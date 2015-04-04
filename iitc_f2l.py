import sys
import unittest

# Convert IITC draw tools fields to lines
KEY_ORDERS = (("type", "latLng", "latLngs", "color"), ("lat", "lng"))

def normalize(objs):
	# II2C seems to want keys in a specific order...
	def normalize_one(obj):
		out = []
		for order in KEY_ORDERS:
			if order[0] in obj:
				parts = []
				for k in order:
					val = obj.get(k)
					if val is None:
						continue
					if type(val) is str:
						val = '"%s"' % val
					if type(val) is list:
						val = normalize(val)
					if type(val) is dict:
						val = normalize_one(val)
					parts.append('"%s":%s' % (k, val))
						
				out.append("{%s}" % ",".join(parts))
		return ",".join(out)		
		
	out = []
	for obj in objs:
		out.append(normalize_one(obj))
				
	return "[%s]" % ",".join(out)

	
def f2l(src):
	def buildLink(a, b, color):
		return {"type" : "polyline", "latLngs": [a, b], "color":color}
		
	dest = []
	for obj in eval(src):
		if obj["type"] == "polygon":
			vertices = obj["latLngs"]
			color = obj["color"]
			dest.append(buildLink(vertices[0], vertices[1], color))
			dest.append(buildLink(vertices[0], vertices[2], color))
			dest.append(buildLink(vertices[1], vertices[2], color))
		else:
			dest.append(obj)
	return normalize(dest)
	

class Autotest(unittest.TestCase):
	def test01_alreadyLine(self):
		alreadyOk = '[{"type":"polyline","latLngs":[{"lat":47.264051,"lng":6.052921},{"lat":47.761173,"lng":7.294874}],"color":"#a24ac3"},{"type":"polyline","latLngs":[{"lat":47.761173,"lng":7.294874},{"lat":48.461385,"lng":6.320278}],"color":"#a24ac3"}]'
		self.assertEquals(f2l(alreadyOk), alreadyOk)

	def test02_reorderLine(self):
		inp = '[{"latLngs":[{"lat":47.264051,"lng":6.052921},{"lat":47.761173,"lng":7.294874}],"color":"#a24ac3", "type":"polyline"},{"type":"polyline","latLngs":[{"lng":7.294874, "lat":47.761173},{"lat":48.461385,"lng":6.320278}],"color":"#a24ac3"}]'
		exp = '[{"type":"polyline","latLngs":[{"lat":47.264051,"lng":6.052921},{"lat":47.761173,"lng":7.294874}],"color":"#a24ac3"},{"type":"polyline","latLngs":[{"lat":47.761173,"lng":7.294874},{"lat":48.461385,"lng":6.320278}],"color":"#a24ac3"}]'
		self.assertEquals(f2l(inp), exp)

	def test03_fieldToLink(self):
		inp = '[{"type":"polygon","latLngs":[{"lat":47.264051,"lng":6.052921},{"lat":47.761173,"lng":7.294874},{"lat":48.461385,"lng":6.320278}],"color":"#a24ac3"}]'
		exp ='[{"type":"polyline","latLngs":[{"lat":47.264051,"lng":6.052921},{"lat":47.761173,"lng":7.294874}],"color":"#a24ac3"},{"type":"polyline","latLngs":[{"lat":47.264051,"lng":6.052921},{"lat":48.461385,"lng":6.320278}],"color":"#a24ac3"},{"type":"polyline","latLngs":[{"lat":47.761173,"lng":7.294874},{"lat":48.461385,"lng":6.320278}],"color":"#a24ac3"}]'
		self.assertEquals(f2l(inp), exp)

	def test04_marker(self):
		inp = '[{"type":"marker","latLng":{"lat":49.601164,"lng":7.376891},"color":"#c34a6f"}]'
		exp = '[{"type":"marker","latLng":{"lat":49.601164,"lng":7.376891},"color":"#c34a6f"}]'
		self.assertEquals(f2l(inp), exp)


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Test Mode  (please supply input file for real mode"
		unittest.main()
	
	inp = open(sys.argv[1], "rt").read()
	res = f2l(inp)
	if len(sys.argv) > 2:
		outfile = sys.argv[2]
		out = open(outfile, "wt")
		out.write(res)
		print "Written result to %s" % outfile
	else:
		print res

