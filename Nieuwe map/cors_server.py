from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
import os

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        if self.path == '/data.json':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data)
                ip = data.get('ip')
                # Load existing IPs or start a new list
                if os.path.exists('data.json'):
                    with open('data.json', 'r') as f:
                        try:
                            ip_list = json.load(f)
                            if not isinstance(ip_list, list):
                                ip_list = []
                        except Exception:
                            ip_list = []
                else:
                    ip_list = []
                # Append new IP if present
                if ip:
                    ip_list.append(ip)
                # Save updated list
                with open('data.json', 'w') as f:
                    json.dump(ip_list, f)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'success'}).encode())
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'error', 'message': str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

if __name__ == '__main__':
    HTTPServer(('0.0.0.0', 8000), CORSRequestHandler).serve_forever()