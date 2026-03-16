"""
INSECURE demo server — intentionally bad practices for demonstration purposes.

BAD PRACTICES demonstrated here:
  - No HTTPS (plain HTTP)
  - Passwords stored in plaintext
  - No input validation or sanitization
  - Sensitive data written to a world-readable text file
  - No authentication or access control
  - No rate limiting
  - Stack traces leaked to the client on errors
  - Data file path is user-controllable (path traversal risk)
"""

import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

DATA_FILE = "data.txt"  # Insecure: plain-text, no encryption


class InsecureHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            with open("index.html", "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/submit":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)

            # Insecure: no input validation whatsoever
            data = json.loads(body)

            # Insecure: store all sensitive fields in plain text
            with open(DATA_FILE, "a") as f:
                f.write(
                    f"name={data.get('name')} | "
                    f"email={data.get('email')} | "
                    f"password={data.get('password')} | "
                    f"phone={data.get('phone')} | "
                    f"dob={data.get('dob')} | "
                    f"ssn={data.get('ssn')}\n"
                )

            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Stored.")
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, fmt, *args):  # noqa: D102
        print(fmt % args)


if __name__ == "__main__":
    host, port = "0.0.0.0", 8080
    server = HTTPServer((host, port), InsecureHandler)
    print(f"[INSECURE DEMO] Running on http://{host}:{port}  —  DO NOT USE IN PRODUCTION")
    server.serve_forever()
