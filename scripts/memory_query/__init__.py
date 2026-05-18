"""Memory Query — BM25 retrieval for Agent Memory Framework.

Usage:
    from memory_query import MemoryIndex
    idx = MemoryIndex(".ai")
    idx.build()
    results = idx.query("what is the database schema")
"""

from .indexer import MemoryIndex, format_results

__all__ = ["MemoryIndex", "format_results"]
