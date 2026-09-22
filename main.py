from fastapi import FastAPI, Request, Response
import httpx

app = FastAPI()

# Target Game Server URL jahan request forward karni hai
TARGET_SERVER = "https://loginbp.ppmainecoonghj.com"

@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy(request: Request, path_name:path):
    client = httpx.AsyncClient(verify=False)
    url = f"{TARGET_SERVER}/{path_name}"
    
    # Incoming request ke data aur headers read karna
    body = await request.body()
    headers = dict(request.headers)
    
    # Host header ko target ke hisaab se update karna
    headers["host"] = "loginbp.ppmainecoonghj.com"
    
    # Optional: Yahan aap login bypass ya token manipulation kar sakte hain
    # Jaise agar koi specific header add ya remove karna ho:
    # headers["Authorization"] = "Bearer BYPASSED_TOKEN"

    try:
        # Target server ko request bhejLikewise
        response = await client.request(
            method=request.method,
            url=url,
            headers=headers,
            content=body,
            params=request.query_params
        )
        
        # Server ka response wapas client ko dena
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers)
        )
    except Exception as e:
        return {"error": str(e)}
    finally:
        await client.aclose()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
  
