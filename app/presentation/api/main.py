from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from presentation.api.endpoints.ws import router as ws_router
from presentation.api.endpoints.users import router as users_router
from presentation.api.endpoints.chats import router as chats_router
from presentation.api.endpoints.messages import router as messages_router


def create_app() -> FastAPI:
    app: FastAPI = FastAPI(title="WebSocket Chat", version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=r"http://localhost(:\d+)?",
        allow_origins=["file://"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(ws_router)
    app.include_router(users_router)
    app.include_router(chats_router)
    app.include_router(messages_router)

    @app.get("/")
    async def index():
        return {"message": "WebSocket Chat API", "docs": "/docs"}

    @app.get("/health")
    async def health():
        return {"status": "healthy"}

    return app