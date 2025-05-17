import numpy as np
import openai
import hnswlib

from services.imindexsearch.base import (
    IInMemoryIndexDB,
    IndexDBDocument,
    IndexDBDocumentResult
)


class HNSWInMemoryIndexDB(IInMemoryIndexDB):
    def __init__(self, space: str = "cosine", ef_construction: int = 200, m: int = 16) -> None:
        self._space = space
        self._ef_construction = ef_construction
        self._m = m

        self._documents: dict[int, IndexDBDocument] = {}

    def add(self, reference: str, text: str, embedding: np.ndarray) -> None:
        start_id = len(self._documents)
        self._documents[start_id] = IndexDBDocument(
            id=start_id,
            reference=reference,
            text=text,
            embedding=embedding
        )

    def add_batch(self, reference: str, texts: list[str], embeddings: np.ndarray[np.ndarray]) -> None:
        start_id = len(self._documents)
        self._documents |= {
            (start_id + i): IndexDBDocument(
                id=start_id + i,
                reference=reference,
                text=texts[i],
                embedding=embeddings[i]
            )
            for i in range(0, len(texts))
        }

    def search(self, query: str, k: int = 5, as_dict: bool = False) -> list[IndexDBDocumentResult] | list[dict]:
        if len(self._documents) == 0 or len(query) == 0:
            return []

        query_embedding = self._embed_query(query)
        ids, embeddings = zip(*[(doc.id, doc.embedding) for doc in self._documents.values()])

        index = self._create_index(ids, embeddings)
        labels, distances = index.knn_query(query_embedding, k=k)
        results = zip(labels[0], distances[0])

        if as_dict:
            return [self._documents[label].to_result_dict(query, distance) for label, distance in results]
        return [self._documents[label].to_result(query, distance) for label, distance in results]

    def _create_index(self, ids: list[int], embeddings: list[np.ndarray]) -> hnswlib.Index:
        index = hnswlib.Index(space=self._space, dim=embeddings[0].shape[0])

        index.init_index(max_elements=len(ids), ef_construction=self._ef_construction, M=self._m)
        index.add_items(embeddings, ids)

        return index

    def _embed_query(self, query: str) -> np.ndarray:
        response = openai.embeddings.create(
            input=query,
            model="text-embedding-3-large"
        )

        embedding = np.array([record.embedding for record in response.data], dtype=np.float32)

        return embedding
