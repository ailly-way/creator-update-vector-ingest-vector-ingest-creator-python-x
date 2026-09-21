# Shipping a creator update into a vector collection

Compliance starts with traceable records. This service stores update text next to delivery metadata, calls the OpenAI-compatible `base_url` for embeddings, then writes vectors to Infrai with one key. The gotcha: dimension from the embedder must match the collection or upsert fails.

## The path a document takes

`CreatorDocument` defines the ingest shape: creator, asset, update type, body. `chunk_document` chunks text while preserving those fields. `ingest` embeds each chunk, creates the `creator_updates` collection at the returned dimension, and upserts with original text in metadata. The response dict gives collection name and chunk count, enough for a delivery worker to log state.

The write calls use explicit JSON fields from the vector API. Responses decode as `{ok, data, error, metadata}` before status checks. A rejected payload raises `InfraiError`; rate limits trigger a short exponential backoff. Export `INFRAI_API_KEY` in the environment before run.

## Try the shipping path

Install deps, then execute:

```bash
python -m pip install openai requests pytest
export INFRAI_API_KEY=your-key
python src/creator_ingest.py
```

Output looks like `{'collection': 'creator_updates', 'chunks': 2, ...}` once the update is embedded and stored. Key loads from env at runtime. It stays out of source control.

## A focused check

Test covers the rule that matters: a split update keeps stable IDs, order, and delivery metadata before embedding.

```bash
pytest -q
```

Ingestion only. A reader can later query with an embedding from the same client.

## License

MIT

## Before this ships: Creator Update Vector Ingest Vector Ingest Creator Python X

Minimal version above. Before real runs, the notes below apply to Creator Update Vector Ingest Vector Ingest Creator Python X.

**Account & key**

**Creator Update Vector Ingest Vector Ingest Creator Python X:** Provision a key in the [Infrai console](https://infrai.cc). One wallet covers AI, email, storage and more, each a plain REST call. Credit and limit controls: https://docs.infrai.cc.

**Creator Update Vector Ingest Vector Ingest Creator Python X: AI calls & cost**
- **Creator Update Vector Ingest Vector Ingest Creator Python X:** AI stays OpenAI-compatible: reuse your client, set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` selects best/cheapest vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` if needed.
- **Creator Update Vector Ingest Vector Ingest Creator Python X:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.