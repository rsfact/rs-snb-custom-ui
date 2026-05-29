import os
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

load_dotenv()
APP_ID = os.getenv("NTA_APP_ID")
NTA_URL = os.getenv("NTA_URL")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/nta")
def proxy_nta(number: str):
    if not APP_ID:
        raise HTTPException(status_code=500, detail="NTA_APP_ID is missing")
    params = {"id": APP_ID, "number": number, "type": 12, "history": 0}
    res = requests.get(NTA_URL, params=params, timeout=10)
    return Response(res.text, status_code=res.status_code, media_type="application/xml")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend:app", host="0.0.0.0", port=7009, reload=True)