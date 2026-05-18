"""BM25 indexer for Agent Memory Framework. Zero external dependencies.

Indexes .ai/ memory files and provides ranked full-text search.

Usage:
    from memory_query.indexer import MemoryIndex
    idx = MemoryIndex(".ai")
    idx.build()
    results = idx.query("database schema")
"""

import json
import math
import os
import re
import sys
from collections import Counter
from pathlib import Path
from typing import List, Tuple, Optional


# ── Tokenizer ──────────────────────────────────────────────────────────────

_TOKEN_PATTERN = re.compile(r"[a-zA-Z_][a-zA-Z0-9_]{1,}")


def tokenize(text: str) -> List[str]:
    """Split text into lowercase tokens suitable for BM25 indexing."""
    return [t.lower() for t in _TOKEN_PATTERN.findall(text)]


# ── BM25 Parameters ───────────────────────────────────────────────────────

K1 = 1.5   # Term frequency saturation
B = 0.75   # Length normalization
EPSILON = 0.25


# ── Index Entry ────────────────────────────────────────────────────────────

class IndexEntry:
    """A single indexed file with its metadata."""

    def __init__(self, rel_path: str, title: str, tokens: List[str]):
        self.rel_path = rel_path
        self.title = title
        self.tokens = tokens
        self.doc_len = len(tokens)
        self.term_freqs = Counter(tokens)


# ── Memory Index ───────────────────────────────────────────────────────────

class MemoryIndex:
    """Build and query a BM25 index over .ai/ memory files.

    The index is stored as a JSON file in .ai/.memory_index/ for fast reload.
    """

    INDEX_DIR = ".memory_index"
    INDEX_FILE = "index.json"

    def __init__(self, ai_dir: str = ".ai", cache_dir: Optional[str] = None):
        self.ai_dir = Path(ai_dir).resolve()
        self.cache_dir = Path(cache_dir or self.ai_dir / self.INDEX_DIR)
        self.docs: List[IndexEntry] = []
        self.avg_doc_len: float = 0.0
        self.num_docs: int = 0
        self.idf: dict = {}         # term -> idf score
        self._built = False

    # ── Document Loading ───────────────────────────────────────────────────

    def _load_docs(self) -> List[IndexEntry]:
        """Load and tokenize all .md and .yaml files in .ai/ directory."""
        if not self.ai_dir.exists():
            print(f"Warning: {self.ai_dir} does not exist", file=sys.stderr)
            return []

        docs = []
        for fpath in sorted(self.ai_dir.iterdir()):
            if fpath.suffix not in (".md", ".yaml", ".yml"):
                continue
            if fpath.is_dir():
                continue

            text = fpath.read_text(encoding="utf-8", errors="replace")
            tokens = tokenize(text)

            # Extract a title from the first heading
            title = ""
            for line in text.splitlines():
                if line.startswith("# "):
                    title = line.lstrip("# ").strip()
                    break
            if not title:
                title = fpath.name

            rel = fpath.relative_to(self.ai_dir.parent if self.ai_dir.parent.name == ".ai" else self.ai_dir)
            # Store as .ai/file.md consistently
            rel_str = f".ai/{fpath.name}"

            docs.append(IndexEntry(rel_str, title, tokens))

        return docs

    # ── Build Index ────────────────────────────────────────────────────────

    def build(self, force: bool = False) -> "MemoryIndex":
        """Build the BM25 index from .ai/ files.

        Loads from cache if available (unless force=True).
        """
        if not force:
            cached = self._load_cache()
            if cached:
                return cached

        self.docs = self._load_docs()
        self.num_docs = len(self.docs)

        if self.num_docs == 0:
            self.avg_doc_len = 0.0
            self.idf = {}
            self._built = True
            return self

        # Average document length
        self.avg_doc_len = sum(d.doc_len for d in self.docs) / self.num_docs

        # Document frequency per term
        df = Counter()
        for doc in self.docs:
            for term in doc.term_freqs:
                df[term] += 1

        # IDF: log((N - df + 0.5) / (df + 0.5))
        N = self.num_docs
        self.idf = {}
        for term, freq in df.items():
            self.idf[term] = math.log((N - freq + 0.5) / (freq + 0.5) + 1.0)

        self._built = True
        self._save_cache()
        return self

    # ── Query ──────────────────────────────────────────────────────────────

    def query(self, query_text: str, top_k: int = 5) -> List[dict]:
        """Run a BM25 search query and return ranked results.

        Returns list of dicts:
            {path, title, score, snippet}
        """
        if not self._built:
            self.build()

        query_terms = tokenize(query_text)
        if not query_terms or self.num_docs == 0:
            return []

        # Score each document
        scored: List[Tuple[float, IndexEntry]] = []
        for doc in self.docs:
            score = 0.0
            for term in set(query_terms):
                tf = doc.term_freqs.get(term, 0)
                if tf == 0:
                    continue
                idf = self.idf.get(term, 0)
                # BM25 scoring
                numerator = tf * (K1 + 1)
                denominator = tf + K1 * (1 - B + B * doc.doc_len / self.avg_doc_len)
                score += idf * numerator / denominator
            if score > 0:
                scored.append((score, doc))

        # Sort by score descending
        scored.sort(key=lambda x: -x[0])

        results = []
        for score, doc in scored[:top_k]:
            results.append({
                "path": doc.rel_path,
                "title": doc.title,
                "score": round(score, 4),
                "snippet": self._get_snippet(doc, query_terms),
            })

        return results

    # ── Search (file-first, like grep) ─────────────────────────────────────

    def search(self, term: str) -> List[dict]:
        """Search for files containing a specific term. Returns per-file match counts."""
        if not self._built:
            self.build()

        query_terms = tokenize(term)
        if not query_terms:
            return []

        results = []
        for doc in self.docs:
            matches = 0
            for qt in query_terms:
                matches += doc.term_freqs.get(qt, 0)
            if matches > 0:
                results.append({
                    "path": doc.rel_path,
                    "title": doc.title,
                    "matches": matches,
                })

        results.sort(key=lambda x: -x["matches"])
        return results

    # ── Snippet Generation ─────────────────────────────────────────────────

    def _get_snippet(self, doc: IndexEntry, query_terms: List[str], context: int = 40) -> str:
        """Extract a relevant snippet around the first query term match."""
        # Read the actual file to get text with line boundaries
        fpath = self.ai_dir / doc.rel_path.split("/")[-1]
        if not fpath.exists():
            # Try relative to cwd
            fpath = Path(doc.rel_path)
            if not fpath.exists():
                return ""

        try:
            text = fpath.read_text(encoding="utf-8", errors="replace")
            lines = text.splitlines()
        except Exception:
            return ""

        # Find the first line containing any query term
        for i, line in enumerate(lines):
            lower = line.lower()
            for qt in query_terms:
                if qt in lower:
                    start = max(0, i - 2)
                    end = min(len(lines), i + 3)
                    snippet_lines = lines[start:end]
                    snippet = "\n".join(snippet_lines)
                    if len(snippet) > 500:
                        snippet = snippet[:500] + "..."
                    return snippet
        return ""

    # ── Cache ──────────────────────────────────────────────────────────────

    def _save_cache(self):
        """Persist the index to disk as JSON for fast reload."""
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        cache_path = self.cache_dir / self.INDEX_FILE

        data = {
            "version": 1,
            "avg_doc_len": self.avg_doc_len,
            "num_docs": self.num_docs,
            "idf": self.idf,
            "docs": [
                {
                    "rel_path": d.rel_path,
                    "title": d.title,
                    "doc_len": d.doc_len,
                    "term_freqs": dict(d.term_freqs),
                }
                for d in self.docs
            ],
        }

        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _load_cache(self) -> Optional["MemoryIndex"]:
        """Load cached index if it exists and is newer than any .ai/ file."""
        cache_path = self.cache_dir / self.INDEX_FILE
        if not cache_path.exists():
            return None

        # Check freshness: cache must be newer than all .ai/ files
        cache_mtime = cache_path.stat().st_mtime
        for f in self.ai_dir.iterdir():
            if f.suffix in (".md", ".yaml", ".yml") and f.is_file():
                if f.stat().st_mtime > cache_mtime:
                    return None  # Stale cache

        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, KeyError, ValueError):
            return None

        self.avg_doc_len = data["avg_doc_len"]
        self.num_docs = data["num_docs"]
        self.idf = data["idf"]
        self.docs = []
        for d in data["docs"]:
            entry = IndexEntry(d["rel_path"], d["title"], [])
            entry.doc_len = d["doc_len"]
            entry.term_freqs = Counter(d["term_freqs"])
            self.docs.append(entry)

        self._built = True
        return self


# ── CLI Helpers ────────────────────────────────────────────────────────────

def format_results(results: List[dict], mode: str = "query") -> str:
    """Format results for terminal display."""
    if not results:
        return "No results found."

    lines = []
    if mode == "query":
        lines.append(f"Top {len(results)} results:\n")
        for i, r in enumerate(results, 1):
            lines.append(f"[{i}] {r['path']} (score: {r['score']})")
            lines.append(f"    Title: {r['title']}")
            if r.get("snippet"):
                lines.append(f"    Snippet:\n{r['snippet'].strip()}")
            lines.append("")
    elif mode == "search":
        lines.append(f"Files containing query terms ({len(results)} matches):\n")
        for i, r in enumerate(results, 1):
            lines.append(f"[{i}] {r['path']} ({r['matches']} matches) — {r['title']}")

    return "\n".join(lines)
