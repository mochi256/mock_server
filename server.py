#!/usr/bin/env python3
import json
import threading
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from http import HTTPStatus

PORT = 5000

with open('response.json') as f:
    data = json.load(f)

def httpServe():
    handler = StubHttpRequestHandler
    httpd = HTTPServer(('',PORT),handler)
    httpd.serve_forever()

class StubHttpRequestHandler(BaseHTTPRequestHandler):
    server_version = "HTTP Stub/0.1"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def __send(self, data, status):
        data = json.dumps(data).encode()
        self.send_response(status)
        # specify json for content-type violate 
        # the cors policy, use text
        self.send_header("Content-type", "text/plain; charset=UTF-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Request-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)
    
    def do_OPTIONS(self):
        try:
            path = self.path
            response = data['GET'][path]
            write_data = response['data']
            http_status = response['status']
        except:
            write_data = {'message': 'not found'}
            http_status = 404
        self.__send(write_data, http_status)

    def do_GET(self):
        try:
            path = self.path
            response = data['GET'][path]
            write_data = response['data']
            http_status = response['status']
        except:
            write_data = {'message': 'not found'}
            http_status = 404
        self.__send(write_data, http_status)
    
    def do_POST(self):
        try:
            path = self.path
            response = data['POST'][path]
            write_data = response['data']
            http_status = response['status']
        except:
            write_data = {'message': 'not found'}
            http_status = 404
        self.__send(write_data, http_status)

if __name__ == "__main__":
    print('Server Start: localhost:%s'%(PORT))
    thread = threading.Thread(target=httpServe)
    thread.start()