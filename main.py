import os
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="KEYZO Backend Service",
    description="Render-ready backend for Free Fire login configuration",
    version="1.0.0"
)

# CORS middleware enable karna taaki external requests block na ho
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {
        "status": "Online",
        "service": "KEYZO Backend is running successfully on Render!",
        "code": 200
    }

@app.get("/login")
def handle_login(access_token: str = Query(..., description="User Access Token")):
    """
    Yeh endpoint game client se aane wale access token ko process 
    karke required serverUrl structure return karta hai.
    """
    # Naye domain structure ke mutabiq login URL mapping
    target_server_url = f"https://loginbp.ppmainecoonghj.com/login?access_token={access_token}"
    
    return {
        "serverUrl": target_server_url,
        "status": "Success",
        "message": "Configuration generated successfully."
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
    
