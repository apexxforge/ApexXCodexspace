import os
import requests
from flask import Flask, request, Response

app = Flask(__name__)

UPSTREAM_SERVER = "https://client.ind.freefiremobile.com"

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'])
def proxy_handler(path):
    target_url = f"{UPSTREAM_SERVER.rstrip('/')}/{path}"
    if request.query_string:
        target_url += f"?{request.query_string.decode('utf-8')}"

    # जरूरी हेडर्स को छोड़कर बाकी सब फॉरवर्ड करना
    excluded_headers = ['host', 'content-length', 'transfer-encoding', 'connection']
    headers = {k: v for k, v in request.headers.items() if k.lower() not in excluded_headers}
    
    # अपस्ट्रीम के लिए होस्ट सेट करना
    headers['Host'] = 'client.ind.freefiremobile.com'

    #ऑथेंटिकेशन टोकन या सेशन लॉग करना
    auth_token = request.headers.get('Authorization') or request.headers.get('access_token')
    if auth_token:
        print(f"[+] Active Token on [{path}]: {auth_token[:25]}...")

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

    # रिस्पॉन्स हेडर तैयार करना और रिडायरेक्ट लोकेशन को फिक्स करना
    response_headers = []
    proxy_host = request.host  # आपके सर्वर का डोमेन (जैसे Render URL)

    for k, v in resp.raw.headers.items():
        k_lower = k.lower()
        if k_lower in ('content-encoding', 'transfer-encoding', 'connection', 'content-length'):
            continue
        
        # अगर अपस्ट्रीम सर्वर रिडायरेक्ट भेज रहा है, तो उसका डोमेन प्रॉक्सी पर ही रीडायरेक्ट करें
        if k_lower == 'location':
            v = v.replace('https://client.ind.freefiremobile.com', f"https://{proxy_host}")
            v = v.replace('http://client.ind.freefiremobile.com', f"http://{proxy_host}")
            
        response_headers.append((k, v))

    return Response(
        response=resp.content,
        status=resp.status_code,
        headers=response_headers
    )

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
