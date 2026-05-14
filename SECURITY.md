# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability, please **do NOT open a public issue**.

Email the details to the maintainers. We will respond within 48 hours.

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.2.x  | Active |
| < 0.2  | No longer supported |

## Security Design

Sophia follows these security principles:

- **Local-first**: All data stays on your machine by default. No telemetry.
- **No network dependency**: Core compiler runs entirely offline.
- **Input validation**: Empty and malformed inputs are rejected.
- **No credential handling**: Sophia does not manage API keys or authentication.

## Known Limitations

- MCP server has no built-in authentication (localhost-only by design)
- Trace data stored as plain JSON (no encryption at rest)
