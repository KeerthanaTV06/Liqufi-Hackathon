"""
PointZero Verdict Generator
=============================
Writes the irreversibility verdict to a JSON file.
Uses atomic writes for crash safety.
"""

import json
import os
import tempfile

from backend.security import safe_file_path


# --- Schema Validation ---

REQUIRED_VERDICT_KEYS = {"wallet", "verdict", "block", "reason"}
VALID_VERDICTS = {"TRUST BROKEN", "TRUST SAFE"}


def _validate_verdict(verdict_data: dict) -> None:
    """
    Validate that verdict data conforms to the expected schema.

    Expected format:
    {
        "wallet": "0x...",
        "verdict": "TRUST BROKEN" | "TRUST SAFE",
        "block": 12345,
        "reason": "..."
    }

    Raises:
        ValueError: If the verdict is missing keys or has invalid values.
    """
    if not isinstance(verdict_data, dict):
        raise ValueError("Verdict data must be a dictionary.")

    missing = REQUIRED_VERDICT_KEYS - set(verdict_data.keys())
    if missing:
        raise ValueError(f"Verdict missing required keys: {missing}")

    if verdict_data["verdict"] not in VALID_VERDICTS:
        raise ValueError(
            f"Invalid verdict value: '{verdict_data['verdict']}'. "
            f"Must be one of: {VALID_VERDICTS}"
        )

    if not isinstance(verdict_data["block"], int):
        raise ValueError("'block' must be an integer.")

    if not isinstance(verdict_data["reason"], str):
        raise ValueError("'reason' must be a string.")

    if not isinstance(verdict_data["wallet"], str):
        raise ValueError("'wallet' must be a string.")


# --- Public API ---

def write_verdict(verdict_data: dict, output_path: str = None) -> str:
    """
    Write the verdict to a JSON file using atomic write.

    The write is crash-safe: data is written to a temp file first,
    then atomically renamed to the target path.

    Args:
        verdict_data: Validated verdict dict.
        output_path: Destination file path.
                     Defaults to backend/data/irreversibility_verdict.json.

    Returns:
        Absolute path of the written file.

    Raises:
        ValueError: If verdict data is invalid or path is unsafe.
    """
    # Validate verdict schema
    _validate_verdict(verdict_data)

    # Resolve output path
    if output_path is None:
        output_path = os.path.join(
            os.path.dirname(__file__), "data", "irreversibility_verdict.json"
        )

    resolved_path = safe_file_path(output_path)

    # Ensure directory exists
    os.makedirs(os.path.dirname(resolved_path), exist_ok=True)

    # Atomic write: write to temp file, then rename
    dir_name = os.path.dirname(resolved_path)
    tmp_path = None
    try:
        fd, tmp_path = tempfile.mkstemp(
            suffix=".tmp",
            prefix="verdict_",
            dir=dir_name,
        )
        with os.fdopen(fd, "w", encoding="utf-8") as tmp_file:
            json.dump(verdict_data, tmp_file, indent=2, ensure_ascii=False)
            tmp_file.write("\n")

        # Atomic rename (same filesystem)
        os.replace(tmp_path, resolved_path)
        tmp_path = None  # Successfully renamed, no cleanup needed

    except Exception:
        # Clean up temp file on failure
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise

    return resolved_path
