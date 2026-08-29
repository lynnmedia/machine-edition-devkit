from pathlib import Path
import json
import re

def build_rag_corpus(source_md: Path, output_json: Path, chunk_size: int = 250, overlap: int = 40):
    """Builds a deterministic textual RAG corpus with standard sliding-window chunking."""
    text = source_md.read_text(encoding="utf-8")
    
    # Split paragraphs
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    
    chunks = []
    chunk_index = 0
    
    current_chunk = ""
    for p in paragraphs:
        if len(current_chunk) + len(p) + 1 <= chunk_size:
            current_chunk = (current_chunk + " " + p).strip() if current_chunk else p
        else:
            if current_chunk:
                chunks.append({
                    "chunk_id": f"chunk-{chunk_index:03d}",
                    "text": current_chunk,
                    "source_document": "comparison-source.md",
                    "position": chunk_index,
                    "char_length": len(current_chunk)
                })
                chunk_index += 1
            current_chunk = p

    if current_chunk:
        chunks.append({
            "chunk_id": f"chunk-{chunk_index:03d}",
            "text": current_chunk,
            "source_document": "comparison-source.md",
            "position": chunk_index,
            "char_length": len(current_chunk)
        })

    config = {
        "strategy": "paragraph-preserving sliding window",
        "target_chunk_size": chunk_size,
        "overlap": overlap,
        "chunk_count": len(chunks),
        "source_document": "comparison-source.md",
        "chunks": chunks
    }

    output_json.write_text(json.dumps(config, indent=2), encoding="utf-8")
    print(f"RAG corpus created with {len(chunks)} chunks:", output_json)

if __name__ == "__main__":
    src = Path(__file__).resolve().parent.parent / "source" / "comparison-source.md"
    dst = Path(__file__).resolve().parent / "rag-corpus.json"
    build_rag_corpus(src, dst)
