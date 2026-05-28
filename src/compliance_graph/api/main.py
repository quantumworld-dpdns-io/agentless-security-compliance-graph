from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import api_router

app = FastAPI(
    title="Compliance Graph API",
    version="0.1.0",
    description="Agentless Security Compliance Graph API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.get("/health")
def health():
    return {"status": "ok", "version": "0.1.0"}
