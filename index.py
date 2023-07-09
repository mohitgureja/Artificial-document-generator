import uvicorn
from fastapi import FastAPI

from orchestrator import orchestrator_service
from orchestrator.models import RequestBody

app = FastAPI()


@app.get("/")
def read_root():
    return 'Welcome to Artificial Data Generator!'


# Endpoint to create invoices
@app.post("/create")
def create_invoices(body: RequestBody):
    json_data = orchestrator_service.orchestrate(body)
    return json_data


if __name__ == "__main__":
    app.title = "Artificial Data Generator"
    uvicorn.run("__main__:app")
