from pathlib import Path
import re

def generate_minimal_pdf(input_md: Path, output_pdf: Path):
    """Generates a simple, standard, valid PDF containing the source text."""
    lines = input_md.read_text(encoding="utf-8").splitlines()
    
    # Simple Postscript/PDF text stream
    pdf_lines = []
    y = 750
    for line in lines:
        if not line.strip():
            y -= 14
            continue
        # escape parens
        clean_text = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        pdf_lines.append(f"BT /F1 11 Tf 50 {y} Td ({clean_text}) Tj ET")
        y -= 16

    content_stream = "\n".join(pdf_lines)
    stream_len = len(content_stream.encode("utf-8"))

    pdf_content = f"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>
endobj
4 0 obj
<< /Length {stream_len} >>
stream
{content_stream}
endstream
endobj
5 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj
xref
0 6
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000224 00000 n 
0000000000 00000 n 
trailer
<< /Size 6 /Root 1 0 R >>
startxref
500
%%EOF
"""
    output_pdf.write_bytes(pdf_content.encode("latin-1"))

if __name__ == "__main__":
    src = Path(__file__).resolve().parent.parent / "source" / "comparison-source.md"
    dst = Path(__file__).resolve().parent / "comparison-document.pdf"
    generate_minimal_pdf(src, dst)
    print("PDF generated successfully:", dst)
