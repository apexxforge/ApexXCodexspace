from fastapi import FastAPI, Request, Response
import httpx
import time
import random
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

app = FastAPI()

TARGET_SERVER = "https://loginbp.ppmainecoonghj.com"

AES_KEY = bytes([89,103,38,116,99,37,68,69,117,104,54,37,90,99,94,56])
AES_IV  = bytes([54,111,121,90,68,114,50,50,69,51,121,99,104,106,77,37])

dEvIcEs = [
    "Asus ASUS_I005DA", "SM-G998B", "CPH2095", "Pixel 6", "OnePlus 9 Pro",
    "Samsung Galaxy S23 Ultra", "Xiaomi 13 Pro", "Redmi Note 10 Pro"
]
cArRiErS = ["Jio", "Airtel", "Vodafone Idea", "BSNL", "T-Mobile", "AT&T"]
GPUS = ["Adreno (TM) 640", "Mali-G78", "Adreno 660", "Mali-G610"]

def sTaR_vArInT_eNcOdE(n):
    if n < 0:
        n += 1 << 64
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        if n:
            out.append(b | 0x80)
        else:
            out.append(b)
            return bytes(out)

def sTaR_bUiLd_FiElD(field_num, value):
    if isinstance(value, bool):
        return sTaR_vArInT_eNcOdE((field_num << 3) | 0) + sTaR_vArInT_eNcOdE(1 if value else 0)
    if isinstance(value, int):
        return sTaR_vArInT_eNcOdE((field_num << 3) | 0) + sTaR_vArInT_eNcOdE(value)
    if isinstance(value, (str, bytes)):
        data = value.encode("utf-8") if isinstance(value, str) else value
        return sTaR_vArInT_eNcOdE((field_num << 3) | 2) + sTaR_vArInT_eNcOdE(len(data)) + data
    if isinstance(value, dict):
        sub = sTaR_aSsEmBlE_pRoTo(value)
        return sTaR_vArInT_eNcOdE((field_num << 3) | 2) + sTaR_vArInT_eNcOdE(len(sub)) + sub
    raise TypeError(f"Unsupported type: {type(value)}")

def sTaR_aSsEmBlE_pRoTo(fields: dict) -> bytes:
    packet = b""
    for k in sorted(fields.keys(), key=lambda x: int(x)):
        v = fields[k]
        fn = int(k)
        if isinstance(v, list):
            for item in v:
                packet += sTaR_bUiLd_FiElD(fn, item)
        else:
            packet += sTaR_bUiLd_FiElD(fn, v)
    return packet

def sTaR_aEs_EnCrYpT(plain: bytes) -> bytes:
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plain) + padder.finalize()
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(AES_IV), backend=default_backend())
    encryptor = cipher.encryptor()
    return encryptor.update(padded_data) + encryptor.finalize()

def build_major_login_proto(access_token):
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    model = random.choice(dEvIcEs)
    carrier = random.choice(cArRiErS)
    gpu = random.choice(GPUS)
    
    # Consistent user_id and open_id based on access_token hash so it never creates a new account
    token_hash = hashlib.md5(access_token.encode()).hexdigest()
    user_id = f"Google|{token_hash}"
    open_id = token_hash

    fields = {
        3: now, 4: "free fire", 5: 1, 7: "2.127.13",
        8: "Android OS 9 / API-28 (PI/rel.cjw.20220518.114133)", 9: "Handheld",
        10: carrier, 11: "WIFI", 12: 1334, 13: 750, 14: "300",
        15: "ARMv7 VFPv3 NEON VMH | 2400 | 2", 16: 1993, 17: gpu,
        18: "OpenGL ES 3.2", 19: user_id, 20: "105.235.139.91",
        21: "en", 22: open_id, 23: "4", 24: "Handheld", 25: model,
        29: access_token, 30: 1, 41: carrier, 42: "WIFI",
        57: "7428b253defc164018c604a1ebbfebdf", 60: 32936, 61: 29430,
        62: 2479, 63: 900, 64: 30823, 65: 32936, 66: 30823, 67: 32936,
        73: 1, 74: "/data/app/com.dts.freefireth-PdeDnOilCSFn37p1AH_FLg==/lib/arm",
        76: 1, 77: "2087f61c19f57f2af4e7feff0b24d9d9|/data/app/com.dts.freefireth-PdeDnOilCSFn37p1AH_FLg==/base.apk",
        78: 3, 79: 1, 81: "32", 83: "2019118692", 86: "OpenGLES2",
        87: 16383, 88: 4, 92: 9075, 93: "android",
        94: "KqsHT5ZLWrYljNb5Vqh//yFRlaPHSO9NWSQsVvOmdhEEn7W+VHNUK+Q+fduA3ptNrGB0Ll0LRz3WW0jOwesLj6aiU7sZ40p8BfUE/FI/jzSTwRe2",
        95: 111227, 97: 1, 98: 1, 99: "4", 100: "4",
        102: bytes.fromhex("47 51 40 4f 00 0e 5e 00 44 06 55 41 0e 50 4d 0d 13 68 5a 07 54 06 0c 6d 5c 56 0e 6a 59 56 3b 0b 55 35")
    }
    return sTaR_aEs_EnCrYpT(sTaR_aSsEmBlE_pRoTo(fields))

@app.api_route("/MajorLogin", methods=["GET", "POST"])
@app.api_route("/", methods=["GET", "POST"])
@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def universal_handler(request: Request, path_name: str = ""):
    access_token = request.query_params.get("access_token")

    if access_token:
        url = f"{TARGET_SERVER}/MajorLogin"
        encrypted_payload = build_major_login_proto(access_token)
        headers = {
            "Accept-Encoding": "gzip",
            "Connection": "Keep-Alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "loginbp.ppmainecoonghj.com",
            "ReleaseVersion": "OB55",
            "User-Agent": "UnityPlayer/2022.3.47f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)",
            "X-GA": "v1 1",
            "X-Ga-Sv": "1789534056",
            "X-Unity-Version": "2022.3.47f1"
        }
        async with httpx.AsyncClient(verify=False, timeout=30.0) as client:
            try:
                response = await client.post(url, headers=headers, content=encrypted_payload)
                return Response(content=response.content, status_code=response.status_code, headers=dict(response.headers))
            except Exception as e:
                return Response(content=str(e), status_code=500)

    async with httpx.AsyncClient(verify=False, timeout=30.0) as client:
        target_path = path_name if path_name else ""
        url = f"{TARGET_SERVER}/{target_path}"
        body = await request.body()
        headers = dict(request.headers)
        headers.pop("host", None)
        headers["host"] = "loginbp.ppmainecoonghj.com"

        try:
            response = await client.request(
                method=request.method,
                url=url,
                headers=headers,
                content=body,
                params=request.query_params
            )
            return Response(content=response.content, status_code=response.status_code, headers=dict(response.headers))
        except Exception as e:
            return Response(content=str(e), status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
