from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def show_index():
    return {"showing": bool(1)}
