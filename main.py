import os
import requests
from flask import Flask, request, Response

app = Flask(__name__)

# Free Fire ka official regional upstream server (India region ke liye)
UPSTREAM_SERVER = "https://client.ind.freefiremobile.com"

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'])
def proxy_handler(path):
    target_url = f"{UPSTREAM_SERVER.rstrip('/')}/{path}"
    if request.query_string:
        target_url += f"?{request.query_string.decode('utf-8')}"

    # Unnecessary headers filter karna taaki connection stable rahe
    excluded_headers = ['host', 'content-length', 'transfer-encoding', 'connection']
    headers = {k: v for k, v in request.headers.items() if k.lower() not in excluded_headers}
    
    # Upstream ke liye sahi Host header explicitly define karna
    headers['Host'] = 'client.ind.freefiremobile.com'

    # Token ya request log check karne ke liye
    auth_token = request.headers.get('Authorization') or request.headers.get('access_token')
    if auth_token:
        print(f"[+] Active Token Detected on path [{path}]: {auth_token[:25]}...")

    try:
        resp = requests.request(
            method=request.method,
            url=target_url,
            headers=headers,
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False,
            timeout=30
        )
    except requests.exceptions.RequestException as e:
        return Response(f"Proxy upstream error: {e}", status=502)

    # Response headers ko filter karna
    response_headers = [
        (k, v) for k, v in resp.headers.items()
        if k.lower() not in ('content-encoding', 'transfer-encoding', 'connection', 'content-length')
    ]

    return Response(
        response=resp.content,
        status=resp.status_code,
        headers=response_headers
    )

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
