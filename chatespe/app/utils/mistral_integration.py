import subprocess

def generate_response_mistral(query):
    try:
        script = f"""
        const MistralClient = require('@mistralai/mistralai');

        const token = process.env["GITHUB_TOKEN"];
        const endpoint = "https://models.inference.ai.azure.com";
        const modelName = "Mistral-large";

        async function main() {{
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

        with open("mistral_query.js", "w") as file:
            file.write(script)

        result = subprocess.run(["node", "mistral_query.js"], capture_output=True, text=True)

        if result.returncode != 0:
            return "Lo siento, hubo un error procesando tu pregunta."

        response = result.stdout.strip()
        return response if response else "Lo siento, no pude generar una respuesta."
    
    except Exception as e:
        print(f"Error en generate_response_mistral: {str(e)}")
        return "Lo siento, hubo un problema al generar la respuesta."
