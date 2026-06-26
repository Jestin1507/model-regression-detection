from app.classifier import TicketClassifier

classifier = TicketClassifier()

result = classifier.classify(
    "I want my money back because the order never arrived."
)

print(result)