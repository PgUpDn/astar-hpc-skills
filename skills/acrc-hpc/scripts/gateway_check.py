#!/usr/bin/env python3
"""List gateway models; an optional model argument makes one small inference call.
Credentials: ACRC_GATEWAY_BASE_URL and ACRC_GATEWAY_API_KEY in the environment.
Uses stdlib HTTPS with normal certificate validation; no redirects or raw errors.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def check(model=None):
    base = os.environ.get("ACRC_GATEWAY_BASE_URL", "").rstrip("/")
    key = os.environ.get("ACRC_GATEWAY_API_KEY", "")
    parts = urllib.parse.urlsplit(base)
    if (parts.scheme != "https" or not parts.hostname or parts.username or
            parts.password or parts.query or parts.fragment or not key or
            any(c in key for c in "\r\n")):
        print("Provide an HTTPS gateway URL without embedded credentials and a valid key.", file=sys.stderr)
        return 2
    if not base.endswith("/v1"):
        base += "/v1"
    opener = urllib.request.build_opener(NoRedirect())

    def request(path, payload=None):
        data = None if payload is None else json.dumps(payload).encode()
        req = urllib.request.Request(base + path, data=data, headers={
            "Authorization": "Bearer " + key, "Content-Type": "application/json"})
        try:
            with opener.open(req, timeout=60) as response:
                body = response.read(4 * 1024 * 1024 + 1)
            if len(body) > 4 * 1024 * 1024:
                raise ValueError("oversized response")
            result = json.loads(body)
            if not isinstance(result, dict):
                raise ValueError("unexpected response")
            return result
        except urllib.error.HTTPError as error:
            print(f"Gateway returned HTTP {error.code}; response body suppressed.", file=sys.stderr)
        except Exception:
            # Errors can contain URLs, headers or server-provided sensitive strings.
            print("Gateway request failed (network, TLS or response format); details suppressed.", file=sys.stderr)
        return None

    result = request("/models")
    if result is None:
        return 1
    rows = result.get("data")
    if not isinstance(rows, list):
        print("Unexpected model-list format.", file=sys.stderr)
        return 1
    ids = sorted({row["id"] for row in rows if isinstance(row, dict) and isinstance(row.get("id"), str)})
    print(json.dumps({"models": ids}))
    if model is None:
        return 0
    if model not in ids:
        print("Requested model was not returned by the gateway; no inference sent.", file=sys.stderr)
        return 2
    result = request("/chat/completions", {
        "model": model, "max_tokens": 256,
        "messages": [{"role": "user", "content": "Reply with the single word OK."}]})
    if result is None:
        return 1
    choices = result.get("choices")
    choice = choices[0] if isinstance(choices, list) and choices and isinstance(choices[0], dict) else {}
    message = choice.get("message")
    content = message.get("content") if isinstance(message, dict) else None
    ok = isinstance(content, str) and bool(content.strip())
    # Report shape only, not generated text or arbitrary upstream metadata.
    print(json.dumps({"completion_has_text": ok}))
    return 0 if ok else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", nargs="?", help="Also send one short completion for this model")
    args = parser.parse_args()
    try:
        return check(args.model)
    except Exception:
        print("Invalid configuration or unexpected response; details suppressed.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
