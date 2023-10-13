from fastapi import FastAPI

from api.endpoints import api_router

app = FastAPI(tittle="Questions Backend")

app.include_router(api_router)
