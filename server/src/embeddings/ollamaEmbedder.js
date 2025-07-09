// OllamaEmbedder.js
import fetch from "node-fetch";
import { EmbeddingsInterface } from "langchain/schema/embeddings";

export class OllamaEmbedder extends EmbeddingsInterface {
  constructor(options = {}) {
    super();
    this.model = options.model || "nomic-embed-text";
    this.baseUrl = options.baseUrl || "http://localhost:11434";
  }

  async embedQuery(text) {
    const response = await fetch(`${this.baseUrl}/api/embeddings`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ model: this.model, prompt: text }),
    });

    if (!response.ok) throw new Error("Failed to get embedding from Ollama");

    const data = await response.json();
    return data.embedding;
  }

  async embedDocuments(texts) {
    const embeddings = [];
    for (const text of texts) {
      const vector = await this.embedQuery(text);
      embeddings.push(vector);
    }
    return embeddings;
  }
}
