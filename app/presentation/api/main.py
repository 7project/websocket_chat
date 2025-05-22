from fastapi import FastAPI
from presentation.api.endpoints.ws import router as ws_router


def create_app() -> FastAPI:
    app: FastAPI = FastAPI(title="WebSocket Chat", version="1.0.0")

    app.include_router(ws_router)

    @app.get("/")
    async def index():
        return {"message": "WebSocket Chat is start!"}

    return app