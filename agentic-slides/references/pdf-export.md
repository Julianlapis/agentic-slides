---
name: pdf-export
description: PDF Export Pipeline for Paper Slides - direct MCP screenshot approach
---

# PDF Export Pipeline for Paper Slides

## The Approach: Direct MCP Screenshots → Pillow PDF

Paper's MCP server at `localhost:29979` accepts JSON-RPC calls. Call `get_screenshot` for each artboard at 2x scale, decode the base64 response, save to disk, assemble with Pillow.

This is the **only** approach. Do not use JSX conversion. It introduces visual differences.

## Full Script

```python
import json, urllib.request, base64, os, glob
from PIL import Image

def call_paper_mcp(method, params):
    payload = json.dumps({"jsonrpc": "2.0", "method": method, "params": params, "id": 1}).encode()
    req = urllib.request.Request("http://localhost:29979/mcp", data=payload,
        headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream"})
    resp = urllib.request.urlopen(req, timeout=60)
    data = resp.read().decode()
    for line in data.split("\n"):
        if line.startswith("data: "):
            return json.loads(line[6:])
    return json.loads(data)

def export_pdf(artboard_ids, output_path, slide_dir="/tmp/paper-pdf/slides"):
    """
    artboard_ids: list of (node_id, slide_number) tuples, e.g. [("1-0", "01"), ("8-0", "02"), ...]
    output_path: e.g. "/Users/.../Desktop/deck.pdf"
    """
    os.makedirs(slide_dir, exist_ok=True)

    # Screenshot each artboard
    for node_id, num in artboard_ids:
        path = f"{slide_dir}/slide-{num}.jpg"
        if os.path.exists(path) and os.path.getsize(path) > 1000:
            print(f"  Slide {num}: cached")
            continue
        result = call_paper_mcp("tools/call", {
            "name": "get_screenshot",
            "arguments": {"nodeId": node_id, "scale": 2}
        })
        content = result.get("result", {}).get("content", [])
        for item in content:
            if item.get("type") == "image":
                img_data = base64.b64decode(item["data"])
                with open(path, "wb") as f:
                    f.write(img_data)
                print(f"  Slide {num}: saved ({len(img_data)} bytes)")
                break
        else:
            print(f"  Slide {num}: FAILED")

    # Assemble PDF
    slides = sorted(glob.glob(f"{slide_dir}/slide-*.jpg"))
    images = [Image.open(s).convert("RGB") for s in slides]
    images[0].save(output_path, save_all=True, append_images=images[1:], resolution=144.0)
    print(f"PDF saved: {output_path} ({len(slides)} slides)")
```

## Usage

1. Get artboard IDs from `get_basic_info()`
2. Build the `artboard_ids` list in slide order
3. Call `export_pdf(artboard_ids, output_path)`
4. Verify the PDF matches Paper exactly

## Why Not JSX

JSX-to-HTML conversion introduces:
- CSS translation bugs (camelCase → kebab-case mismatches)
- Line-height rounding differences (`round(up, X%, 1px)` → `X%`)
- Color format mismatches (oklab → hex approximations)
- Font loading timing issues
- Indentation and spacing differences

Screenshots are rendered by Paper's own engine. They are pixel-perfect by definition.

## Dependencies

Only Pillow is needed. It's usually pre-installed. No reportlab, no Puppeteer, no npm packages.

```bash
pip3 install Pillow  # if not already available
```
