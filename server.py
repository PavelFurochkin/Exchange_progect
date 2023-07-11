from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import Execute_from_db as Ex_db


class HelloWorld:
    def __init__(self, hello):
        self.hello = hello


Hello = HelloWorld('world')


class OurHandler(BaseHTTPRequestHandler):
    def currencies(self):
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()

        json_st = json.dumps(Ex_db.ExecuteBd.rows, ensure_ascii=False)
        self.wfile.write(json_st.encode('utf-8'))

    def hello_page(self):
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-Type', 'text/html; charset = UTF-8')
        self.end_headers()

        self.wfile.write('<h1>Hello World</h1>'.encode('utf-8'))

    def test_page(self):
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        json_string = json.dumps(Hello.__dict__)

        self.wfile.write(bytes(json_string, 'utf-8'))

    def do_GET(self):
        if self.path == '/hello':
            self.hello_page()
        if self.path == '/test':
            self.test_page()
        if self.path == '/currencies':
            self.currencies()


if __name__ == '__main__':
    with HTTPServer(('', 8000), OurHandler) as server:
        server.serve_forever()
