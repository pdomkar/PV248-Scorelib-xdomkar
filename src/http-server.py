import http.server

class MyHttp(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if len(self.path) == 1:
            self.protocol_version = 'HTTP/1.1'
            self.send_response(404, 'not requested file')
            self.end_headers()
        else:
            self.protocol_version = 'HTTP/1.1'
            self.send_response(200, 'OK')
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(bytes("you asked for " + self.path[1:], 'UTF-8'))

if __name__ == "__main__":
    port = 8000
    print('Listening on localhost:%s' % port)
    server = http.server.HTTPServer(('', port), MyHttp)
    server.serve_forever()

