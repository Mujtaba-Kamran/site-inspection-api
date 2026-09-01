from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {
        "name": "Site Inspection API",
        "version": "1.0",
        "endpoints": ["/inspections"],
    }


@app.get("/health")
def health():
    return {"status": "ok"}
