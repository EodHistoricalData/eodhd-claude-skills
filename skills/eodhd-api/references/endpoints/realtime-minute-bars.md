# Real-Time Minute Bars (`/history`)

Path: `/history` on the real-time host `https://ws.eodhistoricaldata.com` — **not** on
`https://eodhd.com/api` like the rest of the REST surface.

```
GET https://ws.eodhistoricaldata.com/history?market={us|eu}&symbol={symbol}&api_token=YOUR_API_KEY
```

Returns the recent **closed** one-minute OHLCV bars the real-time service holds for a single
symbol. This is the answer to a WebSocket stream that dropped: fill the gap here rather than
waiting for the streams to rebuild.

## Parameters

| Name | Required | Notes |
|---|---|---|
| `market` | yes | `us` or `eu`. Only the Cboe equity markets keep bars. |
| `symbol` | yes | Same form used to subscribe: plain ticker for US (`AAPL`), `TICKER.EXCHANGE` for Europe (`GSK.LSE`). The native Cboe symbol and the un-hyphenated alias of a dual-class ticker (`ERICB.ST` for `ERIC-B.ST`) are both accepted. |
| `api_token` | yes | Standard token. |

## Response

A JSON array of bars, oldest first:

```json
[
  {"s":"AAPL","i":"1m","t":1787701620000,"o":309.32,"h":309.32,"l":309.31,"c":309.31,"v":223},
  {"s":"AAPL","i":"1m","t":1787701680000,"o":309.31,"h":309.36,"l":309.29,"c":309.36,"v":418}
]
```

- `s` is the **canonical EODHD ticker**, whichever form was requested.
- `i` is the interval, `1m`.
- `t` is the bar **OPEN** time, epoch milliseconds UTC.
- `c` is the **close price** here. On the trade streams `c` is the conditions array instead.

## Two properties that read as bugs and are not

**The array is sparse.** Only minutes in which the symbol actually traded produce a bar, so a
quiet name returns a handful of bars spanning hours rather than one bar per consecutive minute.
Measured: AAPL returned 37 bars across 547 minutes.

**Empty results are not errors.** An unknown market, an unknown symbol, and the `crypto` and
`forex` markets — which keep no bars at all — every one of them returns `[]` with HTTP 200.

## Errors

Authentication failures use the key `status`, not `status_code`:

```json
{"status": 403, "message": "Server error"}
{"status": 422, "message": "Server error"}
```

which is the same shape the WebSocket path uses, and deliberately generic — the endpoint used
to echo the caller's token back in this message.

## Why the client does not implement this

`eodhd_client.py` targets `BASE_URL` (`https://eodhd.com/api`). This endpoint lives on a
different host, so the registry entry is `support_tier: documented` with
`client_endpoint: null` rather than pretending the client can reach it. Call it directly, or
pass `--base-url https://ws.eodhistoricaldata.com`.

## See also

- `websockets-realtime.md` — the streams this backfills, including the minute-bar stream
- Public documentation: https://eodhd.com/financial-apis/new-real-time-data-api-websockets
