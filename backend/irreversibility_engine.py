"""
PointZero Irreversibility Engine
=================================
Core deterministic analysis engine that detects irreversible authority
leakage from an authority graph.

Pipeline:
  1. Validate wallet address
  2. Load authority graph (or accept it directly)
  3. Extract authority edges
  4. Evaluate all irreversibility rules
  5. Produce deterministic verdict

The engine is Liquify-ready: the graph input source (JSON file or API)
is fully replaceable via the graph_path parameter or by passing a
pre-loaded graph dict.
"""

from backend.security import validate_wallet_address
from backend.graph_loader import load_authority_graph, get_authority_edges, get_graph_wallet
from backend.authority_rules import evaluate_rules


class IrreversibilityEngine:
    """
    Deterministic engine that analyzes whether a wallet has crossed
    an irreversible trust boundary based on its authority edges.
    """

    def __init__(self, graph_path: str = None):
        """
        Initialize the engine.

        Args:
            graph_path: Path to authority_graph.json.
                        Defaults to backend/data/authority_graph.json.
        """
        self.graph_path = graph_path

    def analyze(self, wallet_address: str) -> dict:
        """
        Run the full irreversibility analysis pipeline.

        Args:
            wallet_address: Raw wallet address string (will be validated).

        Returns:
            Verdict dict with keys:
            - wallet: str (validated address)
            - verdict: "TRUST BROKEN" | "TRUST SAFE"
            - block: int (block of first breach, or 0)
            - reason: str (human-readable cause)
            - details: dict (extended analysis data)

        Raises:
            ValueError: If wallet address is invalid or graph is malformed.
            FileNotFoundError: If authority graph file is missing.
        """
        # Step 1: Validate wallet address
        validated_address = validate_wallet_address(wallet_address)

        # Step 2: Load authority graph from file
        graph = load_authority_graph(self.graph_path)

        # Step 3: Verify graph wallet matches the requested wallet
        graph_wallet = get_graph_wallet(graph)
        wallet_mismatch = False
        if graph_wallet:
            graph_wallet_norm = graph_wallet.lower().strip()
            if graph_wallet_norm != validated_address:
                wallet_mismatch = True

        # Step 4: Extract authority edges
        authority_edges = get_authority_edges(graph)

        # Step 5: Evaluate all irreversibility rules against edges
        triggered_rules = evaluate_rules(validated_address, authority_edges)

        # Step 6: Build deterministic verdict
        verdict = self._build_verdict(
            wallet=validated_address,
            triggered_rules=triggered_rules,
            authority_edges=authority_edges,
            wallet_mismatch=wallet_mismatch,
        )

        return verdict

    def analyze_graph(self, wallet_address: str, graph: dict) -> dict:
        """
        Analyze a pre-loaded authority graph (Liquify-ready interface).

        Use this method when the graph comes from an API or other source
        instead of a local JSON file.

        Args:
            wallet_address: Raw wallet address string.
            graph: Pre-loaded and validated authority graph dict.

        Returns:
            Verdict dict (same format as analyze()).
        """
        validated_address = validate_wallet_address(wallet_address)
        authority_edges = get_authority_edges(graph)
        triggered_rules = evaluate_rules(validated_address, authority_edges)

        return self._build_verdict(
            wallet=validated_address,
            triggered_rules=triggered_rules,
            authority_edges=authority_edges,
            wallet_mismatch=False,
        )

    # --- Private Helpers ---

    @staticmethod
    def _build_verdict(
        wallet: str,
        triggered_rules: list,
        authority_edges: list,
        wallet_mismatch: bool,
    ) -> dict:
        """Build the final verdict dict from analysis results."""

        if triggered_rules:
            # TRUST BROKEN — use earliest (first) triggered rule
            first_breach = triggered_rules[0]
            return {
                "wallet": wallet,
                "verdict": "TRUST BROKEN",
                "block": first_breach["block"],
                "reason": first_breach["rule_name"],
                "details": {
                    "total_breaches": len(triggered_rules),
                    "edges_analyzed": len(authority_edges),
                    "wallet_mismatch": wallet_mismatch,
                    "triggered_rules": [
                        {
                            "rule_id": r["rule_id"],
                            "rule_name": r["rule_name"],
                            "severity": r["severity"],
                            "block": r["block"],
                            "description": r["description"],
                        }
                        for r in triggered_rules
                    ],
                },
            }
        else:
            return {
                "wallet": wallet,
                "verdict": "TRUST SAFE",
                "block": 0,
                "reason": "No irreversible authority events detected",
                "details": {
                    "total_breaches": 0,
                    "edges_analyzed": len(authority_edges),
                    "wallet_mismatch": wallet_mismatch,
                    "triggered_rules": [],
                },
            }
