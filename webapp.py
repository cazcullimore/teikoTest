
# from flask import Flask, render_template



from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            self.wfile.write(b"""
                <html>
                <body>
                    <form method="POST" action="/submit">
                        <input name="text">
                        <button type="submit">Send</button>
                    </form>
                </body>
                </html>
            """)

    def do_POST(self):
        if self.path == "/submit":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode()

            data = parse_qs(post_data)
            text = data.get("text", [""])[0]

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            response = f"<html><body>You typed: {text}</body></html>"
            self.wfile.write(response.encode())

server = HTTPServer(("localhost", 8000), MyHandler)
server.serve_forever()