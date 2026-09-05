from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.resources import router as resources_router
from app.api.users import router as users_router
from app.api.auth import router as auth_router


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
app.include_router(auth_router)
app.include_router(resources_router)


# Serve uploaded files
app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)