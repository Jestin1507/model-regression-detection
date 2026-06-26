from fastapi import FastAPI
from pydantic import BaseModel

from app.classifier import TicketClassifier

app = FastAPI(
    title="Model Regression Detection System",
    version="1.0.0"
)

classifier = TicketClassifier()


class TicketRequest(BaseModel):
    text: str


class TicketResponse(BaseModel):
    category: str


@app.get("/")
def home():
    return {
        "message": "Model Regression Detection System API is running."
    }


@app.post("/classify", response_model=TicketResponse)
def classify_ticket(request: TicketRequest):

    prediction = classifier.classify(request.text)

    return TicketResponse(category=prediction)