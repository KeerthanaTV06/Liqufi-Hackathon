"""
PointZero Graph Loader Module
==============================
Safe loader for the authority graph JSON file.
Validates the { "wallet": "...", "authority_edges": [...] } schema
and prevents path traversal.
"""

import json
import os
from typing import Optional

from backend.security import safe_file_path, validate_wallet_address


# --- Schema Constants ---

REQUIRED_TOP_KEYS = {"wallet", "authority_edges"}
REQUIRED_EDGE_KEYS = {"type", "block"}
VALID_EDGE_TYPES = frozenset({
    "token_approval",
    "proxy_admin_transfer",
    "ownership_transfer",
    "role_grant",
    "role_revoke",
})


# --- Public API ---

def load_authority_graph(path: str = None) -> dict:
    """
    Load and validate the authority graph from a JSON file.

    Args:
        path: Path to the authority_graph.json file.
              Defaults to backend/data/authority_graph.json.

    Returns:
        Parsed and validated authority graph dict with:
        - 'wallet': str (Ethereum address)
        - 'authority_edges': list of edge dicts

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the JSON is malformed or schema is invalid.
    """
    if path is None:
        path = os.path.join(
            os.path.dirname(__file__), "data", "authority_graph.json"
        )

    # Validate path safety
    resolved_path = safe_file_path(path)

    if not os.path.isfile(resolved_path):
        raise FileNotFoundError(
            f"Authority graph not found at: {resolved_path}"
        )

    # Read and parse JSON
    try:
        with open(resolved_path, "r", encoding="utf-8") as f:
            raw = f.read()
    except (IOError, OSError) as e:
        raise ValueError(f"Cannot read authority graph file: {e}") from e

    if not raw.strip():
        raise ValueError("Authority graph file is empty.")

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Authority graph contains invalid JSON: {e}"
        ) from e

    # Validate schema
    _validate_schema(data)

    return data


def get_authority_edges(graph: dict) -> list:
    """
    Extract the authority_edges list from a validated graph.

    Args:
        graph: Validated authority graph dict.

    Returns:
        List of authority edge dicts.
    """
    edges = graph.get("authority_edges", [])
    if not isinstance(edges, list):
        return []
    return edges


def get_graph_wallet(graph: dict) -> Optional[str]:
    """
    Extract the wallet address from a validated graph.

    Args:
        graph: Validated authority graph dict.

    Returns:
        The wallet address string, or None if missing.
    """
    return graph.get("wallet")


# --- Schema Validation ---

def _validate_schema(data: dict) -> None:
    """
    Validate the authority graph structure.

    Expected format:
    {
        "wallet": "0x...",
        "authority_edges": [
            {
                "type": "token_approval" | "proxy_admin_transfer" | ...,
                "contract": "0x...",
                "block": 12345,
                ...
            }
        ]
    }

    Raises:
        ValueError: If schema is invalid.
    """
    if not isinstance(data, dict):
        raise ValueError("Authority graph must be a JSON object.")

    missing_keys = REQUIRED_TOP_KEYS - set(data.keys())
    if missing_keys:
        raise ValueError(
            f"Authority graph missing required keys: {missing_keys}"
        )

    # Validate wallet field
    wallet = data["wallet"]
    if not isinstance(wallet, str) or not wallet.strip():
        raise ValueError("'wallet' must be a non-empty string.")

    # Validate authority_edges
    edges = data["authority_edges"]
    if not isinstance(edges, list):
        raise ValueError("'authority_edges' must be a JSON array.")

    for i, edge in enumerate(edges):
        if not isinstance(edge, dict):
            raise ValueError(
                f"authority_edges[{i}] must be a JSON object."
            )

        missing = REQUIRED_EDGE_KEYS - set(edge.keys())
        if missing:
            raise ValueError(
                f"authority_edges[{i}] missing required keys: {missing}"
            )

        edge_type = edge.get("type", "")
        if edge_type not in VALID_EDGE_TYPES:
            raise ValueError(
                f"authority_edges[{i}] has invalid type '{edge_type}'. "
                f"Valid types: {sorted(VALID_EDGE_TYPES)}"
            )

        block = edge.get("block")
        if not isinstance(block, int) or block < 0:
            raise ValueError(
                f"authority_edges[{i}] 'block' must be a non-negative integer."
            )
