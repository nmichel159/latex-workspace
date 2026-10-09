"""Writes image fixtures with planted metadata for the packager trace-scan tests.

Usage: python -I make_trace_fixtures.py <jpeg-source> <output-dir>
"""
import struct
import sys
import zlib
from pathlib import Path


def chunk(kind: bytes, data: bytes) -> bytes:
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)


def png(extra: list[bytes]) -> bytes:
    ihdr = chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 0, 0, 0, 0))
    idat = chunk(b"IDAT", zlib.compress(b"\x00\x80"))
    return b"\x89PNG\r\n\x1a\n" + ihdr + b"".join(extra) + idat + chunk(b"IEND", b"")


def jpeg_with(source: bytes, segment: bytes) -> bytes:
    assert source[:2] == b"\xff\xd8"
    return source[:2] + segment + source[2:]


def segment(marker: int, payload: bytes) -> bytes:
    return bytes([0xFF, marker]) + struct.pack(">H", len(payload) + 2) + payload


def main() -> None:
    jpeg_source = Path(sys.argv[1]).read_bytes()
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    (out / "plain.png").write_bytes(png([]))
    (out / "text-software.png").write_bytes(png([chunk(b"tEXt", b"Software\x00Claude")]))
    (out / "ztext-author.png").write_bytes(png([chunk(b"zTXt", b"Author\x00\x00" + zlib.compress(b"norom"))]))
    itxt = b"Comment\x00\x01\x00en\x00\x00" + zlib.compress("Co-Authored-By: someone".encode("utf-8"))
    (out / "itext-comment.png").write_bytes(png([chunk(b"iTXt", itxt)]))
    (out / "berge-software.png").write_bytes(png([chunk(b"tEXt", b"Software\x00Drawn after Claude Berge")]))
    (out / "com-chatgpt.jpg").write_bytes(jpeg_with(jpeg_source, segment(0xFE, b"Created by ChatGPT")))
    xmp = (b"http://ns.adobe.com/xap/1.0/\x00<x:xmpmeta xmlns:x='adobe:ns:meta/'><rdf:RDF><rdf:Description "
           b"xmlns:xmp='http://ns.adobe.com/xap/1.0/'><xmp:CreatorTool>Gemini</xmp:CreatorTool>"
           b"</rdf:Description></rdf:RDF></x:xmpmeta>")
    (out / "xmp-gemini.jpg").write_bytes(jpeg_with(jpeg_source, segment(0xE1, xmp)))
    exif_text = "Copilot".encode("utf-16-le")
    (out / "exif-utf16.jpg").write_bytes(jpeg_with(jpeg_source, segment(0xE1, b"Exif\x00\x00II*\x00" + exif_text)))
    (out / "creator-claude.eps").write_bytes(
        b"%!PS-Adobe-3.0 EPSF-3.0\n%%Creator: Claude\n%%For: norom\n%%BoundingBox: 0 0 10 10\n"
        b"%%EndComments\nnewpath 0 0 moveto 10 10 lineto stroke\n%%EOF\n")
    (out / "generator.svg").write_bytes(
        b"<?xml version='1.0'?>\n<!-- Generator: ChatGPT -->\n"
        b"<svg xmlns='http://www.w3.org/2000/svg' width='10' height='10'>"
        b"<image href='data:image/png;base64,iVBORw0KGgoTODOclaudeAAAA'/></svg>\n")


if __name__ == "__main__":
    main()
