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

    def do_GET(self):
        try:
            path = self.path
            response = {
                '/api': json.dumps(data['GET']).encode()
            }[path]
            self.send_response(HTTPStatus.OK)
        except:
            response = json.dumps({'error': 'null'}).encode()
            self.send_response(HTTPStatus.INTERNAL_SERVER_ERROR)
        self.send_header("Content-type", "application/json; charset=UTF-8")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)
    
    def do_POST(self):
        try:
            path = self.path
            response = {
                '/api': json.dumps(data['POST']).encode()
            }[path]
            self.send_response(HTTPStatus.OK)
        except:
            response = json.dumps({'error': 'null'}).encode()
            self.send_response(HTTPStatus.INTERNAL_SERVER_ERROR)
        self.send_header("Content-type", "application/json; charset=UTF-8")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

if __name__ == "__main__":
    print('Server Start: localhost:%s'%(PORT))
    thread = threading.Thread(target=httpServe)
    thread.start()