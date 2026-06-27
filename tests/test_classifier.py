from app.classifier import TicketClassifier

classifier = TicketClassifier()

text = "My payment failed yesterday."

prediction = classifier.classify(text)

print(prediction)