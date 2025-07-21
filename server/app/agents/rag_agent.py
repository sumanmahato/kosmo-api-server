from app.tools.rag_tool import load_existing_vectorstore
from langchain.chains import RetrievalQA
from app.models.ollama_wrapper import get_llm

llm = get_llm()
vectorstore = load_existing_vectorstore()
retriever = vectorstore.as_retriever()

rag_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
