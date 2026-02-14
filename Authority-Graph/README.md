# Authority Graph Builder (Member C)

Pure transformation layer for PointZero irreversibility analysis pipeline.

## Design Principles

✅ **Deterministic** - Same input always produces same output  
✅ **Lossless** - Preserves all input data  
✅ **No Inference** - No risk scoring, no heuristics  
✅ **Pure Transformation** - Maps events to graph structure  
✅ **No External Dependencies** - No database, no blockchain calls  

## What It Does

- Accepts array of authority transition events
- Groups events by wallet address
- Normalizes amount representations
- Sorts edges by block number (ascending)
- Emits structured authority graph
- Sets `revocation_possible: "UNKNOWN"` for downstream analysis

## What It Does NOT Do

❌ Score risk  
❌ Detect irreversibility  
❌ Assign verdicts  
❌ Make blockchain calls  
❌ Store data  
❌ Apply heuristics  

## Input Schema

```json
[
  {
    "wallet": "0xABC",
    "contract": "0xTOKEN",
    "authority_type": "token_approval",
    "target_entity": "0xDEX",
    "amount": "MAX_UINT",
    "block": 18392012,
    "timestamp": 1712345678,
    "tx_hash": "0xTX1",      // optional
    "log_index": 0           // optional
  }
]
```

### Required Fields
- `wallet` - Wallet address granting authority
- `contract` - Contract address receiving authority
- `authority_type` - Type of authority (e.g., "token_approval", "nft_approval_all")
- `target_entity` - Address that will receive authority
- `amount` - Amount or scope (string, number, null, or "MAX_UINT")
- `block` - Block number
- `timestamp` - Unix timestamp

### Optional Fields
- `tx_hash` - Transaction hash (improves determinism)
- `log_index` - Event log index within transaction (improves determinism)

## Output Schema

```json
{
  "0xABC": {
    "wallet": "0xABC",
    "authority_edges": [
      {
        "type": "token_approval",
        "contract": "0xTOKEN",
        "target_entity": "0xDEX",
        "amount": "unlimited",
        "block": 18392012,
        "timestamp": 1712345678,
        "tx_hash": "0xTX1",
        "log_index": 0,
        "revocation_possible": "UNKNOWN"
      }
    ]
  }
}
```

## Amount Normalization

| Input | Output |
|-------|--------|
| `"MAX_UINT"` | `"unlimited"` |
| `"UNLIMITED"` | `"unlimited"` |
| `null` | `"unlimited"` |
| `undefined` | `"unlimited"` |
| `"0"` | `"0"` |
| `0` | `"0"` |
| `"1000000"` | `"1000000"` |
| `1000000` | `"1000000"` |

## Sorting Rules

Edges are sorted within each wallet using:

1. **Primary**: Block number (ascending)
2. **Secondary**: Transaction hash (lexicographic)
3. **Tertiary**: Log index (numeric)
4. **Fallback**: Timestamp (ascending)

This ensures deterministic output regardless of input order.

---

## Usage Examples

### Node.js

```javascript
const { buildAuthorityGraph, buildSingleWalletGraph } = require('./authority-graph-builder');

// Multiple wallets
const events = [
  {
    wallet: "0xABC",
    contract: "0xTOKEN",
    authority_type: "token_approval",
    target_entity: "0xDEX",
    amount: "MAX_UINT",
    block: 18392012,
    timestamp: 1712345678,
    tx_hash: "0xTX1",
    log_index: 0
  },
  {
    wallet: "0xDEF",
    contract: "0xNFT",
    authority_type: "nft_approval_all",
    target_entity: "0xMARKET",
    amount: null,
    block: 18392015,
    timestamp: 1712345690
  }
];

const graphs = buildAuthorityGraph(events);
console.log(JSON.stringify(graphs, null, 2));

// Single wallet (convenience method)
const singleWalletEvents = events.filter(e => e.wallet === "0xABC");
const graph = buildSingleWalletGraph(singleWalletEvents);
console.log(JSON.stringify(graph, null, 2));
```

### Python

```python
from authority_graph_builder import build_authority_graph, build_single_wallet_graph
import json

# Multiple wallets
events = [
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
        "wallet": "0xDEF",
        "contract": "0xNFT",
        "authority_type": "nft_approval_all",
        "target_entity": "0xMARKET",
        "amount": None,
        "block": 18392015,
        "timestamp": 1712345690
    }
]

graphs = build_authority_graph(events)
print(json.dumps(graphs, indent=2))

# Single wallet (convenience method)
single_wallet_events = [e for e in events if e["wallet"] == "0xABC"]
graph = build_single_wallet_graph(single_wallet_events)
print(json.dumps(graph, indent=2))
```

---

## Testing

### Node.js

```bash
node test-authority-graph-builder.js
```

### Python

```bash
python test_authority_graph_builder.py
```

Both test suites validate:
- Basic transformation
- Amount normalization
- Block ordering (determinism)
- Multiple wallet handling
- Optional field preservation
- Sorting with tx_hash and log_index
- Empty input handling
- Validation errors
- Single wallet convenience method
- Determinism (same input = same output)

---

## Pipeline Integration

### Input Source (Member A)
Member A extracts raw authority events from blockchain and passes them to Member C.

### Output Consumer (Member B)
Member B receives the normalized authority graph and applies:
- Risk scoring
- Irreversibility detection
- Verdict assignment
- Pattern matching

### Data Flow

```
Member A          Member C              Member B
(Extractor)   →   (Graph Builder)   →   (Analyzer)
   │                    │                    │
   │  Raw Events        │  Authority Graph   │
   │ ──────────────→    │ ──────────────→    │
   │                    │                    │
   │                    │                    ↓
   │                    │              Risk Analysis
   │                    │              Irreversibility
   │                    │              Verdicts
```

---

## Error Handling

All validation errors throw with descriptive messages:

```javascript
// Missing required field
Error: Event missing required field: wallet

// Invalid input type
Error: Input must be an array of events

// Multiple wallets in single-wallet method
Error: Multiple wallets detected. Use buildAuthorityGraph() for batch processing.
```

---

## Performance Characteristics

- **Time Complexity**: O(n log n) where n = number of events (due to sorting)
- **Space Complexity**: O(n) for output storage
- **Determinism**: Guaranteed via stable sorting
- **Memory**: No accumulation, single-pass transformation

---

## Compliance

✅ No database dependencies  
✅ No network calls  
✅ No external APIs  
✅ Pure functions  
✅ Stateless transformation  
✅ Deterministic output  
✅ Lossless data preservation  

---