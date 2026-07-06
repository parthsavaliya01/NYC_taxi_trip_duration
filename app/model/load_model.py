"""Compatibility shim kept to preserve existing imports.

Previously this module loaded the pipeline from a local file. The model is
now downloaded from Hugging Face Hub and loaded by the centralized
`model_loader` module. Importing `pipeline` from here preserves existing
call sites.
"""

from app.model.model_loader import get_pipeline as _get_pipeline

_cached_pipeline = None


def get_pipeline():
    """Return the cached pipeline instance."""
    global _cached_pipeline
    if _cached_pipeline is None:
        _cached_pipeline = _get_pipeline()
    return _cached_pipeline


def __getattr__(name):
    if name == "pipeline":
        return get_pipeline()
    raise AttributeError(f"module {__name__} has no attribute {name}")
