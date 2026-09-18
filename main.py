import os
import requests
from flask import Flask, request, Response
from urllib.parse import urlparse

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'])
def proxy_handler(path):
    # Default active bypass upstream server
    upstream_base = "https://clientbp.ggblueshark.com"
    
    path_lower = path.lower()
    full_url_str = request.url.lower()

    # Dynamic multi-server routing logic based on request path and domain
    if 'connect.garena.com' in full_url_str or 'oauth' in path_lower or 'game/account_security' in path_lower:
        upstream_base = "https://100067.connect.garena.com"
    elif 'ggblueshark.com' in full_url_str:
        upstream_base = "https://clientbp.ggblueshark.com"
    elif 'ggwhitehawk.com' in full_url_str:
        upstream_base = "https://clientbp.ggwhitehawk.com"
    elif 'ggpolarbear.com' in full_url_str or any(k in path_lower for k in ['majorlogin', 'majorregister', 'getlogindata', 'chooseregion', 'majormodifynickname']):
        upstream_base = "https://loginbp.ggpolarbear.com"

    target_url = f"{upstream_base.rstrip('/')}/{path}"
    if request.query_string:
        target_url += f"?{request.query_string.decode('utf-8')}"

    # Unnecessary headers filter karna taaki connection stable rahe
    excluded_headers = ['host', 'content-length', 'transfer-encoding', 'connection']
    headers = {k: v for k, v in request.headers.items() if k.lower() not in excluded_headers}
    
    parsed_upstream = urlparse(upstream_base)
    headers['Host'] = parsed_upstream.netloc

    # Token ya request log check karne ke liye
    auth_token = request.headers.get('Authorization') or request.headers.get('access_token')
    if auth_token:
        print(f"[+] Active Token Detected on path [{path}] -> Routing to: {parsed_upstream.netloc}")

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

    # Response headers ko filter karna aur location header rewrite karna
    response_headers = []
    proxy_host = request.host

    for k, v in resp.raw.headers.items():
        k_lower = k.lower()
        if k_lower in ('content-encoding', 'transfer-encoding', 'connection', 'content-length'):
            continue
        if k_lower == 'location':
            v = v.replace(parsed_upstream.netloc, proxy_host)
        response_headers.append((k, v))

    return Response(
        response=resp.content,
        status=resp.status_code,
        headers=response_headers
    )

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
