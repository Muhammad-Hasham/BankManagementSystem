from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import ClientRoutes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ClientRoutes.router, prefix="/client", tags=["Client"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
