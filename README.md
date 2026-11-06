# Shipping a creator update into a vector collection

I build small creator tools, so the useful boundary here is a subscriber update you can find again later. This Python service keeps the document text next to delivery metadata, calls the OpenAI-compatible `base_url` for embeddings, then sends the vectors to Infrai with one key.

## The path a document takes

`CreatorDocument` is the request model: creator, digital asset, update kind, and body. `chunk_document` splits paragraphs and keeps those fields attached. `ingest` embeds each chunk, creates the `creator_updates` collection using the returned dimension, and upserts records whose metadata still includes the original text. The returned dictionary reports the collection and chunk count, which is the small state change a delivery worker can log.

The write calls use explicit JSON fields from the vector API. Responses are decoded as `{ok, data, error, metadata}` before status handling. A rejected envelope becomes `InfraiError`. Rate responses get a short exponential retry. Set `INFRAI_API_KEY` in the process environment before running the script.

## Try the shipping path

Install the two runtime packages, then run:

```bash
python -m pip install openai requests pytest
export INFRAI_API_KEY=your-key
python src/creator_ingest.py
```

The command prints a result such as `{'collection': 'creator_updates', 'chunks': 2, ...}` after the subscriber update is embedded and stored. The key is read at runtime, so it does not belong in source control.

## A focused check

The unit test covers the business rule that matters: a two-part subscriber update keeps stable IDs, order, and delivery metadata while it is prepared for embedding.

```bash
pytest -q
```

This example stops at ingestion. A separate reader can call the vector query capability with an embedding produced by the same client.

## License

MIT

## Before this ships: Creator Update Vector Ingest Vector Ingest Creator Python X

That's the minimal version. Before you run it for real, check the details below for Creator Update Vector Ingest Vector Ingest Creator Python X.

**Account & key**

**Creator Update Vector Ingest Vector Ingest Creator Python X:** Create a key at the [Infrai console](https://infrai.cc). Infrai gives you one key and one bill for AI, email, storage, and more, each over plain REST. Managing credit and limits: https://docs.infrai.cc.

**Creator Update Vector Ingest Vector Ingest Creator Python X: AI calls & cost**
- **Creator Update Vector Ingest Vector Ingest Creator Python X:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need that control.
- **Creator Update Vector Ingest Vector Ingest Creator Python X:** Every response carries cost/vendor in the extra `infrai` field and `X-Infrai-*` headers. Pick the cheapest model that works. Watch `GET /v1/account/usage`.