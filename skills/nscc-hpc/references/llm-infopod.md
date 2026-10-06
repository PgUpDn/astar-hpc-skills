# Institutional inference services

The source notes described an ASPIRE2A proof-of-concept service called inf-pod with an Anthropic-compatible API. Its deployment node, models, access conditions and certificate are not stable. Obtain the currently approved endpoint, credentials and CA certificate from the service owner. No individual contact, private node or shared-directory path is included here.

## TLS and authentication

Use the institution-provided CA certificate and an endpoint whose hostname matches the certificate. For an HTTPS health check:

```bash
curl --fail --silent --show-error --connect-timeout 10 --max-time 30 \
  --cacert "$INFERENCE_CA_FILE" "$INFERENCE_BASE_URL/health/readiness"
```

The readiness path is a historical example: confirm the service's documented API. Never disable TLS verification. For authenticated requests, load the key only in the client process or a mode-600 header/config file; do not put it in command-line arguments, shared settings, logs or version control.

A readiness response does not test inference or credential validity. When a small end-to-end test is requested, use the current model ID and protocol with a bounded output budget. Inspect status and sanitized error categories. A 401 can mean missing, expired or invalid credentials; an unexpected service's error suggests incorrect endpoint/proxy routing.

## Client configuration and tunnels

Use dedicated per-invocation settings so existing global client configuration is not overwritten. Verify effective endpoint, model mapping and certificate trust without showing tokens. Absolute certificate paths may be required by clients that do not expand `~`.

An SSH tunnel must preserve TLS hostname validation; a localhost URL is valid only if the certificate includes localhost or the client provides a supported hostname-preserving routing mechanism. Bind local forwards to loopback and use only approved destinations.

Network availability can differ between login and compute nodes. Run substantial inference/agent workloads under PBS. For installing a client on a restricted network, use current official installation instructions and a verified download/checksum route permitted by site policy. Do not reproduce historical installer URLs as guaranteed current access.
