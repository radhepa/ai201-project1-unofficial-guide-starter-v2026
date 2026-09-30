"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

import re
from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split on paragraph breaks, one paragraph per chunk.

    campus_life's 88 documents are all shaped the same way: a one-line title,
    a blank line, then one to four body paragraphs — and every body paragraph
    turned out to be a complete, self-contained fact on its own, even the
    short ones ("Expect 8 to 10 hours a week outside class." is 42 characters
    and still a whole sentence). Multi-paragraph posts mix genuinely separate
    topics (a dining hall's wait times vs. its hours and price; a course's
    format vs. its workload vs. a piece of advice about it), so keeping the
    whole post as one chunk would bury each fact in the others. Splitting on
    paragraphs keeps every fact intact without gluing unrelated facts together.

    The one thing paragraph splitting gets wrong on its own: the title line is
    always its own paragraph, and a title ("CS 210 Data Structures") is a
    fragment, not a sentence — exactly the "too small" failure the milestone
    warns about. So the title is merged into the first body paragraph rather
    than emitted alone.

    A paragraph longer than config.CHUNK_SIZE falls back to fixed windows
    (chunker.py::fallback_split's approach) for just that paragraph. campus_life
    never hits this — its longest body paragraph is 373 characters, comfortably
    under CHUNK_SIZE — but it keeps the function from silently producing one
    giant chunk if a longer document ever gets added to this corpus.
    """
    chunk_size = config.CHUNK_SIZE
    overlap = config.CHUNK_OVERLAP

    chunks: list[Chunk] = []
    for doc in documents:
        blocks = [b.strip() for b in re.split(r"\n\s*\n", doc.text) if b.strip()]
        if not blocks:
            continue

        if len(blocks) > 1:
            # Title + first body paragraph travel together as one chunk.
            paragraphs = [f"{blocks[0]}\n\n{blocks[1]}", *blocks[2:]]
        else:
            paragraphs = blocks

        index = 0
        for para in paragraphs:
            if len(para) <= chunk_size:
                chunks.append(
                    Chunk(
                        text=para,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::split_documents",
                    )
                )
                index += 1
                continue

            start = 0
            while start < len(para):
                piece = para[start : start + chunk_size].strip()
                if piece:
                    chunks.append(
                        Chunk(
                            text=piece,
                            source=doc.source,
                            index=index,
                            produced_by="chunker.py::split_documents",
                        )
                    )
                    index += 1
                start += chunk_size - overlap

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
