import torch
from transformers import BertTokenizer, BertForQuestionAnswering

# Cargar el modelo y el tokenizador
tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

def generate_response_bert(question, context=""):
    inputs = tokenizer(question, context, return_tensors='pt')
    
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Obtener el índice de la respuesta más probable
    answer_start_index = torch.argmax(outputs.start_logits)
    answer_end_index = torch.argmax(outputs.end_logits) + 1
    
    # Convertir los tokens en la respuesta
    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs['input_ids'][0][answer_start_index:answer_end_index]))
    
    # Manejar respuestas vacías
    if not answer.strip() or answer == "[SEP]":
        return "Lo siento, no pude encontrar una respuesta adecuada."
    
    return answer.strip()  # Eliminar espacios en blanco
