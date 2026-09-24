# acts as both our REST API and our target website - uses python built-in HTTP server so requires no more packages
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

PRODUCTS_DATA = [
    {"id": 1, "name": "Freddie's Loaf", "price": 6500, "category": "Baked"},
    {"id": 2, "name": "Freddie's Bun", "price": 6500, "category": "Baked"},
    {"id": 3, "name": "Zinga Daddies", "price": 25000, "category": "Fried"},
    {"id": 4, "name": "Zinga Plantain Chips", "price": 33000, "category": "Fried"},
    {"id": 5, "name": "Tropik Fruit Mango", "price": 15500, "category": "Dried"},
    {"id": 6, "name": "Tropik Fruit Pineapple", "price": 15500, "category": "Baked"},
]

REVIEWS_DATA = {
    1:{"score":4.5, "count":120},
    2:{"score":0.0, "count":0},     # edge case: No reviews
    3:{"score":4.5, "count":850},
    4:{"score":4.7, "count":350},
    5:{"score":4.1, "count":980},
    6:{"score":5.0, "count":1047},
}

class MockHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return      # silence the terminal log noise

    def do_GET(self):
        if self.path == "/api/products":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(PRODUCTS_DATA).encode())

        elif self.path.startswith("/reviews/"):
            try:
                prod_id = int(self.path.split("/")[-1])
                rev = REVIEWS_DATA.get(prod_id, {"score": 0.0, "count":0})
                html = f"""
                <html>
                    <body>
                        <span id="avg-score">{rev['score']}</span>
                        <span id="review-count">{rev['count']}</span>
                    </body>
                </html>
                """

                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(html.encode())
            except ValueError:
                self.send_response(404)
                self.end_headers()

if __name__ == "__main__":
    server = HTTPServer(("localhost",8000), MockHandler)
    print("Mock Server listening on http://localhost:8000...")
    server.serve_forever()