from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def show_index():
    return {"success": True}
