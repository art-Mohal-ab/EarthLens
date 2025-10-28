from fastapi import FastAPI
from server.database import engine, Base
from server.routes import auth


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EarthLens API",
    description="Backend API for EarthLens authentication",
    version="1.0.0"
)


app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Welcome to EarthLens API"}
