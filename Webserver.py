# https://wiki.python.org/moin/BaseHttpServer
# https://www.w3schools.com/graphics/svg_intro.asp
from http.server import BaseHTTPRequestHandler, HTTPServer
# import BaseHTTPServer
import time
import requests
import json

HOST_NAME = '127.0.0.1'
PORT_NUMBER = 1234  # Maybe set this to 1234


class Status():
    status = False

    def set(self):
        self.status = True

    def reset(self):
        self.status = False

    def get(self):
        return self.status


status = Status()


class MyHandler(BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write(
            bytes('<html><head><title>Cool interface.</title><meta http-equiv="refresh" content="3"></head>', 'utf-8'))
        s.wfile.write(bytes("<body><p>This is a test.</p>", "utf-8"))
        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        s.wfile.write(bytes("<p>You accessed path: %s</p>" % s.path, "utf-8"))
        color = "yellow"
        checkStatus('{}')
        if status.get():
            color = "red"
        else:
            color = "yellow"
        s.wfile.write(bytes(
            '<svg width="100" height="100"><circle cx="50" cy="50" r="40" stroke="green" stroke-width="4" fill="' + color + '" /></svg>',
            'utf-8'))
        s.wfile.write(bytes("</body></html>", "utf-8"))


def checkStatus(data):
    data_ = json.loads(data)
    url = 'http://escop.rd.tut.fi:3000/RTU/SimCNV8/services/Z1'
    headers = {"Content-Type": "application/json"}
    # call get service with headers and params
    response = requests.post(url, json=data_)
    print("code:" + str(response.status_code))
    print("******************")
    print("headers:" + str(response.headers))
    print("******************")
    print("content:" + str(response.json()))
    if response.json()["PalletID"] != -1:
        status.set()
    else:
        status.reset()


if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print(time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER))
