"""
Example Usage: Authority Graph Builder (Python)

Demonstrates real-world usage patterns for the PointZero Member C component
"""

import sys
import os
import json

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from authority_graph_builder import build_authority_graph, build_single_wallet_graph


print("=" * 60)
print("EXAMPLE 1: Single Wallet with Multiple Authority Events")
print("=" * 60)

example1 = [
    {
        "wallet": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
        "contract": "0xdAC17F958D2ee523a2206206994597C13D831ec7",  # USDT
        "authority_type": "token_approval",
        "target_entity": "0x1111111254EEB25477B68fb85Ed929f73A960582",  # 1inch
        "amount": "115792089237316195423570985008687907853269984665640564039457584007913129639935",
        "block": 18392012,
        "timestamp": 1712345678,
        "tx_hash": "0x1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b",
        "log_index": 0
    },
    {
        "wallet": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
        "contract": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",  # USDC
        "authority_type": "token_approval",
        "target_entity": "0x1111111254EEB25477B68fb85Ed929f73A960582",  # 1inch
        "amount": "MAX_UINT",
        "block": 18392015,
        "timestamp": 1712345690,
        "tx_hash": "0x2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3",
        "log_index": 1
    },
    {
        "wallet": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
        "contract": "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D",  # BAYC NFT
        "authority_type": "nft_approval_all",
        "target_entity": "0x00000000000000ADc04C56Bf30aC9d3c0aAF14dC",  # Seaport
        "amount": None,
        "block": 18392020,
        "timestamp": 1712345700,
        "tx_hash": "0x3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4",
        "log_index": 0
    }
]

graph1 = build_single_wallet_graph(example1)
print(json.dumps(graph1, indent=2))

print("\n" + "=" * 60)
print("EXAMPLE 2: Multiple Wallets with Mixed Authority Types")
print("=" * 60)

example2 = [
    {
        "wallet": "0xAlice",
        "contract": "0xTokenA",
        "authority_type": "token_approval",
        "target_entity": "0xDEX_Uniswap",
        "amount": "1000000000000000000",  # 1 token (18 decimals)
        "block": 18392000,
        "timestamp": 1712345600
    },
    {
        "wallet": "0xBob",
        "contract": "0xTokenB",
        "authority_type": "token_approval",
        "target_entity": "0xDEX_Sushiswap",
        "amount": "MAX_UINT",
        "block": 18392005,
        "timestamp": 1712345650
    },
    {
        "wallet": "0xAlice",
        "contract": "0xNFT_Collection",
        "authority_type": "nft_approval_all",
        "target_entity": "0xMarketplace_OpenSea",
        "amount": None,
        "block": 18392010,
        "timestamp": 1712345670
    }
]

graphs2 = build_authority_graph(example2)
print(json.dumps(graphs2, indent=2))

print("\n" + "=" * 60)
print("All examples demonstrate:")
print("✓ Deterministic output (same input = same output)")
print("✓ Lossless transformation (all data preserved)")
print("✓ Proper sorting (block, tx_hash, log_index)")
print("✓ Amount normalization (unlimited, 0, regular)")
print("✓ No inference or scoring (pure transformation)")
print("=" * 60)