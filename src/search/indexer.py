"""
Crea el índice en Azure AI Search e indexa los documentos de data/docs/.

Uso:
    python -m src.search.indexer
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    SimpleField,
    SearchableField,
)
from azure.core.credentials import AzureKeyCredential

load_dotenv(Path("config/.env"))

ENDPOINT  = os.environ["AZURE_SEARCH_ENDPOINT"]
KEY       = os.environ["AZURE_SEARCH_KEY"]
INDEX     = "walmart-docs"


def create_index():
    client = SearchIndexClient(ENDPOINT, AzureKeyCredential(KEY))
    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="title", type=SearchFieldDataType.String),
        SearchableField(name="content", type=SearchFieldDataType.String),
        SimpleField(name="source", type=SearchFieldDataType.String),
    ]
    index = SearchIndex(name=INDEX, fields=fields)
    client.create_or_update_index(index)
    print("✅ Índice creado")


def load_documents():
    docs_path = Path("data/docs")
    documents = []
    for i, file in enumerate(docs_path.glob("*.md")):
        content = file.read_text(encoding="utf-8")
        documents.append({
            "id": str(i),
            "title": file.stem,
            "content": content,
            "source": file.name,
        })
    return documents


def index_documents(documents):
    client = SearchClient(ENDPOINT, INDEX, AzureKeyCredential(KEY))
    result = client.upload_documents(documents)
    print(f"✅ {len(documents)} documentos indexados")
    return result


def main():
    print("🔧 Creando índice en Azure AI Search...")
    create_index()

    print("\n📄 Cargando documentos...")
    documents = load_documents()
    print(f"   Encontrados: {len(documents)} documentos")

    print("\n📤 Indexando documentos...")
    index_documents(documents)

    print("\n✅ Bloque 9 — Indexación completada.")
    print(f"🔗 Índice: {INDEX}")
    print(f"🔗 Endpoint: {ENDPOINT}")


if __name__ == "__main__":
    main()