from fastapi import FastAPI

from app.api.users import router as users_router

app = FastAPI(
    title="Uni_Find API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Uni_Find Backend Running"
    }


app.include_router(users_router)