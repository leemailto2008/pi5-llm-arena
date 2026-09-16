# f:\12_prj_raspi5\benchmark\speedtest_server.py
import http.server
import socketserver

class StreamHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/octet-stream')
        self.send_header('Content-length', str(100 * 1024 * 1024))
        self.end_headers()
        chunk = b'x' * (256 * 1024)
        for _ in range(400):
            try:
                self.wfile.write(chunk)
            except Exception:
                break

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    with socketserver.TCPServer(('0.0.0.0', 8888), StreamHandler) as httpd:
        httpd.handle_request()
