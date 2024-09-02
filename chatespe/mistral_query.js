
        const MistralClient = require('@mistralai/mistralai');

        const token = process.env["GITHUB_TOKEN"];
        const endpoint = "https://models.inference.ai.azure.com";
        const modelName = "Mistral-large";

        async function main() {
            const client = new MistralClient(token, endpoint);
            try {
                const response = await client.chat({
                    model: modelName,
                    messages: [
                        { role:"system", content: "You are a helpful assistant." },
                        { role:"user", content: "filosofia institucional de la universidad espe" }
                    ],
                    temperature: 1.,
                    max_tokens: 1000,
                    top_p: 1.
                });
                console.log(response.choices[0].message.content);
            } catch (error) {
                console.error("Error llamando a Mistral:", error);
            }
        }

        main().catch((err) => {
            console.error("Error ejecutando el script principal:", err);
        });
        