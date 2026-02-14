"""
Test Suite for Authority Graph Builder

Validates deterministic behavior, edge cases, and schema compliance
"""

import json
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from authority_graph_builder import build_authority_graph, build_single_wallet_graph, normalize_amount


def test_basic_transformation():
    """Test basic single event transformation"""
    events = [
        {
            "wallet": "0xABC",
            "contract": "0xTOKEN",
            "authority_type": "token_approval",
            "target_entity": "0xDEX",
            "amount": "1000000",
            "block": 100,
            "timestamp": 1712345678
        }
    ]
    
    result = build_authority_graph(events)
    
    expected = {
        "0xABC": {
            "wallet": "0xABC",
            "authority_edges": [
                {
                    "type": "token_approval",
                    "contract": "0xTOKEN",
                    "target_entity": "0xDEX",
                    "amount": "1000000",
                    "block": 100,
                    "timestamp": 1712345678,
                    "revocation_possible": "UNKNOWN"
                }
            ]
        }
    }
    
    assert result == expected, "Basic single event transformation"
    print("✓ Basic single event transformation")


def test_amount_normalization():
    """Test amount normalization"""
    assert normalize_amount("MAX_UINT") == "unlimited", "MAX_UINT → unlimited"
    assert normalize_amount("UNLIMITED") == "unlimited", "UNLIMITED → unlimited"
    assert normalize_amount(None) == "unlimited", "None → unlimited"
    assert normalize_amount("0") == "0", "Zero string"
    assert normalize_amount(0) == "0", "Zero number"
    assert normalize_amount("1000000") == "1000000", "Regular amount string"
    assert normalize_amount(1000000) == "1000000", "Regular amount number"
    print("✓ Amount normalization")


def test_block_ordering():
    """Test block ordering (determinism)"""
    events = [
        {
            "wallet": "0xABC",
            "contract": "0xTOKEN1",
            "authority_type": "token_approval",
            "target_entity": "0xDEX",
            "amount": "100",
            "block": 103,
            "timestamp": 1712345690
        },
        {
            "wallet": "0xABC",
            "contract": "0xTOKEN2",
            "authority_type": "token_approval",
            "target_entity": "0xDEX",
            "amount": "200",
            "block": 101,
            "timestamp": 1712345670
        },
        {
            "wallet": "0xABC",
            "contract": "0xTOKEN3",
            "authority_type": "token_approval",
            "target_entity": "0xDEX",
            "amount": "300",
            "block": 102,
            "timestamp": 1712345680
        }
    ]
    
    result = build_authority_graph(events)
    edges = result["0xABC"]["authority_edges"]
    
    assert edges[0]["block"] == 101, "First edge is block 101"
    assert edges[1]["block"] == 102, "Second edge is block 102"
    assert edges[2]["block"] == 103, "Third edge is block 103"
    assert edges[0]["amount"] == "200", "Correct amount for first edge"
    assert edges[1]["amount"] == "300", "Correct amount for second edge"
    assert edges[2]["amount"] == "100", "Correct amount for third edge"
    print("✓ Block ordering (determinism)")


def test_multiple_wallets():
    """Test multiple wallets"""
    events = [
        {
            "wallet": "0xABC",
            "contract": "0xTOKEN",
            "authority_type": "token_approval",
            "target_entity": "0xDEX",
            "amount": "100",
            "block": 100,
            "timestamp": 1712345678
        },
        {
            "wallet": "0xDEF",
            "contract": "0xTOKEN",
            "authority_type": "token_approval",
            "target_entity": "0xDEX",
            "amount": "200",
            "block": 101,
            "timestamp": 1712345680
        },
        {
            "wallet": "0xABC",
            "contract": "0xNFT",
            "authority_type": "nft_approval",
            "target_entity": "0xMARKET",
            "amount": None,
            "block": 102,
            "timestamp": 1712345690
        }
    ]
    
    result = build_authority_graph(events)
    
    assert len(result) == 2, "Two wallets in output"
    assert len(result["0xABC"]["authority_edges"]) == 2, "Wallet 0xABC has 2 edges"
    assert len(result["0xDEF"]["authority_edges"]) == 1, "Wallet 0xDEF has 1 edge"
    print("✓ Multiple wallets")


def test_optional_fields():
    """Test optional fields (tx_hash, log_index)"""
    events = [
        {
            "wallet": "0xABC",
            "contract": "0xTOKEN",
            "authority_type": "token_approval",
            "target_entity": "0xDEX",
            "amount": "100",
            "block": 100,
            "timestamp": 1712345678,
            "tx_hash": "0xTX1",
            "log_index": 5
        }
    ]
    
    result = build_authority_graph(events)
    edge = result["0xABC"]["authority_edges"][0]
    
    assert edge["tx_hash"] == "0xTX1", "tx_hash preserved"
    assert edge["log_index"] == 5, "log_index preserved"
    print("✓ Optional fields (tx_hash, log_index)")


def test_deterministic_sorting():
    """Test deterministic sorting with tx_hash and log_index"""
    events = [
        {
            "wallet": "0xABC",
            "contract": "0xTOKEN1",
            "authority_type": "token_approval",
            "target_entity": "0xDEX",
            "amount": "100",
            "block": 100,
            "timestamp": 1712345678,
            "tx_hash": "0xTX2",
            "log_index": 1
        },
        {
            "wallet": "0xABC",
            "contract": "0xTOKEN2",
            "authority_type": "token_approval",
            "target_entity": "0xDEX",
            "amount": "200",
            "block": 100,
            "timestamp": 1712345678,
            "tx_hash": "0xTX1",
            "log_index": 0
        },
        {
            "wallet": "0xABC",
            "contract": "0xTOKEN3",
            "authority_type": "token_approval",
            "target_entity": "0xDEX",
            "amount": "300",
            "block": 100,
            "timestamp": 1712345678,
            "tx_hash": "0xTX1",
            "log_index": 2
        }
    ]
    
    result = build_authority_graph(events)
    edges = result["0xABC"]["authority_edges"]
    
    # Same block, sorted by tx_hash then log_index
    assert edges[0]["tx_hash"] == "0xTX1", "First by tx_hash"
    assert edges[0]["log_index"] == 0, "First by log_index within tx"
    assert edges[1]["log_index"] == 2, "Second by log_index within tx"
    assert edges[2]["tx_hash"] == "0xTX2", "Last tx_hash"
    print("✓ Deterministic sorting with tx_hash and log_index")


def test_empty_input():
    """Test empty input"""
    result = build_authority_graph([])
    assert result == {}, "Empty array returns empty object"
    print("✓ Empty input")


def test_validation_errors():
    """Test validation errors"""
    try:
        build_authority_graph("not a list")
        assert False, "Should reject non-list input"
    except ValueError:
        pass
    
    try:
        build_authority_graph([{"contract": "0xTOKEN"}])
        assert False, "Should reject event missing wallet"
    except ValueError:
        pass
    
    try:
        build_authority_graph([{"wallet": "0xABC"}])
        assert False, "Should reject event missing contract"
    except ValueError:
        pass
    
    try:
        build_authority_graph([{
            "wallet": "0xABC",
            "contract": "0xTOKEN",
            "authority_type": "token_approval",
            "target_entity": "0xDEX",
            "amount": "100"
            # missing block and timestamp
        }])
        assert False, "Should reject event missing block"
    except ValueError:
        pass
    
    print("✓ Validation errors")


def test_single_wallet_graph():
    """Test single wallet convenience method"""
    events = [
        {
            "wallet": "0xABC",
            "contract": "0xTOKEN",
            "authority_type": "token_approval",
            "target_entity": "0xDEX",
            "amount": "100",
            "block": 100,
            "timestamp": 1712345678
        }
    ]
    
    result = build_single_wallet_graph(events)
    
    assert result["wallet"] == "0xABC", "Returns single wallet graph"
    assert len(result["authority_edges"]) == 1, "Contains edges"
    print("✓ Single wallet convenience method")


def test_determinism():
    """Test determinism (same input = same output)"""
    events = [
        {
            "wallet": "0xABC",
            "contract": "0xTOKEN1",
            "authority_type": "token_approval",
            "target_entity": "0xDEX",
            "amount": "100",
            "block": 103,
            "timestamp": 1712345690
        },
        {
            "wallet": "0xDEF",
            "contract": "0xTOKEN2",
            "authority_type": "token_approval",
            "target_entity": "0xDEX",
            "amount": "200",
            "block": 101,
            "timestamp": 1712345670
        }
    ]
    
    result1 = build_authority_graph(events)
    result2 = build_authority_graph(events)
    
    assert result1 == result2, "Same input produces identical output"
    print("✓ Determinism test (same input = same output)")


if __name__ == "__main__":
    print("\n🧪 Running Authority Graph Builder Tests\n")
    
    try:
        test_basic_transformation()
        test_amount_normalization()
        test_block_ordering()
        test_multiple_wallets()
        test_optional_fields()
        test_deterministic_sorting()
        test_empty_input()
        test_validation_errors()
        test_single_wallet_graph()
        test_determinism()
        
        print("\n✅ All tests passed!\n")
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}\n")
        exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}\n")
        exit(1)