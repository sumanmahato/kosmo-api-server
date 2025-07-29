from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from app.models.ollama_wrapper import get_llm
from app.tools.rag_tools.vectorstore import load_existing_vectorstore

class RAGPipeline:
    def __init__(self, k=5):
        # Load LLM and VectorStore
        self.llm = get_llm()
        self.vectorstore = load_existing_vectorstore()
        self.retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k}
        )

        # Define HTML-aware Prompt
        self.prompt = PromptTemplate(
            input_variables=["query", "summary", "history", "context"],
            template="""
You are a helpful assistant that answers user questions using retrieved internal content.

Instructions:
- Format your response using valid HTML tags.
- Use <p> for paragraphs, <b> for emphasis, <ul>/<li> for bullet points.
- Do NOT include any links or URLs — not even as plain text.
- Do NOT reference external documentation (like "see docs" or "visit...").
- Use only the provided context and history to answer.
- If an answer is not found in the context, say "No information available" or similar.

[Conversation Summary]
{summary}

[Conversation History]
{history}

[User Question]
{query}

[Relevant Context]
{context}

Respond with well-formatted HTML only.
""".strip()
        )

        # Answer Generator
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def run(self, query: str, summary: str = "", history: str = "") -> dict:
        # Step 1: Retrieve relevant documents
        docs = self.retriever.get_relevant_documents(query)
        context = "\n\n".join(doc.page_content for doc in docs)

        print(f"[RAGPipeline] Retrieved {len(docs)} documents.")
        for i, doc in enumerate(docs, 1):
            print(f"\n[CHUNK {i}]\n{doc.page_content}")
            print(f"[Source] {doc.metadata.get('source', 'Unknown')}")

        # Step 2: Generate answer with context + history + summary
        response = self.chain.run({
            "query": query,
            "summary": summary.strip(),
            "history": history,
            "context": context.strip()
        })

        return {
            "answer": response,
            "sources": [doc.metadata for doc in docs]
        }