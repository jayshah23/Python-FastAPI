from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import model
from .database import engine
from .routes import posts, users, auth, votes

# model.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"Message": "Hello Jay"}

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)