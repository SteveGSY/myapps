import http.server
import ssl
import os
import subprocess

PORT = 8443
CERT_FILE = "cert.pem"
KEY_FILE = "key.pem"

def generate_cert():
    print("🔐 No certificate found — generating self‑signed certificate...")
    cmd = [
        "openssl", "req", "-new", "-x509",
        "-keyout", KEY_FILE,
        "-out", CERT_FILE,
        "-days", "365",
        "-nodes",
        "-subj", "/CN=localhost"
    ]
    subprocess.run(cmd, check=True)
    print("✅ Certificate generated.\n")

def main():
    # Generate cert if missing
    if not (os.path.exists(CERT_FILE) and os.path.exists(KEY_FILE)):
        generate_cert()

    handler = http.server.SimpleHTTPRequestHandler
    httpd = http.server.HTTPServer(("0.0.0.0", PORT), handler)

    # Modern SSL context (Python 3.12+ compatible)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)

    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

    print("🔒 Secure HTTPS server running")
    print(f"👉 https://localhost:{PORT}")
    print(f"👉 https://YOUR_PC_IP:{PORT}  (for iPhone/Android)")
    print("\nPress CTRL+C to stop.\n")

    httpd.serve_forever()

if __name__ == "__main__":
    main()