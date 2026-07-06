"""
Centralized model loader that downloads the model from Hugging Face Hub
and loads it via joblib. Ensures the model is downloaded and loaded only
once using an LRU cache.

Provides:
- get_pipeline(): returns the loaded scikit-learn pipeline
"""
from functools import lru_cache
import logging
import os
import joblib

try:
    from huggingface_hub import hf_hub_download
    from huggingface_hub.utils import EntryNotFoundError, RepositoryNotFoundError
    import requests
except Exception as e:  # pragma: no cover - environment/dependency issues
    hf_hub_download = None  # type: ignore
    EntryNotFoundError = Exception  # type: ignore
    RepositoryNotFoundError = Exception  # type: ignore
    requests = None  # type: ignore
    _HF_IMPORT_ERROR = e

from app.core.config import settings

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_pipeline():
    """Download (if necessary) and load the pipeline from HF Hub.

    Returns:
        sklearn.pipeline.Pipeline: Loaded pipeline object.

    Raises:
        RuntimeError: If download or loading fails. Errors are logged with
        helpful messages.
    """
    repo_id = getattr(settings, "model").model_repo
    filename = getattr(settings, "model").model_filename

    if not repo_id or not filename:
        msg = (
            "Model repository or filename not configured. "
            "Set MODEL_REPO and MODEL_FILENAME environment variables."
        )
        logger.error(msg)
        raise RuntimeError(msg)

    # Ensure huggingface_hub imported correctly
    if hf_hub_download is None:
        msg = (
            "The huggingface_hub package is not installed or failed to import. "
            "Install it (e.g. `pip install huggingface_hub`) and try again."
        )
        logger.error(msg)
        # Surface original import error for debugging
        logger.debug(f"huggingface_hub import error: {_HF_IMPORT_ERROR}")
        raise RuntimeError(msg)

    try:
        logger.info(f"Attempting to download model {filename} from {repo_id}")
        model_path = hf_hub_download(repo_id=repo_id, filename=filename)
        logger.info(f"Model downloaded to {model_path}")
    except RepositoryNotFoundError:
        msg = f"Hugging Face repository not found: {repo_id}"
        logger.error(msg)
        raise RuntimeError(msg)
    except EntryNotFoundError:
        msg = f"Model file not found in repo '{repo_id}': {filename}"
        logger.error(msg)
        raise RuntimeError(msg)
    except requests.exceptions.ConnectionError:
        msg = (
            "Network error: unable to reach Hugging Face. "
            "Check your internet connection."
        )
        logger.error(msg)
        raise RuntimeError(msg)
    except Exception as e:
        msg = f"Failed to download model from Hugging Face: {e}"
        logger.exception(msg)
        raise RuntimeError(msg)

    # Load with joblib and handle corrupted files
    try:
        pipeline = joblib.load(model_path)
        logger.info("Model loaded successfully from Hugging Face cache")
        return pipeline
    except Exception as e:
        # If the file is corrupted, attempt to remove it from the cache so
        # subsequent runs can retry downloading. Be careful and only remove
        # if the path exists and looks like a cache file.
        try:
            if os.path.exists(model_path):
                logger.warning(f"Removing corrupted model file: {model_path}")
                os.remove(model_path)
        except Exception:
            logger.exception("Failed to remove corrupted model file from disk")

        msg = f"Failed to load model artifact (corrupted or incompatible): {e}"
        logger.exception(msg)
        raise RuntimeError(msg)
