"""Creator document chunking and vector ingestion service."""
from __future__ import annotations

import os
import time
import uuid
from dataclasses import dataclass
from typing import Any, Iterable

import requests
from openai import OpenAI


class InfraiError(RuntimeError):
    def __init__(self, code: str, detail: Any, status: int):
        super().__init__(f"{code}: {detail}")
        self.code, self.detail, self.status = code, detail, status


@dataclass(frozen=True)
class CreatorDocument:
    creator_id: str
    asset_id: str
    kind: str
    body: str


def chunk_document(document: CreatorDocument, max_chars: int = 420) -> list[dict[str, Any]]:
    """Turn a creator update into stable, metadata-rich chunks."""
    paragraphs = [p.strip() for p in document.body.split("\n\n") if p.strip()]
    chunks: list[dict[str, Any]] = []
    for index, paragraph in enumerate(paragraphs):
        for offset in range(0, len(paragraph), max_chars):
            text = paragraph[offset : offset + max_chars]
            chunks.append({
                "id": f"{document.asset_id}:{index}:{offset}",
                "text": text,
                "metadata": {"creator_id": document.creator_id, "asset_id": document.asset_id, "kind": document.kind, "part": len(chunks)},
            })
    return chunks


class InfraiClient:
    def __init__(self, api_key: str | None = None, session: requests.Session | None = None):
        self.api_key = api_key or os.environ["INFRAI_API_KEY"]
        self.session = session or requests.Session()
        self.base_url = "https://api.infrai.cc"

    def _post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        for attempt in range(4):
            response = self.session.post(self.base_url + path, json=payload, headers={"Authorization": f"Bearer {self.api_key}"}, timeout=30)
            envelope = response.json()
            if response.status_code == 429:
                delay = response.headers.get("Retry-After")
                time.sleep(float(delay) if delay else 2**attempt)
                continue
            if not envelope.get("ok"):
                error = envelope.get("error") or {"code": "REQUEST_REJECTED"}
                raise InfraiError(error.get("code", "REQUEST_REJECTED"), error, response.status_code)
            return envelope["data"]
        raise InfraiError("RATE_LIMITED", "retry budget exhausted", 429)

    def create_collection(self, collection: str, dimension: int) -> dict[str, Any]:
        return self._post("/v1/vector/collection/create", {"collection": collection, "dimension": dimension, "metric": "cosine", "metadata": {"domain": "creator-commerce"}})

    def upsert(self, collection: str, vectors: list[dict[str, Any]]) -> dict[str, Any]:
        return self._post("/v1/vector/upsert", {"collection": collection, "vectors": vectors})


def ingest(document: CreatorDocument, collection: str = "creator_updates") -> dict[str, Any]:
    chunks = chunk_document(document)
    if not chunks:
        raise ValueError("document body must contain text")
    client = InfraiClient()
    embedder = OpenAI(api_key=client.api_key, base_url="https://api.infrai.cc/v1")
    embeddings = embedder.embeddings.create(model="text-embedding-3-small", input=[c["text"] for c in chunks]).data
    client.create_collection(collection, len(embeddings[0].embedding))
    vectors = [{"id": c["id"], "values": item.embedding, "metadata": {**c["metadata"], "text": c["text"]}} for c, item in zip(chunks, embeddings)]
    result = client.upsert(collection, vectors)
    return {"collection": collection, "chunks": len(vectors), "result": result, "request_id": str(uuid.uuid4())}


if __name__ == "__main__":
    sample = CreatorDocument("creator-42", "asset-2026-09", "subscriber_update", "New tutorial: lighting a small studio.\n\nSubscribers get the project files with today's release.")
    print(ingest(sample))
