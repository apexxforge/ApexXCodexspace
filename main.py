from fastapi import FastAPI, Request, Response
import httpx

app = FastAPI()

TARGET_SERVER = "https://loginbp.ppmainecoonghj.com"

@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy(request: Request, path_name: str):
    async with httpx.AsyncClient(verify=False, timeout=30.0) as client:
        url = f"{TARGET_SERVER}/{path_name}"
        
        # Request body aur headers lena
        body = await request.body()
        headers = dict(request.headers)
        
        # Render/Host headers clean karna taaki target server reject na kare
        headers.pop("host", None)
        headers["host"] = "loginbp.ppmainecoonghj.com"

        try:
            # Target server par request forward karna
            response = await client.request(
                method=request.method,
                url=url,
                headers=headers,
                content=body,
                params=request.query_params
            )
            
            # Response wapas client ko bhejna
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
        except Exception as e:
            return Response(content=str(e), status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
