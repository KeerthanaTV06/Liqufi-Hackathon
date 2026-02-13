"""
PointZero Security Module
=========================
Input validation, sanitization, and file-safety utilities.
All external inputs must pass through this module before processing.
"""

import re
import os

# --- Constants ---

WALLET_PATTERN = re.compile(r"^0x[0-9a-fA-F]{40}$")
MAX_INPUT_LENGTH = 256
ALLOWED_DATA_DIR = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "data")
)


# --- Wallet Validation ---

def validate_wallet_address(address: str) -> str:
    """
    Validate an Ethereum wallet address.

    Args:
        address: Raw address string from user input.

    Returns:
        Checksummed (lowercase-normalized) address string.

    Raises:
        ValueError: If the address is malformed.
    """
    if not isinstance(address, str):
        raise ValueError("Wallet address must be a string.")

    address = address.strip()

    if len(address) == 0:
        raise ValueError("Wallet address cannot be empty.")

    if len(address) > MAX_INPUT_LENGTH:
        raise ValueError(
            f"Input exceeds maximum length of {MAX_INPUT_LENGTH} characters."
        )

    if not WALLET_PATTERN.match(address):
        raise ValueError(
            f"Invalid Ethereum address format: '{address}'. "
            "Expected '0x' followed by 40 hexadecimal characters."
        )

    # Normalize to lowercase for deterministic comparisons
    return address.lower()


# --- General Input Sanitization ---

def sanitize_input(value: str) -> str:
    """
    Sanitize a generic string input.

    - Strips leading/trailing whitespace
    - Rejects null bytes and control characters
    - Enforces max length

    Args:
        value: Raw string input.

    Returns:
        Sanitized string.

    Raises:
        ValueError: If the input contains forbidden characters or is too long.
    """
    if not isinstance(value, str):
        raise ValueError("Input must be a string.")

    value = value.strip()

    if len(value) > MAX_INPUT_LENGTH:
        raise ValueError(
            f"Input exceeds maximum length of {MAX_INPUT_LENGTH} characters."
        )

    # Reject null bytes and control characters (except newline/tab)
    if re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", value):
        raise ValueError("Input contains forbidden control characters.")

    return value


# --- File Path Safety ---

def safe_file_path(path: str) -> str:
    """
    Ensure a file path resolves within the allowed data directory.
    Prevents directory traversal attacks.

    Args:
        path: Requested file path (relative or absolute).

    Returns:
        Resolved absolute path guaranteed to be inside backend/data/.

    Raises:
        ValueError: If the path escapes the allowed directory.
    """
    if not isinstance(path, str):
        raise ValueError("File path must be a string.")

    resolved = os.path.normpath(os.path.abspath(path))

    if not resolved.startswith(ALLOWED_DATA_DIR):
        raise ValueError(
            f"Access denied: path '{path}' resolves outside the allowed "
            f"data directory '{ALLOWED_DATA_DIR}'."
        )

    return resolved
