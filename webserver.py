from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pydantic import BaseModel
from pydantic import ValidationError


class Crypto(BaseModel):
    name: str
    price: int


class SimpleHandler(BaseHTTPRequestHandler):

    db = {
        1: Crypto(name="TrumpCoin", price=8000000),
        2: Crypto(name="FPIBank", price=88888888),
        3: Crypto(name="Bitcoin", price=10000000),
    }

    def do_GET(self):
        if self.path == '/':
            self.home()
        elif self.path == '/crypto':
            self.crypto()
        else:
            self.not_found()

    def do_POST(self):
        if self.path == '/submit':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            self.submit(post_data)
        else:
            self.not_found()

    def home(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Hello: FastAPI")

    def crypto(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        crypto_data = {
            key: crypto.model_dump()
            for key, crypto in self.db.items()
        }
        response = json.dumps(crypto_data).encode('utf-8')
        self.wfile.write(response)

    def submit(self, post_data):
        try:
            decoded_data = json.loads(post_data.decode('utf-8'))
            new_id = max(self.db.keys()) + 1 if self.db else 1
            crypto_obj = Crypto(**decoded_data)
            self.db[new_id] = crypto_obj
            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = json.dumps({
                "id": new_id,
                "name": crypto_obj.name,
                "price": crypto_obj.price
            })
            self.wfile.write(response.encode('utf-8'))
        except (json.JSONDecodeError, ValidationError) as e:
            self.send_response(400)
            self.end_headers()
            error_msg = f"Invalid data: {str(e)}"
            self.wfile.write(error_msg.encode('utf-8'))

    def not_found(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"404 Not Found")


server = HTTPServer(('localhost', 8080), SimpleHandler)
server.serve_forever()
