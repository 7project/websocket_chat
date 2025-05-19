from fastapi import FastAPI



def create_app() -> FastAPI:
    app: FastAPI = FastAPI(title="WebSocket Chat", version="1.0.0")


    @app.get("/")
    async def index():
        return {"message": "WebSocket Chat is start!"}

    return app