import os
import requests
from flask import Flask, request, Response

app = Flask(__name__)

UPSTREAM_SERVER = "https://httpbin.org"

@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
def proxy(path):
    url = f"{UPSTREAM_SERVER}/{path}"

    if request.query_string:
        url += "?" + request.query_string.decode()

    headers = {
        k: v for k, v in request.headers.items()
        if k.lower() not in ["host", "content-length", "transfer-encoding", "connection"]
    }

    try:
        r = requests.request(
            request.method,
            url,
            headers=headers,
            data=request.get_data(),
            allow_redirects=False,
            timeout=20
        )

        return Response(
            r.content,
            status=r.status_code,
            headers={
                k: v for k, v in r.headers.items()
                if k.lower() not in ["content-length", "transfer-encoding", "connection"]
            }
        )

    except requests.RequestException as e:
        return Response(f"Upstream error: {e}", status=502)


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
