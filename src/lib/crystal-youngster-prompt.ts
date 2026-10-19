import type { ReferenceImage } from "$lib/types";

/** Construct a provider-ready request using active, imported images (not fake file paths). */
export function youngsterReferencePrompt(refs: Pick<ReferenceImage, "name">[]): string {
  if (refs.length < 2) throw new Error("Attach both the FireRed identity PNG and the Crystal style PNG first.");
  const identity = refs.find(r => /firered/i.test(r.name)) ?? refs[0];
  const style = refs.find(r => /crystal/i.test(r.name) && r !== identity) ?? refs.find(r => r !== identity)!;
  return `/sprite Create ONE transparent 56×56 trainer battle sprite. Identity reference: "${identity.name}"—preserve this boy's exact recognizable costume, hairstyle, face and pose. Pixel-work reference: "${style.name}"—borrow only the crisp monochrome 4-tone cluster technique, not the character identity. Use black, white and two intermediate gray shades, plus transparency; zero antialiasing or gradients. Carefully reconstruct linework and anatomy in native-scale pixel art, minimizing dithering. Upper-left light. Do not scale a large finished image down blindly. Deliver a single static PNG asset. Keep the identity distinct from the style-reference character.`;
}
