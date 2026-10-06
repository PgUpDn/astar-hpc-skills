# Institutional LLM gateways

Obtain the approved gateway URL, API protocol, key and permitted model IDs from the service owner. Endpoints and model rosters are configurable; no private host, account-specific key location or historical model list is embedded here.

For an OpenAI-compatible gateway, the bundled helper accepts `ACRC_GATEWAY_BASE_URL` (origin or URL ending in `/v1`) and `ACRC_GATEWAY_API_KEY`. Load them from your private configuration only when needed, with shell tracing disabled. Keep credential files outside this repository and restrict their permissions. Scheduler jobs can inherit the submitter's exported environment, so load keys only in the process that needs them.

```bash
# With the two variables already provided by your private credential mechanism:
python3 scripts/gateway_check.py
# When a small inference check is requested; use a currently available model ID:
python3 scripts/gateway_check.py REPLACE_MODEL_ID
```

The helper requires HTTPS, does not follow redirects, and does not print keys or raw error bodies. Listing models verifies only the listing path. One successful completion is stronger evidence, but does not prove sustained availability. A completion probe consumes service capacity.

## Client and proxy diagnosis

Confirm whether the backend supports Chat Completions, Responses or Anthropic Messages before choosing an adapter. Preserve message roles and tool semantics; do not silently rewrite system messages to work around a bridge bug. Check current adapter documentation and installed version for relevant configuration.

For an authorized per-job proxy, bind to loopback, use a distinct port and run directory, isolate client configuration, keep the upstream key only in the proxy process, and stop the proxy when the job ends. Model routing should be explicit; do not silently map unexpected models to a different backend. Existing client settings may override environment variables, so inspect the effective endpoint without printing credentials.

Reasoning models may consume an output budget before producing visible text. Inspect finish reason and usage before treating empty content as an outage. For 401/403 check credentials and entitlement; for 400 inspect protocol/schema; for 5xx use bounded backoff and preserve the failure. Do not launch repeated job waves during a known outage or cancel/relaunch workloads without authorization.
