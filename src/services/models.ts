import OpenAI from "openai";

// Inicializando o cliente apontando para a base URL do OpenRouter
const openai = new OpenAI({
  baseURL: "https://openrouter.ai/api/v1",
  apiKey: import.meta.env.VITE_OPENROUTER_API_KEY,
  dangerouslyAllowBrowser: true,
  defaultHeaders: {
    // Opcional, mas recomendado pelo OpenRouter para métricas de uso
    "HTTP-Referer": process.env.SITE_URL || "http://localhost:3000",
    "X-Title": process.env.SITE_NAME || "MyPetApp",
  },
});

export async function petVisionAnalysis(base64Image: string) {
  const response = await openai.chat.completions.create({

    model: "baidu/qianfan-ocr-fast:free", 
    messages: [
      {
        role: "user",
        content: [
          {
            type: "text",
            text: "Analyze this image of a pet and return a JSON object with the following fields: species, breed (if identifiable, else 'unknown'), primaryColor, distinguishingMarks (brief description), and likelyMood (one word). Be concise. You must return ONLY valid JSON.",
          },
          {
            type: "image_url",
            image_url: {
              // A API da OpenAI/OpenRouter exige o prefixo do Data URI para imagens base64
              url: `data:image/jpeg;base64,${base64Image}`,
            },
          },
        ],
      },
    ],
    // Força a saída como JSON (suportado pela maioria dos modelos modernos no OpenRouter)
    response_format: { type: "json_object" },
  });

  const content = response.choices[0].message?.content;
  if (!content) {
    throw new Error("Falha ao gerar o conteúdo a partir da imagem.");
  }

  return JSON.parse(content);
}

export async function generateEmbedding(base64Image: string) {
  // Mantendo a mesma lógica da sua implementação original:
  // Gera a descrição em texto primeiro e depois faz o embedding
  const visionData = await petVisionAnalysis(base64Image);
  const textToEmbed = `${visionData.species} ${visionData.breed} ${visionData.primaryColor} ${visionData.distinguishingMarks}`;
  
  const response = await openai.embeddings.create({
    // Escolha um modelo de embedding disponível no OpenRouter
    // "openai/text-embedding-3-small" ou "nomic-ai/nomic-embed-text-v1.5" são ótimas opções
    model: "openai/text-embedding-3-small",
    input: textToEmbed,
  });

  return response.data[0].embedding;
}