
from src.backend import Backend
import fastapi
import asyncio

app = fastapi.FastAPI()

@app.on_event("startup")
async def startup_event():
    backend = Backend(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
