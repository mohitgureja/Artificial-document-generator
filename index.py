import uvicorn
from fastapi import FastAPI

from components.artifact_engine import config_service
from components.orchestrator import orchestrator_service
from components.orchestrator.models import RequestBody

app = FastAPI()


@app.get("/")
def read_root():
    return 'Welcome to Artificial Document Generator!'


# Endpoint to create invoices
@app.post("/create")
def create_documents(body: RequestBody, doc_format="invoice"):
    json_data = orchestrator_service.orchestrate(body, doc_format)
    return json_data


@app.get("/config")
def get_configuration(doc_format="invoice"):
    return config_service.get_configuration(doc_format)


if __name__ == "__main__":
    app.title = "Artificial Document Generator"
    uvicorn.run("__main__:app", port=8002)
