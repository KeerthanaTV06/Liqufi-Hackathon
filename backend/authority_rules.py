"""
PointZero Authority Rules Module
=================================
Deterministic rule definitions that detect irreversible authority leakage
from on-chain authority edges. Each rule represents a trust boundary that,
once crossed, cannot be undone.

Rules operate on authority_edges from the authority graph:
    {
        "type": "token_approval" | "proxy_admin_transfer" | "ownership_transfer" | "role_grant",
        "contract": "0x...",
        "spender": "0x...",       (for approvals)
        "new_admin": "0x...",     (for proxy transfers)
        "new_owner": "0x...",     (for ownership transfers)
        "role": "...",            (for role grants)
        "amount": "...",          (string — may be MAX_UINT)
        "block": int
    }
"""

# --- Constants ---

# Solidity type(uint256).max = 2^256 - 1
MAX_UINT256 = str(2**256 - 1)

# Common representations of unlimited/max approval amounts
UNLIMITED_INDICATORS = frozenset({
    MAX_UINT256,
    "unlimited",
    "UNLIMITED",
    "MAX",
    "max",
    "MAX_UINT256",
    "type(uint256).max",
    "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
})


# --- Rule Definitions ---

IRREVERSIBILITY_RULES = [
    {
        "id": "RULE_001",
        "name": "Unlimited Token Approval (MAX_UINT256)",
        "description": (
            "An unlimited (type(uint256).max) token approval was granted to "
            "a spender, giving them unrestricted access to drain all tokens. "
            "This approval persists until explicitly revoked."
        ),
        "edge_type": "token_approval",
        "severity": "CRITICAL",
    },
    {
        "id": "RULE_002",
        "name": "Proxy Admin Transfer",
        "description": (
            "The admin role of a proxy contract was transferred to another "
            "address. The new admin can upgrade the contract implementation "
            "to arbitrary code, permanently altering all future execution."
        ),
        "edge_type": "proxy_admin_transfer",
        "severity": "CRITICAL",
    },
    {
        "id": "RULE_003",
        "name": "Ownership Transfer",
        "description": (
            "Contract ownership was transferred to another address via "
            "transferOwnership(). The previous owner permanently loses all "
            "administrative privileges over the contract."
        ),
        "edge_type": "ownership_transfer",
        "severity": "CRITICAL",
    },
    {
        "id": "RULE_004",
        "name": "Role Grant Without Revoke",
        "description": (
            "A privileged role was granted to an address without a "
            "corresponding revoke of the same role. This creates a "
            "persistent authority leak that remains active indefinitely."
        ),
        "edge_type": "role_grant",
        "severity": "HIGH",
    },
]


# --- Detection Functions ---

def _detect_unlimited_approval(edge: dict) -> bool:
    """
    Detect if a token_approval edge has an unlimited (MAX_UINT256) amount.

    Checks against multiple string representations of unlimited approval.
    """
    if edge.get("type") != "token_approval":
        return False

    amount = str(edge.get("amount", "")).strip()
    return amount in UNLIMITED_INDICATORS


def _detect_proxy_admin_transfer(edge: dict) -> bool:
    """
    Detect if a proxy contract's admin was transferred.

    Requires a valid new_admin address different from implied current state.
    """
    if edge.get("type") != "proxy_admin_transfer":
        return False

    new_admin = edge.get("new_admin", "")
    return (
        isinstance(new_admin, str)
        and len(new_admin) > 0
        and new_admin != "0x0000000000000000000000000000000000000000"
    )


def _detect_ownership_transfer(edge: dict) -> bool:
    """
    Detect if contract ownership was transferred.

    Requires a valid new_owner address (non-zero).
    """
    if edge.get("type") != "ownership_transfer":
        return False

    new_owner = edge.get("new_owner", "")
    return (
        isinstance(new_owner, str)
        and len(new_owner) > 0
        and new_owner != "0x0000000000000000000000000000000000000000"
    )


def _detect_role_grant_without_revoke(edge: dict, all_edges: list) -> bool:
    """
    Detect if a role was granted without a corresponding revoke.

    Scans all edges for a matching role_revoke that cancels this grant.
    If no revoke is found, the role grant is an open authority leak.
    """
    if edge.get("type") != "role_grant":
        return False

    role = edge.get("role", "")
    grantee = edge.get("grantee", edge.get("spender", ""))
    contract = edge.get("contract", "")
    grant_block = edge.get("block", 0)

    if not role or not grantee:
        return False

    # Search for a corresponding revoke AFTER this grant
    for other in all_edges:
        if (
            other.get("type") == "role_revoke"
            and other.get("role", "") == role
            and other.get("grantee", other.get("spender", "")) == grantee
            and other.get("contract", "") == contract
            and other.get("block", 0) > grant_block
        ):
            return False  # Role was revoked — not an open leak

    return True  # No revoke found — open authority leak


# --- Detector Registry ---

_DETECTORS = {
    "token_approval": _detect_unlimited_approval,
    "proxy_admin_transfer": _detect_proxy_admin_transfer,
    "ownership_transfer": _detect_ownership_transfer,
    # role_grant uses a special signature (needs all_edges), handled separately
}


# --- Public API ---

def evaluate_rules(wallet: str, authority_edges: list) -> list:
    """
    Evaluate all irreversibility rules against a wallet's authority edges.

    Args:
        wallet: Validated wallet address.
        authority_edges: List of authority edge dicts from the graph.

    Returns:
        List of triggered rule dicts, each containing:
        - rule_id, rule_name, severity, description
        - triggering_edge (the edge that matched)
        - block (block number where the breach occurred)

        Sorted by block number (earliest breach first).
    """
    if not isinstance(authority_edges, list):
        return []

    triggered = []

    for edge in authority_edges:
        if not isinstance(edge, dict):
            continue

        edge_type = edge.get("type", "")

        for rule in IRREVERSIBILITY_RULES:
            if rule["edge_type"] != edge_type:
                continue

            # Special handling for role_grant (needs full edge list)
            if edge_type == "role_grant":
                matched = _detect_role_grant_without_revoke(edge, authority_edges)
            else:
                detector = _DETECTORS.get(edge_type)
                if detector is None:
                    continue
                matched = detector(edge)

            if matched:
                triggered.append({
                    "rule_id": rule["id"],
                    "rule_name": rule["name"],
                    "severity": rule["severity"],
                    "description": rule["description"],
                    "triggering_edge": edge,
                    "block": edge.get("block", 0),
                })

    # Deterministic ordering: earliest breach first
    triggered.sort(key=lambda t: t["block"])

    return triggered
