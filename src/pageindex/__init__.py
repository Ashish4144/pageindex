"""PageIndex: Vectorless, reasoning-based RAG using hierarchical document indexing."""

from pageindex.config import PageIndexConfig
from pageindex.pdf.processor import page_index, PageIndexProcessor
from pageindex.markdown.processor import md_to_tree
from pageindex.batch import process_folder, process_folder_sync, DoclingServeClient
from pageindex.repo import index_repository, index_repository_sync

__version__ = "0.1.0"

__all__ = [
    "PageIndexConfig",
    "PageIndexProcessor",
    "page_index",
    "md_to_tree",
    "process_folder",
    "process_folder_sync",
    "DoclingServeClient",
    "index_repository",
    "index_repository_sync",
    "__version__",
]
