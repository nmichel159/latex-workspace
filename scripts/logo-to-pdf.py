"""Convert the author's logo (one SVG path of M, L, Z commands) to vector PDFs in given colors.

Usage: python scripts/logo-to-pdf.py <logo.svg> <out-dir>
Writes logo-white.pdf, logo-tint.pdf and logo-cover.pdf for the template beamer-talk.
"""
import pathlib
import re
import sys

MM = 72 / 25.4
LEVELS = 16
COLORS = {
    "white": (1, 1, 1),
    "tint": (0.90, 0.935, 0.965),
}


def content(svg_text, rgb):
    box = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg_text)
    path = re.search(r'\sd="([^"]+)"', svg_text)
    if box is None or path is None:
        raise SystemExit("the SVG has no viewBox or no path")
    width, height = box.groups()
    height = float(height)
    data = path.group(1)
    if set(re.findall(r"[A-Za-z]", data)) - set("MLZ"):
        raise SystemExit("the path uses commands other than M, L, Z")
    out = [f"{rgb[0]:.4f} {rgb[1]:.4f} {rgb[2]:.4f} rg", f"{MM:.5f} 0 0 {-MM:.5f} 0 {height * MM:.3f} cm"]
    for command, x, y in re.findall(r"([MLZ])\s*(?:([\d.-]+),([\d.-]+))?", data):
        if command == "Z":
            out.append("h")
        else:
            out.append(f"{x} {y} {command.lower()}")
    out.append("f*")
    return float(width), height, "\n".join(out).encode("ascii")


def cover(svg_text):
    """White logo whose opacity grows from left to right, per shape, so no viewer needs a soft mask."""
    box = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg_text)
    path = re.search(r'\sd="([^"]+)"', svg_text)
    if box is None or path is None:
        raise SystemExit("the SVG has no viewBox or no path")
    width, height = float(box.group(1)), float(box.group(2))
    shapes = []
    for part in path.group(1).split("M")[1:]:
        points = [(float(x), float(y)) for x, y in re.findall(r"([\d.-]+),([\d.-]+)", part)]
        xs, ys = [p[0] for p in points], [p[1] for p in points]
        shapes.append({"points": points, "box": (min(xs), min(ys), max(xs), max(ys))})
    for shape in shapes:
        # A hole stays with the shape around it, because even-odd filling needs both in one path.
        x0, y0, x1, y1 = shape["box"]
        around = [
            s["box"] for s in shapes
            if s is not shape and s["box"][0] <= x0 and s["box"][1] <= y0 and s["box"][2] >= x1 and s["box"][3] >= y1
        ]
        x0, _, x1, _ = max(around, key=lambda b: (b[2] - b[0]) * (b[3] - b[1])) if around else shape["box"]
        position = min(max(((x0 + x1) / 2 / width - 0.2) / 0.6, 0), 1)
        shape["level"] = round(position * (LEVELS - 1))
    out = ["1 1 1 rg", f"{MM:.5f} 0 0 {-MM:.5f} 0 {height * MM:.3f} cm"]
    states = []
    for level in range(LEVELS):
        t = level / (LEVELS - 1)
        alpha = 0.12 + 0.73 * t * t * (3 - 2 * t)
        states.append(f"/G{level} << /ca {alpha:.3f} >>")
        out.append(f"/G{level} gs")
        for shape in (s for s in shapes if s["level"] == level):
            x, y = shape["points"][0]
            out.append(f"{x:.3f} {y:.3f} m")
            out.extend(f"{x:.3f} {y:.3f} l" for x, y in shape["points"][1:])
            out.append("h")
        out.append("f*")
    return width, height, "\n".join(out).encode("ascii"), "/ExtGState << " + " ".join(states) + " >>"


def pdf(width, height, stream, resources=""):
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {width * MM:.3f} {height * MM:.3f}] "
        f"/Contents 4 0 R /Resources << {resources} >> >>".encode("ascii"),
        b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"\nendstream",
    ]
    body = b"%PDF-1.4\n"
    offsets = []
    for number, obj in enumerate(objects, 1):
        offsets.append(len(body))
        body += f"{number} 0 obj\n".encode("ascii") + obj + b"\nendobj\n"
    xref = len(body)
    body += f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode("ascii")
    for offset in offsets:
        body += f"{offset:010d} 00000 n \n".encode("ascii")
    body += f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode("ascii")
    return body


def main():
    svg_text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
    out_dir = pathlib.Path(sys.argv[2])
    for name, rgb in COLORS.items():
        width, height, stream = content(svg_text, rgb)
        (out_dir / f"logo-{name}.pdf").write_bytes(pdf(width, height, stream))
    width, height, stream, resources = cover(svg_text)
    (out_dir / "logo-cover.pdf").write_bytes(pdf(width, height, stream, resources))


if __name__ == "__main__":
    main()
