<script lang="ts">
  import { assetUrl } from "$lib/api";
  import type { Asset } from "$lib/types";
  let { asset }: { asset: Asset } = $props();
  let status = $state<"checking" | "pass" | "fail" | "error">("checking");
  let findings = $state<string[]>([]);
  let colorCount = $state(0);

  $effect(() => {
    const url = assetUrl(asset.path);
    let cancelled = false;
    status = "checking";
    findings = [];
    colorCount = 0;
    const img = new Image();
    img.crossOrigin = "anonymous";
    img.onload = () => {
      if (cancelled) return;
      try {
        const canvas = document.createElement("canvas");
        canvas.width = img.naturalWidth;
        canvas.height = img.naturalHeight;
        const ctx = canvas.getContext("2d", { willReadFrequently: true });
        if (!ctx) throw new Error("Canvas inspection unavailable");
        ctx.drawImage(img, 0, 0);
        const bytes = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
        const opaque = new Set<string>();
        let transparent = 0;
        let partial = 0;
        for (let i = 0; i < bytes.length; i += 4) {
          if (bytes[i+3] === 0) transparent++;
          else if (bytes[i+3] !== 255) partial++;
          else opaque.add(bytes[i]+","+bytes[i+1]+","+bytes[i+2]);
        }
        const issues: string[] = [];
        if (canvas.width !== 56 || canvas.height !== 56) issues.push("Expected 56×56 canvas");
        if (opaque.size > 4) issues.push("More than four opaque colors");
        if (partial > 0) issues.push(partial + " antialiased / partial-alpha pixels");
        if (transparent === 0) issues.push("No transparent pixels");
        colorCount = opaque.size;
        findings = issues;
        status = issues.length ? "fail" : "pass";
      } catch (error) {
        status = "error";
        findings = [error instanceof Error ? error.message : "Pixel data could not be read"];
      }
    };
    img.onerror = () => {
      if (!cancelled) { status = "error"; findings = ["Unable to load image for pixel inspection"]; }
    };
    img.src = url;
    return () => { cancelled = true; img.onload = null; img.onerror = null; };
  });
</script>

<section class="crystal-check">
  <h3>CRYSTAL TRAINER CHECK</h3>
  {#if status === "checking"}<p>Inspecting pixels…</p>
  {:else if status === "pass"}<p class="passed">Pass: 56×56, {colorCount} opaque colors, transparent, no antialiasing.</p>
  {:else}
    <p class="failed">{status === "error" ? "Inspection unavailable" : "Not yet Crystal-format compliant"}</p>
    <ul>{#each findings as finding}<li>{finding}</li>{/each}</ul>
  {/if}
  <p class="note">Technical checks only. Character likeness and authentic pixel clusters still require visual review.</p>
</section>
<style>
  .crystal-check{padding:14px;border-bottom:1px solid var(--border)}h3{font-size:10px;letter-spacing:.14em;color:var(--faint);margin:0 0 11px}p,li{font-size:11px;line-height:1.5;color:var(--muted)}.passed{color:#7eb69a}.failed{color:#dc9d83}ul{padding-left:17px;margin:5px 0}.note{color:var(--faint);font-size:10px;margin-bottom:0}
</style>
