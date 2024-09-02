import re

# Función para verificar si la pregunta está vacía
def is_empty_question(question):
    return not question or question.strip() == ""

# Función para manejar saludos y despedidas
def handle_greeting_or_farewell(question):
    greetings = ['hola', 'buenos dias', 'buenas tardes', 'buenas noches']
    farewells = ['adios', 'hasta luego', 'chau', 'nos vemos']
    
    question_lower = question.lower()
    
    if any(greeting in question_lower for greeting in greetings):
        return "¡Hola! ¿Como puedo ayudarte hoy?"
    
    if any(farewell in question_lower for farewell in farewells):
        return "¡Hasta luego! Que tengas un buen día."
    
    return None  # No es un saludo ni una despedida

# Función para validar preguntas con sentido
def is_valid_question(question):
    return len(re.findall(r'\w+', question)) >= 3  # Al menos 3 palabras
