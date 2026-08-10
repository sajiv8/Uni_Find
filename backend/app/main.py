from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "Uni_Find Backend Running after changing"
    }
