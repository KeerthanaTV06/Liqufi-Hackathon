"""
PointZero Graph Builder Module
===============================
Transforms raw authority events into the normalized Authority Graph schema.

Schema:
{
    "wallet": "0x...",
    "authority_edges": [
        { "type": "...", "contract": "...", "block": ..., ... }
    ]
}
"""

import json
import os
from datetime import datetime

class GraphBuilder:
    """
    Builder for constructing Authority Graph JSON objects.
    """

    def build_authority_graph(self, wallet_address: str, events: list) -> dict:
        """
        Construct the authority graph from raw events.

        Args:
            wallet_address: Validated wallet address string.
            events: List of raw event dicts from LiquifyClient.

        Returns:
            Dict matching the Authority Graph schema.
        """
        # Normalize wallet address
        wallet_norm = wallet_address.lower().strip()

        # Build edges list
        edges = []
        for event in events:
            edge = self._process_event(event)
            if edge:
                edges.append(edge)

        # Sort edges by block number
        edges.sort(key=lambda e: e.get("block", 0))

        return {
            "wallet": wallet_norm,
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "authority_edges": edges
        }

    def _process_event(self, event: dict) -> dict:
        """
        Validate and sanitize a single authority event edge.
        """
        # Ensure mandatory fields
        if not event.get("type") or not event.get("block"):
            return None

        # Copy fields to avoid mutating source
        edge = event.copy()

        # Normalize address fields if present
        for field in ["contract", "spender", "new_admin", "new_owner", "grantee"]:
            if field in edge:
                edge[field] = str(edge[field]).lower()

        # Ensure block is int
        try:
            edge["block"] = int(edge["block"])
        except (ValueError, TypeError):
            return None

        return edge


def save_graph_to_file(graph: dict, path: str = None) -> str:
    """
    Save the generated graph to a JSON file (useful for debugging/persistence).
    """
    if path is None:
        path = os.path.join(
            os.path.dirname(__file__), "data", "authority_graph.json"
        )

    # Use existing safe path logic if imports allowed, else manual check
    # Here we assume simple write since we control the path internally in analyze_wallet.py
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(graph, f, indent=2)
    
    return path
