# scripts/build_vectorstore.py

from app.tools.vectorstore_loader import build_vectorstore

if __name__ == "__main__":
    build_vectorstore("app/data")