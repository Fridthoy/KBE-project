
# ManufReqServer, ver. 200130 v3

from http.server import BaseHTTPRequestHandler, HTTPServer
import requests

HOST_NAME = '127.0.0.1' 
PORT_NUMBER = 4321 # Maybe set this to 1234


class MyHandler(BaseHTTPRequestHandler):
	
	def do_HEAD(s):
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()
	def do_GET(s):
		# https://stackoverflow.com/questions/26563403/variables-not-updated-from-within-basehttpserver-class
		"""Respond to a GET request."""
		
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()
		
		# Check what is the path
		path = s.path
		if path.find("/process") != -1:
			s.wfile.write(bytes('<html><body><h2>Process limits</h2><form action="http://127.0.0.1:4321/setLimits" method="post">', "utf-8"))
			s.wfile.write(bytes('<br>Maximum Length of Legs:<br><input type="text" name="leg_length_min" value="0">', "utf-8"))
			s.wfile.write(bytes('<br>Minimum Length of Legs:<br><input type="text" name="leg_length_max" value="0">', "utf-8"))
			s.wfile.write(bytes('<br>Maximum sidelength of legs:<br><input type="text" name="leg_side_min" value="0">', "utf-8"))
			s.wfile.write(bytes('<br>Minimum sidelength of legs:<br><input type="text" name="leg_side_max" value="0">', "utf-8"))
			s.wfile.write(bytes('<br>Maximum Seat length:<br><input type="text" name="seat_length_min" value="0">', "utf-8"))
			s.wfile.write(bytes('<br>Minimum Seat length:<br><input type="text" name="seat_length_max" value="0">', "utf-8"))
			s.wfile.write(bytes('<br>Maximum Seat Width:<br><input type="text" name="seat_width_min" value="0">', "utf-8"))
			s.wfile.write(bytes('<br>Minimum Seat Width:<br><input type="text" name="seat_width_max" value="0">', "utf-8"))
			s.wfile.write(bytes('<br>Maximum Height of Back:<br><input type="text" name="height_backplate_min">', "utf-8"))
			s.wfile.write(bytes('<br>Minimum Height of Back:<br><input type="text" name="height_backplate_max">', "utf-8"))
			s.wfile.write(bytes('<br><br><input type="submit" value="Submit"></form><p>If you click the "Submit" button, your order will be sent.</p></body></html>', "utf-8"))
			
	def do_POST(s):
		global leg_length, leg_side, seat_length, seat_width, height_backplate, i, productOK

		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()
		
		# Check what is the path
		path = s.path
		print("Path: ", path)	
		if path.find("/setLimits") != -1:
			print("Inside of /product path")
			content_len = int(s.headers.get('Content-Length'))
			post_body = s.rfile.read(content_len)
			body = post_body.decode()
			pairs = body.split("&")
			#First pair
			pair0 = pairs[0].split("=")
			leg_length_min = int(pair0[1])
			#Second pair
			pair1 = pairs[1].split("=")
			leg_length_max = int(pair1[1])
			#Third pair
			pair2 = pairs[2].split("=")
			leg_side_min = int(pair2[1])
			#Fourth pair
			pair3 = pairs[3].split("=")
			leg_side_max = int(pair3[1])
			#Fifth pair
			pair4 = pairs[4].split("=")
			seat_length_min = int(pair4[1])
			#Sixth pair
			pair5 = pairs[5].split("=")
			seat_length_max = int(pair5[1])
			#Seventh pair
			pair6 = pairs[6].split("=")
			seat_width_min = int(pair6[1])
			#Eighth pair
			pair7 = pairs[7].split("=")
			seat_width_max = int(pair7[1])
			#Nineth pair
			pair8 = pairs[8].split("=")
			height_backplate_min = int(pair8[1])
			#Tenth pair
			pair9 = pairs[9].split("=")
			height_backplate_max = int(pair9[1])
			
			print("height_backplate_min", height_backplate_min)
			
			s.setConstrain("hasMaxLengthLeg", leg_length_max)
			s.setConstrain("hasMinLengthLeg", leg_length_min)
			s.setConstrain("hasMaxSideLeg", leg_side_max)
			s.setConstrain("hasMinSideLeg", leg_side_min)
			s.setConstrain("hasMaxLengthTop", seat_length_max)
			s.setConstrain("hasMinLengthTop", seat_length_min)
			s.setConstrain("hasMaxHeightTop", height_backplate_max)
			s.setConstrain("hasMinHeightTop", height_backplate_min)
			s.setConstrain("hasMinWidthTop", seat_width_min)
			s.setConstrain("hasMaxWidthTop", seat_width_max)
				
		
	def setConstrain(self, constrain, value):
		URL = "http://127.0.0.1:3030/kbe/update"
  
		# Step 1: defining a query to delete previous value.
		PARAMS = {'update':'PREFIX kbe:<http://kbe.openode.io/table-kbe.owl#> DELETE {?topcutter kbe:' + constrain + ' ?min.} WHERE { ?topcutter kbe:' + constrain +' ?min.}'}
		# sending get request and saving the response as response object 
		r = requests.post(url = URL, data = PARAMS) 

		#Checking the result
		print("Result for DELETE query:", r.text)
		
		# Step 2: defining a query to INSERT new value.
		# Check if it is top or leg.
		type = ''
		if constrain.find("Top") != -1:
			type = "TopCutter"
		else:
			type = "LegCutter"
		
		PARAMS = {'update':'PREFIX kbe:<http://kbe.openode.io/table-kbe.owl#> INSERT { ?topcutter kbe:' + constrain + ' "' + str(value) + '"^^<http://www.w3.org/2001/XMLSchema#int>.} WHERE { ?topcutter a kbe:' + type + '.}'} 
		  
		# sending get request and saving the response as response object 
		r = requests.post(url = URL, data = PARAMS) 

		#Checking the result
		print("Result of INSERT query:", r.text)


		
		
 
if __name__ == '__main__':
	server_class = HTTPServer
	httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
	
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	httpd.server_close()
