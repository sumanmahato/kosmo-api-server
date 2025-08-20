import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


class BertIntentRouter:
    _instance = None
    _model = None
    _tokenizer = None
    _id2label = {0: "da_query", 1: "workflow", 2: "rag_query"}

    def __new__(cls, model_path="bert-intent"):
        if cls._instance is None:
            cls._instance = super(BertIntentRouter, cls).__new__(cls)
            cls._tokenizer = AutoTokenizer.from_pretrained(model_path)
            cls._model = AutoModelForSequenceClassification.from_pretrained(model_path)
            cls._model.eval()

        return cls._instance

    def predict(self, text: str) -> str:
        """Predict intent for a given input string."""
        inputs = self._tokenizer(text, return_tensors="pt")

        with torch.no_grad():
            outputs = self._model(**inputs)
            logits = outputs.logits
            predictions = torch.argmax(logits, dim=-1)

        return self._id2label[predictions.item()]

