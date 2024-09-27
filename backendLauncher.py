import src.backend as backend
import fastapi
import asyncio
import uvicorn

app = fastapi.FastAPI()
application = backend.Backend(app, 'myapp', aoty=True, bea=True, meta=True, rym=False)

@app.on_event("startup")
async def startup_event():
    await application.async_init()

def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

main()
