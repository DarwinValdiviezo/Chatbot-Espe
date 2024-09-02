import torch
from transformers import BertTokenizer, BertForSequenceClassification

# Cargar el modelo y el tokenizador
tokenizer = BertTokenizer.from_pretrained('dccuchile/bert-base-spanish-wwm-cased')
model = BertForSequenceClassification.from_pretrained('path/to/your/saved/model')  # Asegúrate de reemplazar con la ruta correcta

def generate_response_bert(question, context=None):
    inputs = tokenizer(question, context, return_tensors="pt", padding=True, truncation=True)
    outputs = model(**inputs)
    answer_start_scores = outputs.start_logits
    answer_end_scores = outputs.end_logits

    # Get the most likely beginning and end of answer
    answer_start = torch.argmax(answer_start_scores)
    answer_end = torch.argmax(answer_end_scores) + 1

    # Convert tokens to string
    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs['input_ids'][0][answer_start:answer_end]))

    return answer.strip()  # Eliminar posibles espacios en blanco adicionales


