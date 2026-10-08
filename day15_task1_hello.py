from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Привет, FastAPI!"}

@app.get("/about")
def read_about():
    return {"name": "Алексей", "city": "Ningbo", "learning": "FastAPI"}

@app.get("/health")
def read_health():
    return {"status": "ok"}