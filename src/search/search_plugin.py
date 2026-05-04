"""
Plugin de Azure AI Search para el agente conversacional.
Permite al agente buscar en documentos indexados antes de responder.
"""
import os
from typing import Annotated
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from semantic_kernel.functions import kernel_function


class SearchPlugin:
    """Plugin que busca información en el índice de Azure AI Search."""

    def __init__(self):
        self.client = SearchClient(
            endpoint=os.environ["AZURE_SEARCH_ENDPOINT"],
            index_name="walmart-docs",
            credential=AzureKeyCredential(os.environ["AZURE_SEARCH_KEY"]),
        )

    @kernel_function(
        description="Busca información en documentos de contexto de negocio. "
                    "Úsalo cuando el usuario pregunte sobre estrategia, métricas, "
                    "interpretación de resultados, clusters o información general de Walmart."
    )
    def search(
        self,
        query: Annotated[str, "Pregunta o término a buscar en los documentos"],
    ) -> Annotated[str, "Información relevante encontrada en los documentos"]:
        results = self.client.search(query, top=2)
        output = []
        for r in results:
            output.append(f"### {r['title']}\n{r['content'][:800]}")
        if not output:
            return "No encontré información relevante en los documentos."
        return "\n\n".join(output)