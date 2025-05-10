from fastapi import FastAPI
from app.api.v1.routes import router

app = FastAPI(title="Islamic Finance Compliance Checker")
app.include_router(router)