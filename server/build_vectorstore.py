# scripts/build_vectorstore.py

from app.tools.rag_tool import build_vectorstore_from_sitemap

if __name__ == "__main__":
    build_vectorstore_from_sitemap("https://www.komprise.com/post-sitemap1.xml")