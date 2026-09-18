import os
import requests
from flask import Flask, request, Response
from urllib.parse import urlparse

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'])
def proxy_handler(path):
    full_url_str = request.url.lower()
    path_lower = path.lower()
    path_parts = path.strip('/').split('/')
    endpoint = path_parts[-1] if path_parts else ''
    full_path_str = path.lower()

    # Free Fire aur Garena ke login/dispatch endpoints ki routing
    if 'connect.garena.com' in full_url_str or 'oauth' in path_lower:
        upstream_base = "https://100067.connect.garena.com"
        target_path = path
    elif any(k in full_path_str for k in ['majorlogin', 'majorregister', 'getlogindata', 'chooseregion', 'majormodifynickname', 'getaccountbriefinfobeforelogin', 'getlogininfo']):
        upstream_base = "https://loginbp.ggpolarbear.com"
        target_path = endpoint if endpoint.lower() in ['majorlogin', 'majorregister', 'getlogindata', 'chooseregion', 'majormodifynickname', 'getaccountbriefinfobeforelogin', 'getlogininfo'] else path
    elif 'ggwhitehawk.com' in full_url_str:
        upstream_base = "https://clientbp.ggwhitehawk.com"
        target_path = path
    else:
        upstream_base = "https://clientbp.ggblueshark.com"
        target_path = path

    target_url = f"{upstream_base.rstrip('/')}/{target_path}"
    if request.query_string:
        target_url += f"?{request.query_string.decode('utf-8')}"

    # Headers ko clean karna aur client headers preserve karna
    excluded_headers = ['host', 'content-length', 'transfer-encoding', 'connection']
    headers = {k: v for k, v in request.headers.items() if k.lower() not in excluded_headers}
    
    parsed_upstream = urlparse(upstream_base)
    headers['Host'] = parsed_upstream.netloc

    # Authorization Token & Access Token enforcement for UID injection
    auth_token = request.headers.get('Authorization') or request.headers.get('access_token') or request.headers.get('token')
    if not auth_token:
        # Agar client request me token na ho, toh default fallback ya custom configuration token use karein
        pass

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
    
