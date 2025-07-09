import { Chroma } from "langchain/vectorstores/chroma";
import { OllamaEmbedder } from "./ollamaEmbedder";
import { Document } from "langchain/document";
import fs from "fs/promises";

const rawContent = await fs.readFile("../mock-data/context.txt", "utf8");

// Wrap in a LangChain Document
const docs = [new Document({ pageContent: rawContent })];

// Embed using nomic-embed-text via Ollama
const embeddings = new OllamaEmbedder();

// Store in Chroma
const vectorStore = await Chroma.fromDocuments(docs, embeddings, {
  collectionName: "demo-context",
  url: "http://localhost:8000",
});

console.log("context.txt embedded and stored in Chroma.");
