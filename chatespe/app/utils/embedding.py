import os
import subprocess
import torch
from transformers import AutoTokenizer, AutoModel

# Cargar el modelo y tokenizador de All-MiniLM-L6-v2
tokenizer_mini = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model_mini = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

def embed_text_mini(text):
    inputs = tokenizer_mini(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        embeddings = model_mini(**inputs).last_hidden_state[:, 0, :].numpy()
    return embeddings

def generate_response_mistral(query):
    try:
        # Definir el script JS para llamar a Mistral
        script = f"""
        import MistralClient from '@mistralai/mistralai';

        const token = process.env["GITHUB_TOKEN"];
        const endpoint = "https://models.inference.ai.azure.com";
        const modelName = "Mistral-large";

        export async function main() {{
            const client = new MistralClient(token, endpoint);
            try {{
                const response = await client.chat({{
                    model: modelName,
                    messages: [
                        {{ role:"system", content: "You are a helpful assistant." }},
                        {{ role:"user", content: "{query}" }}
                    ],
                    temperature: 1.,
                    max_tokens: 1000,
                    top_p: 1.
                }});
                console.log(response.choices[0].message.content);
            }} catch (error) {{
                console.error("Error llamando a Mistral:", error);
            }}
        }}

        main().catch((err) => {{
            console.error("Error ejecutando el script principal:", err);
        }});
        """

        # Guardar el script JS temporalmente
        with open("mistral_query.js", "w") as file:
            file.write(script)

        # Ejecutar el script JS usando Node.js
        result = subprocess.run(["node", "mistral_query.js"], capture_output=True, text=True)

        # Verificar la salida y manejar posibles errores
        if result.returncode != 0:
            print("Error ejecutando el script de Mistral:", result.stderr)
            return "Lo siento, hubo un error procesando tu pregunta."

        response = result.stdout.strip()
        print(f"Respuesta de Mistral: {response}")
        return response if response else "Lo siento, no pude generar una respuesta."
    
    except Exception as e:
        print(f"Error en generate_response_mistral: {str(e)}")
        return "Lo siento, hubo un problema al generar la respuesta."

