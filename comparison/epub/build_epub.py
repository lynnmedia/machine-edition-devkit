from pathlib import Path
import zipfile

def build_epub(source_md: Path, output_epub: Path):
    text_content = source_md.read_text(encoding="utf-8")
    
    # Simple HTML conversion
    html_body = []
    for line in text_content.splitlines():
        if line.startswith("## "):
            html_body.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith("# "):
            html_body.append(f"<h1>{line[2:]}</h1>")
        elif line.strip():
            html_body.append(f"<p>{line.strip()}</p>")

    chapter_xhtml = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
  <title>SROW Comparison Document</title>
</head>
<body>
  {"\n  ".join(html_body)}
</body>
</html>"""

    container_xml = """<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>"""

    content_opf = """<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="pub-id" version="3.0">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="pub-id">urn:uuid:srow-comparison-epub-v0.1</dc:identifier>
    <dc:title>SROW Public Reference Comparison Document</dc:title>
    <dc:language>en</dc:language>
  </metadata>
  <manifest>
    <item id="chapter1" href="chapter1.xhtml" media-type="application/xhtml+xml"/>
    <item id="toc" href="toc.xhtml" media-type="application/xhtml+xml" properties="nav"/>
  </manifest>
  <spine>
    <itemref idref="chapter1"/>
  </spine>
</package>"""

    toc_xhtml = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head><title>TOC</title></head>
<body>
  <nav epub:type="toc">
    <h1>Table of Contents</h1>
    <ol>
      <li><a href="chapter1.xhtml">SROW Public Reference Comparison Document</a></li>
    </ol>
  </nav>
</body>
</html>"""

    with zipfile.ZipFile(output_epub, "w", compression=zipfile.ZIP_DEFLATED) as z:
        # mimetype must be uncompressed first entry in EPUB
        z.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml", container_xml)
        z.writestr("OEBPS/content.opf", content_opf)
        z.writestr("OEBPS/toc.xhtml", toc_xhtml)
        z.writestr("OEBPS/chapter1.xhtml", chapter_xhtml)

if __name__ == "__main__":
    src = Path(__file__).resolve().parent.parent / "source" / "comparison-source.md"
    dst = Path(__file__).resolve().parent / "comparison-document.epub"
    build_epub(src, dst)
    print("EPUB generated successfully:", dst)
