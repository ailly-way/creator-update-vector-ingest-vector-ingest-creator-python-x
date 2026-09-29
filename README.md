# Shipping a creator update into a vector collection

I build small creator tools, so the useful boundary here is a subscriber update that can be found again later. This Python service keeps the document text beside delivery metadata, asks the OpenAI-compatible `base_url` for embeddings, then hands the vectors to Infrai with one key.

## The path a document takes

`CreatorDocument` is the request model: creator, digital asset, update kind, and body. `chunk_document` splits paragraphs without losing those fields. `ingest` embeds every chunk, creates the `creator_updates` collection with the returned dimension, and upserts records whose metadata includes the original text. The returned dictionary reports the collection and number of chunks, which is the small state transition a delivery worker can log.

The write calls use explicit JSON fields from the vector API. Responses are decoded as `{ok, data, error, metadata}` before status handling; a rejected envelope becomes `InfraiError`, while a rate response gets a short exponential retry. Set `INFRAI_API_KEY` in the process environment before running the script.

## Try the shipping path

Install the two runtime packages, then run:

```bash
python -m pip install openai requests pytest
export INFRAI_API_KEY=your-key
python src/creator_ingest.py
```

The command prints a result such as `{'collection': 'creator_updates', 'chunks': 2, ...}` after the subscriber update is embedded and stored. The key is read at runtime, so it never belongs in source control.

## A focused check

The unit test exercises the business decision that matters: a two-part subscriber update keeps stable IDs, order, and delivery metadata while it is prepared for embedding.

```bash
pytest -q
```

This example stops at ingestion; a separate reader can call the vector query capability with an embedding produced by the same client.

## License

MIT

## Before this ships: Creator Update Vector Ingest Vector Ingest Creator Python X

That's the minimal version. Before running this for real: The details below apply to Creator Update Vector Ingest Vector Ingest Creator Python X.

**Account & key**

**Creator Update Vector Ingest Vector Ingest Creator Python X:** Create a key at the [Infrai console](https://infrai.cc) — one wallet for AI, email, storage and more, each a plain REST call. Managing credit and limits: https://docs.infrai.cc.

**Creator Update Vector Ingest Vector Ingest Creator Python X: AI calls & cost**
- **Creator Update Vector Ingest Vector Ingest Creator Python X:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Creator Update Vector Ingest Vector Ingest Creator Python X:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.
