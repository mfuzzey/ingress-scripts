import argparse
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

	
def f2l(src, args):
	def buildLink(a, b, color):
		return {"type" : "polyline", "latLngs": [a, b], "color":color}
		
	skipTypes = []
	if args.remove_markers:
		skipTypes.append("marker")
		
	dest = []
	for obj in eval(src):
		objType = obj["type"]
		if objType in skipTypes:
			continue
			
		if objType == "polygon":
			vertices = obj["latLngs"]
			color = obj["color"]
			dest.append(buildLink(vertices[0], vertices[1], color))
			dest.append(buildLink(vertices[0], vertices[2], color))
			dest.append(buildLink(vertices[1], vertices[2], color))
		else:
			dest.append(obj)
	return normalize(dest)
	

def buildOptionParser():
	parser = argparse.ArgumentParser()
	parser.add_argument("--no-markers", dest="remove_markers", action="store_true", help="remove any markers")
	return parser


class Autotest(unittest.TestCase):
	def test01_alreadyLine(self):
		alreadyOk = '[{"type":"polyline","latLngs":[{"lat":47.264051,"lng":6.052921},{"lat":47.761173,"lng":7.294874}],"color":"#a24ac3"},{"type":"polyline","latLngs":[{"lat":47.761173,"lng":7.294874},{"lat":48.461385,"lng":6.320278}],"color":"#a24ac3"}]'
		self.assertEquals(f2l(alreadyOk, self._mkArgs()), alreadyOk)

	def test02_reorderLine(self):
		inp = '[{"latLngs":[{"lat":47.264051,"lng":6.052921},{"lat":47.761173,"lng":7.294874}],"color":"#a24ac3", "type":"polyline"},{"type":"polyline","latLngs":[{"lng":7.294874, "lat":47.761173},{"lat":48.461385,"lng":6.320278}],"color":"#a24ac3"}]'
		exp = '[{"type":"polyline","latLngs":[{"lat":47.264051,"lng":6.052921},{"lat":47.761173,"lng":7.294874}],"color":"#a24ac3"},{"type":"polyline","latLngs":[{"lat":47.761173,"lng":7.294874},{"lat":48.461385,"lng":6.320278}],"color":"#a24ac3"}]'
		self.assertEquals(f2l(inp, self._mkArgs()), exp)

	def test03_fieldToLink(self):
		inp = '[{"type":"polygon","latLngs":[{"lat":47.264051,"lng":6.052921},{"lat":47.761173,"lng":7.294874},{"lat":48.461385,"lng":6.320278}],"color":"#a24ac3"}]'
		exp ='[{"type":"polyline","latLngs":[{"lat":47.264051,"lng":6.052921},{"lat":47.761173,"lng":7.294874}],"color":"#a24ac3"},{"type":"polyline","latLngs":[{"lat":47.264051,"lng":6.052921},{"lat":48.461385,"lng":6.320278}],"color":"#a24ac3"},{"type":"polyline","latLngs":[{"lat":47.761173,"lng":7.294874},{"lat":48.461385,"lng":6.320278}],"color":"#a24ac3"}]'
		self.assertEquals(f2l(inp, self._mkArgs()), exp)

	def test04_marker(self):
		inp = '[{"type":"marker","latLng":{"lat":49.601164,"lng":7.376891},"color":"#c34a6f"}]'
		exp = '[{"type":"marker","latLng":{"lat":49.601164,"lng":7.376891},"color":"#c34a6f"}]'
		self.assertEquals(f2l(inp, self._mkArgs()), exp)

	def test05_removeMarker(self):
		inp = '[{"type":"marker","latLng":{"lat":49.601164,"lng":7.376891},"color":"#c34a6f"},{"type":"polyline","latLngs":[{"lat":47.264051,"lng":6.052921},{"lat":47.761173,"lng":7.294874}],"color":"#a24ac3"},{"type":"polyline","latLngs":[{"lat":47.761173,"lng":7.294874},{"lat":48.461385,"lng":6.320278}],"color":"#a24ac3"}]'
		exp = '[{"type":"polyline","latLngs":[{"lat":47.264051,"lng":6.052921},{"lat":47.761173,"lng":7.294874}],"color":"#a24ac3"},{"type":"polyline","latLngs":[{"lat":47.761173,"lng":7.294874},{"lat":48.461385,"lng":6.320278}],"color":"#a24ac3"}]'
		self.assertEquals(f2l(inp, self._mkArgs("--no-markers")), exp)

	def _mkArgs(self, options=""):
		parser = buildOptionParser()
		return parser.parse_args(options.split())

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Test Mode  (please supply input file for real mode"
		unittest.main()
		
	parser = buildOptionParser()	
	parser.add_argument("infile", type=argparse.FileType("rt"), help="Input file in IITC format")
	parser.add_argument("outfile", type=argparse.FileType("wt"), nargs="?", default="-", help="Output file")
	
	args = parser.parse_args()

	res = f2l(args.infile.read(), args)
	args.outfile.write(res)

