"""
PointZero Member C: Authority Graph Builder

Pure transformation layer that converts authority events into normalized graph structure.
- Deterministic: Same input always produces same output
- Lossless: Preserves all input data
- No inference: No risk scoring, no heuristics
"""

from typing import List, Dict, Any, Optional


def normalize_amount(amount: Any) -> str:
    """
    Normalize amount field to consistent string representation
    
    Args:
        amount: Raw amount value (string, number, or None)
        
    Returns:
        Normalized amount as string
    """
    if amount is None:
        return "unlimited"
    
    amount_str = str(amount).upper()
    
    # Handle common unlimited approval patterns
    if (amount_str == "MAX_UINT" or 
        amount_str == "UNLIMITED" or 
        "115792089237316195423570985008687907853269984665640564039457584007913129639935" in amount_str):
        return "unlimited"
    
    # Handle zero as string
    if amount_str == "0":
        return "0"
    
    # Return as string to preserve precision
    return str(amount)


def build_authority_graph(events: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    Build authority graph from array of authority events
    
    Args:
        events: List of authority transition events
        
    Returns:
        Dictionary mapping wallet addresses to their authority graphs
        
    Raises:
        ValueError: If input is invalid or required fields are missing
    """
    # Validate input
    if not isinstance(events, list):
        raise ValueError("Input must be a list of events")
    
    if len(events) == 0:
        return {}
    
    # Group events by wallet
    wallet_groups: Dict[str, List[Dict[str, Any]]] = {}
    
    for event in events:
        # Validate required fields
        required_fields = ["wallet", "contract", "authority_type", "target_entity", "block", "timestamp"]
        for field in required_fields:
            if field not in event or event[field] is None:
                raise ValueError(f"Event missing required field: {field}")
        
        wallet = event["wallet"]
        
        if wallet not in wallet_groups:
            wallet_groups[wallet] = []
        
        # Build normalized edge
        edge = {
            "type": event["authority_type"],
            "contract": event["contract"],
            "target_entity": event["target_entity"],
            "amount": normalize_amount(event.get("amount")),
            "block": int(event["block"]),
            "timestamp": int(event["timestamp"]),
            "revocation_possible": "UNKNOWN"
        }
        
        # Add optional fields if present
        if "tx_hash" in event and event["tx_hash"] is not None:
            edge["tx_hash"] = event["tx_hash"]
        if "log_index" in event and event["log_index"] is not None:
            edge["log_index"] = int(event["log_index"])
        
        wallet_groups[wallet].append(edge)
    
    # Sort edges within each wallet group by block ascending
    # Secondary sort by tx_hash and log_index for determinism
    for wallet in wallet_groups:
        wallet_groups[wallet].sort(key=lambda x: (
            x["block"],
            x.get("tx_hash", ""),
            x.get("log_index", 0),
            x["timestamp"]
        ))
    
    # Build output format
    results = {}
    
    for wallet, edges in wallet_groups.items():
        results[wallet] = {
            "wallet": wallet,
            "authority_edges": edges
        }
    
    return results


def build_single_wallet_graph(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Build authority graph for a single wallet (convenience method)
    
    Args:
        events: List of authority events for one wallet
        
    Returns:
        Single wallet authority graph
        
    Raises:
        ValueError: If no events provided or multiple wallets detected
    """
    graphs = build_authority_graph(events)
    wallets = list(graphs.keys())
    
    if len(wallets) == 0:
        raise ValueError("No events provided")
    
    if len(wallets) > 1:
        raise ValueError("Multiple wallets detected. Use build_authority_graph() for batch processing.")
    
    return graphs[wallets[0]]


# Example usage (commented out for library use)
if __name__ == "__main__":
    import json
    
    example_events = [
        {
            "wallet": "0xABC",
            "contract": "0xTOKEN",
            "authority_type": "token_approval",
            "target_entity": "0xDEX",
            "amount": "MAX_UINT",
            "block": 18392012,
            "timestamp": 1712345678,
            "tx_hash": "0xTX1",
            "log_index": 0
        },
        {
            "wallet": "0xABC",
            "contract": "0xNFT",
            "authority_type": "nft_approval_all",
            "target_entity": "0xMARKET",
            "amount": None,
            "block": 18392015,
            "timestamp": 1712345690,
            "tx_hash": "0xTX2",
            "log_index": 1
        },
        {
            "wallet": "0xDEF",
            "contract": "0xTOKEN",
            "authority_type": "token_approval",
            "target_entity": "0xDEX",
            "amount": "1000000000000000000",
            "block": 18392010,
            "timestamp": 1712345670,
            "tx_hash": "0xTX3",
            "log_index": 0
        }
    ]
    
    graphs = build_authority_graph(example_events)
    print(json.dumps(graphs, indent=2))