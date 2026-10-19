#!/usr/bin/env python3
"""Check native-scale Crystal trainer PNGs without silently repairing them."""
import argparse, json, sys
from pathlib import Path
from PIL import Image
def validate(path: Path):
    with Image.open(path) as im:
        rgba=im.convert("RGBA")
        pixels=list(rgba.getdata())
        solid={p[:3] for p in pixels if p[3]==255}
        partial=sum(p[3] not in (0,255) for p in pixels)
        transparency=sum(p[3]==0 for p in pixels)
        errors=[]
        if im.size!=(56,56): errors.append(f"wrong dimensions: {im.size}, expected 56x56")
        if len(solid)>4: errors.append(f"{len(solid)} opaque colors, maximum 4")
        if partial: errors.append(f"{partial} partially transparent pixels (antialiasing)")
        if not transparency: errors.append("no transparent background pixels")
        return {"file":str(path),"dimensions":list(im.size),"opaque_colors":len(solid),
                "partial_alpha_pixels":partial,"transparent_pixels":transparency,
                "valid":not errors,"errors":errors}
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("png",type=Path)
    parser.add_argument("--report",type=Path)
    args=parser.parse_args()
    data=validate(args.png)
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(json.dumps(data,indent=2)+"\n")
    print(json.dumps(data,indent=2))
    sys.exit(0 if data["valid"] else 1)
if __name__=="__main__": main()
