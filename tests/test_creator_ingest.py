from src.creator_ingest import CreatorDocument, chunk_document


def test_subscriber_update_keeps_delivery_metadata_and_chunk_order():
    document = CreatorDocument("c-7", "bundle-3", "subscriber_update", "First note.\n\nDownload instructions are in the second note.")
    chunks = chunk_document(document, max_chars=100)
    assert [chunk["id"] for chunk in chunks] == ["bundle-3:0:0", "bundle-3:1:0"]
    assert chunks[1]["metadata"] == {"creator_id": "c-7", "asset_id": "bundle-3", "kind": "subscriber_update", "part": 1}
    assert chunks[1]["text"].startswith("Download instructions")
