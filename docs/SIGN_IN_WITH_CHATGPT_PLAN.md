# Sign in with ChatGPT integration plan

Status: **design only**. No OAuth sign-in flow, token storage, or authorized image-generation integration is implemented yet.

Official sources (reviewed 2026-10-19):
- https://developers.openai.com/siwc/token-sharing-open-source
- https://developers.openai.com/siwc/token-sharing-open-source/registration-and-sign-in
- https://developers.openai.com/siwc/token-sharing-open-source/models-and-inference
- https://developers.openai.com/siwc/token-sharing-open-source/preview-limitations
- https://openai.com/policies/sign-in-with-chatgpt-terms/

## What it would support
Use the documented **open-source dynamic registration** flow, not an embedded webview asking for passwords. User authorizes identity and (separately) the eligible ChatGPT plan-usage scope. Store access/refresh tokens **locally and securely** and never in the repository, app logs, cloud CI, or a shared server. Choose and persist a stable opaque `ext_agent_host_id` for each installation. Derive connected state only from confirmed valid credentials and granted scopes.

After sign-in, retrieve models available to that authenticated account. For eligible Responses API calls, use the official `https://api.openai.com/v1/responses` endpoint with `store:false`, `stream:true`, and explicit input context; handle completion, partial output, token expiration, account limits and user disconnect. Never use private ChatGPT backend endpoints or reuse browser cookies.

## Crucial limitation for Sprite Maker 2K
As of this review, ChatGPT-plan sharing through SIWC **does not support the hosted image-generation tool**. It can support eligible textual style analysis and prompt planning (and image input where supported), but the actual creation of a raster sprite image still requires a separately authorized image provider or a local renderer. A ChatGPT Plus subscription is NOT a substitute for a billed image-generation API.

## Implementation phases
1. Native Tauri OAuth/PKCE browser login and callback handling; no simulated sign-in.
2. Local secret storage and refresh/revoke/disconnect operations (Android secure storage requires separate design).
3. Backend provider for eligible streaming Responses requests; account-specific model catalog and clear limits/errors.
4. UI showing **Connected for style analysis** rather than misleading **Image generation enabled**.
5. Independent image-generation provider selection, opt-in and explicit cost disclosure.
6. Tests: rejected/expired credentials, denied plan sharing, multiple accounts, token refresh, secrets redacted from logs, and rejected unsupported image generation.

Until these are complete, do not display a functional 'Sign in with ChatGPT' button.
