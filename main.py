from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse

app = FastAPI()

inspections = [
    {"id": 1, "plot_id": "P-101", "issue": "Cracked boundary wall", "resolved": False},
    {"id": 2, "plot_id": "P-102", "issue": "Water logging near the gate", "resolved": False},
    {"id": 3, "plot_id": "P-103", "issue": "Construction debris not cleared", "resolved": True},
]


@app.get("/", summary="API info")
def root():
    return {
        "name": "Site Inspection API",
        "version": "1.0",
        "endpoints": ["/inspections"],
    }


@app.get("/health", summary="Health check")
def health():
    return {"status": "ok"}


@app.get("/inspections", summary="List all inspections")
def list_inspections():
    return inspections


@app.get("/inspections/{id}", summary="Get a single inspection by id")
def get_inspection(id: int):
    for inspection in inspections:
        if inspection["id"] == id:
            return inspection
    return JSONResponse(status_code=404, content={"error": f"Inspection {id} not found"})


@app.post("/inspections", status_code=201, summary="Create a new inspection")
def create_inspection(body: dict):
    if not body.get("plot_id"):
        return JSONResponse(status_code=400, content={"error": "plot_id is required"})
    if not body.get("issue"):
        return JSONResponse(status_code=400, content={"error": "issue is required and cannot be empty"})

    new_id = max(inspection["id"] for inspection in inspections) + 1 if inspections else 1

    inspection = {
        "id": new_id,
        "plot_id": body["plot_id"],
        "issue": body["issue"],
        "resolved": False,
    }
    inspections.append(inspection)
    return inspection


@app.put("/inspections/{id}", summary="Update an inspection")
def update_inspection(id: int, body: dict):
    for inspection in inspections:
        if inspection["id"] == id:
            if not any(field in body for field in ("plot_id", "issue", "resolved")):
                return JSONResponse(
                    status_code=400,
                    content={"error": "provide at least one of: plot_id, issue, resolved"},
                )
            if "plot_id" in body and not body["plot_id"]:
                return JSONResponse(status_code=400, content={"error": "plot_id cannot be empty"})
            if "issue" in body and not body["issue"]:
                return JSONResponse(status_code=400, content={"error": "issue cannot be empty"})
            if "resolved" in body and not isinstance(body["resolved"], bool):
                return JSONResponse(status_code=400, content={"error": "resolved must be true or false"})

            for field in ("plot_id", "issue", "resolved"):
                if field in body:
                    inspection[field] = body[field]
            return inspection
    return JSONResponse(status_code=404, content={"error": f"Inspection {id} not found"})


@app.delete("/inspections/{id}", summary="Delete an inspection")
def delete_inspection(id: int):
    for inspection in inspections:
        if inspection["id"] == id:
            inspections.remove(inspection)
            return Response(status_code=204)
    return JSONResponse(status_code=404, content={"error": f"Inspection {id} not found"})
