# Crystal trainer generation in Sprite Studio

**Status:** A selectable generation **style** is wired into the normal StylePicker through `src/lib/style-presets.ts`. This sends descriptive guidance to the app's existing AI provider. It does not train a model and cannot force the AI to output correct pixel topology.

1. Open a character project in Sprite Studio, select **Crystal trainer (4 shades)** as its art style.
2. Set a **Custom** generation profile with width **56**, height **56**, and one static sprite (/sprite); select your configured image provider.
3. Attach the **FireRed Youngster** as identity reference and **Crystal Youngster** as sprite-work reference (use the second reference for style, not for copying its design).
4. Generate. Inspect the actual native-size asset carefully, preserving the best candidate as an anchor.
5. Export PNG and validate with `python tools/crystal_trainer_validate.py output.png` (requires Pillow).

Validator checks dimensions, number of opaque colors, transparency and partial alpha. It intentionally fails invalid sprites rather than claiming its own downscaling is a true hand-authored reconstruction. Art-quality and resemblance require visual review.

The style prompt is a starting point. The next integration should add a convenient 56×56 one-frame profile action in the generation settings and optional validation in the asset inspector.
