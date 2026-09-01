from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

inspections = [
    {"id": 1, "plot_id": "P-101", "issue": "Cracked boundary wall", "resolved": False},
    {"id": 2, "plot_id": "P-102", "issue": "Water logging near the gate", "resolved": False},
    {"id": 3, "plot_id": "P-103", "issue": "Construction debris not cleared", "resolved": True},
]


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


@app.get("/inspections")
def list_inspections():
    return inspections


@app.get("/inspections/{id}")
def get_inspection(id: int):
    for inspection in inspections:
        if inspection["id"] == id:
            return inspection
    return JSONResponse(status_code=404, content={"error": f"Inspection {id} not found"})
