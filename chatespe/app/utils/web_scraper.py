import os
import faiss
import numpy as np
import pandas as pd
from app.utils.embedding import embed_text_mini
from rapidfuzz import process, fuzz
from sentence_transformers import SentenceTransformer
from app.utils.web_search import search_espe_website  # Ahora desde web_search.py
from flask import Flask, request, jsonify


# Configuración del entorno
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Inicializar la aplicación Flask
app = Flask(__name__)

# Inicializar el modelo de embeddings
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Cargar preguntas y respuestas desde el FAQ
def load_faiss():
    data = pd.read_csv('faq.csv')
    questions = data['question'].tolist()
    answers = data['answer'].tolist()

    # Generar los embeddings asegurando que el array sea bidimensional
    embeddings = np.array([model.encode(q) for q in questions])

    if len(embeddings.shape) != 2:
        raise ValueError(f"Los embeddings deben ser bidimensionales, pero tienen forma {embeddings.shape}")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index, questions, answers

index, questions, answers = load_faiss()

# Normalización básica de la consulta
def normalize_query(query):
    if not query:
        return ""

    query = query.lower().strip()
    query = query.replace(" u ", " universidad ")
    return query

# Función para buscar en el FAQ utilizando embeddings y coincidencia difusa
def search_faq(query):
    query_lower = normalize_query(query)
    
    if not query_lower:
        return "Lo siento, no pude entender tu pregunta. Intenta reformularla."

    print(f"Buscando en FAQ: {query_lower}")

    # Embedding de la consulta
    query_embedding = model.encode(query_lower).reshape(1, -1)

    # Buscar el embedding más cercano en FAISS
    D, I = index.search(query_embedding, 5)
    best_match_index = I[0][0]
    best_match_distance = D[0][0]

    if best_match_distance < 0.5:
        return answers[best_match_index]

    # Coincidencia difusa
    best_matches = process.extract(query_lower, questions, scorer=fuzz.token_sort_ratio, limit=5)
    best_match = max(best_matches, key=lambda x: x[1])
    match_question, score, _ = best_match

    if score > 70:
        return answers[questions.index(match_question)]

    return None  # Aquí devolvemos None si no se encuentra en el FAQ

# Función para manejar preguntas
def handle_question(user_question):
    if not user_question:
        return "Por favor, ingresa una pregunta válida."

    # Buscar en FAQ
    faq_response = search_faq(user_question)
    if faq_response:  # Si se encuentra en el FAQ, devolver esa respuesta
        return faq_response

    # Si no se encuentra en el FAQ, buscar en el sitio web
    web_response = search_espe_website(user_question)
    if web_response:  # Si se encuentra en el sitio web, devolver esa respuesta
        return web_response

    # Si no se encuentra en ninguna parte, devolver este mensaje
    return "Lo siento, no pude encontrar una respuesta para tu pregunta ni en el FAQ ni en el sitio web de la ESPE. Por favor, intenta con otra pregunta."

# Ruta para recibir preguntas
@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        data = request.json
        user_question = data.get('question', '')
        response = handle_question(user_question)
        return jsonify({'response': response})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'response': "Lo siento, ocurrió un error mientras procesaba tu solicitud. Intenta de nuevo más tarde."}), 500

# Error handler global
@app.errorhandler(Exception)
def handle_exception(e):
    print(f"Error no manejado: {e}")
    return jsonify({'response': "Lo siento, ocurrió un error mientras procesaba tu solicitud. Intenta de nuevo más tarde."}), 500

if __name__ == '__main__':
    app.run(debug=True)
