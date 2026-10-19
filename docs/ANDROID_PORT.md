# Android experimental port

This is an **experimental diagnostic build**, not a claim of a working Android app.

Sprite Studio's Tauri 2 + Svelte frontend can potentially be reused on Android, but the existing Rust backend assumes desktop process execution, system paths, and agent CLIs. The current interface also assumes a wide desktop viewport. A passing web/frontend check does not imply Android compatibility.

## First milestone

Workflow `crystal-android-prototype.yml` attempts an unsigned debug APK from the Crystal branch and uploads its build logs. It initializes Tauri's Android project on the CI runner only; generated Android project files are not committed.

Do **not** use this as a release build. It may fail in Rust compilation or packaging. The APK artifact is published only when actually produced.

## Android priorities

1. Isolate mobile-compatible PNG editing, preview and Crystal four-shade checking from desktop-only services.
2. Replace filesystem and OS-dependent assumptions with Android app data and file-picker flows.
3. Use an approved remote image provider instead of running Codex/Cursor desktop CLIs on the device. Provide clear key/security and cost handling.
4. Design a small-screen workspace for editing/references and export.
5. Once Android compiles, run real device smoke tests before promising usable generation.

Windows workflow and release configuration remain unchanged.
