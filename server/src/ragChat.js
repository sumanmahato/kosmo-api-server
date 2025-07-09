// ragChat.js
import { Chroma } from "langchain/vectorstores/chroma";
import { OllamaEmbedder } from "./ollamaEmbedder.js";
import { executeLLM } from "./llm-util.js"; // your existing LLM executor

async function ragChat(userQuery) {
  try {
    // Step 1: Load existing Chroma vector store
    const vectorStore = await Chroma.fromExistingCollection(
      new OllamaEmbedder(),
      {
        collectionName: "demo-context", // match what you used in embedContext.js
        url: "http://localhost:8000", // Chroma server URL
      }
    );

    // Step 2: Retrieve relevant docs based on query
    const retriever = vectorStore.asRetriever();
    const docs = await retriever.getRelevantDocuments(userQuery);

    // Step 3: Combine retrieved docs into a single context string
    const context = docs.map((doc) => doc.pageContent).join("\n\n");

    // Step 4: Build the final prompt for LLM
    const prompt = `Answer the question based on the context below.\n\nContext:\n${context}\n\nQuestion: ${userQuery}\nAnswer:`;

    // Step 5: Run it through Ollama
    const response = await executeLLM(prompt);

    return response;
  } catch (err) {
    console.error("RAG Error:", err);
    return "Sorry, I couldn't retrieve an answer at the moment.";
  }
}

module.exports = { ragChat };
