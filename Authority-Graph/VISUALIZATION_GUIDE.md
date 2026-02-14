# 🎨 Authority Graph Visualization Guide

## Overview

This guide demonstrates how to visualize blockchain authority relationships using the Authority Graph Builder. We provide multiple visualization options to suit different needs.

---

## 🚀 Quick Start

### Option 1: Interactive Web Visualization (Recommended for Presentations)

```bash
# Open in browser
open examples/visualize-graph.html
```

**What you'll see:**
- Interactive force-directed graph
- Drag nodes to rearrange
- Hover for detailed information
- Beautiful color-coded visualization

### Option 2: Terminal Visualization (Fastest)

```bash
# Run in terminal
node examples/visualize-graph-ascii.js
```

**What you'll see:**
- Three different ASCII art styles
- Statistics and metrics
- Works anywhere, no dependencies

### Option 3: High-Quality Image (Best for Reports)

```bash
# Install dependencies first
pip install networkx matplotlib

# Generate image
python examples/visualize_graph.py
```

**What you'll get:**
- Professional PNG image (300 DPI)
- Perfect for papers and reports
- Customizable layout and colors

---

## 📊 Visualization Examples

### Example 1: Simple Authority Flow

**Input:**
```javascript
{
  wallet: "0xAlice",
  contract: "0xUSDT",
  authority_type: "token_approval",
  target_entity: "0xUniswap",
  amount: "unlimited"
}
```

**Visual Representation:**
```
👤 Alice's Wallet
    │
    ├─ owns
    ▼
💰 USDT Token
    │
    ├─ approves (unlimited)
    ▼
🔄 Uniswap DEX
```

### Example 2: Multiple Approvals

**Scenario:** Alice approves multiple DEXs for different tokens

```
👤 0xAlice
    │
    ├─ 💰 USDT ──▶ 🔄 Uniswap [unlimited]
    │
    ├─ 💰 USDC ──▶ 🔄 Uniswap [1000000000000000000]
    │
    └─ 🎨 BAYC NFT ──▶ 🏪 OpenSea [all tokens]
```

### Example 3: Multi-Wallet Graph

**Scenario:** Three wallets with various approvals

```
Network Graph:
- 3 Wallets (Alice, Bob, Charlie)
- 5 Contracts (USDT, USDC, DAI, BAYC, CryptoPunks)
- 3 Targets (Uniswap, SushiSwap, OpenSea)
- 6 Authority Edges
```

---

## 🎯 Use Cases

### 1. Security Auditing
**Goal:** Identify risky unlimited approvals

```bash
node examples/visualize-graph-ascii.js | grep "unlimited"
```

**Look for:**
- Red flags: Multiple unlimited approvals
- Suspicious targets: Unknown contracts
- Old approvals: High block numbers

### 2. Portfolio Analysis
**Goal:** Understand wallet's authority landscape

**Visualization shows:**
- All active approvals
- Which DEXs have access
- Token vs NFT approvals
- Approval amounts

### 3. Compliance Reporting
**Goal:** Generate audit trail

```bash
python examples/visualize_graph.py
# Generates authority_graph.png for reports
```

### 4. User Education
**Goal:** Help users understand their approvals

**Interactive HTML shows:**
- Visual representation of risks
- Easy-to-understand relationships
- Hover details for each approval

---

## 🔍 Reading the Visualizations

### Color Coding

| Color | Type | Meaning |
|-------|------|---------|
| 🟢 Green | Wallet | User's wallet address |
| 🔵 Blue | Token | ERC-20 token contract |
| 🟠 Orange | NFT | ERC-721/1155 NFT contract |
| 🔴 Red | Target | DEX/Marketplace with approval |

### Edge Types

| Arrow | Type | Meaning |
|-------|------|---------|
| Gray → | Ownership | Wallet owns tokens |
| Red ⇒ | Approval | Contract approved to target |

### Icons (ASCII)

| Icon | Meaning |
|------|---------|
| 👤 | Wallet/User |
| 💰 | Token Contract |
| 🎨 | NFT Contract |
| 🔄 | DEX (Swap) |
| 🏪 | Marketplace |

---

## 📈 Graph Metrics

### Statistics Shown

1. **Total Wallets**: Number of unique wallet addresses
2. **Authority Edges**: Total approval relationships
3. **Unique Contracts**: Number of different contracts
4. **Unique Targets**: Number of different DEXs/marketplaces

### Example Output:
```
📊 GRAPH STATISTICS:
   Wallets:          3
   Authority Edges:  6
   Unique Contracts: 5
   Unique Targets:   3
```

---

## 🛠️ Customization

### Change Sample Data

Edit any example file to use your own data:

```javascript
const myEvents = [
    {
        wallet: "0xYourAddress",
        contract: "0xTokenAddress",
        authority_type: "token_approval",
        target_entity: "0xDEXAddress",
        amount: "1000000000000000000",
        block: 18392000,
        timestamp: 1712345600
    }
];

const graph = buildAuthorityGraph(myEvents);
```

### Adjust Visual Style

**HTML (D3.js):**
```javascript
// Change node sizes
.attr('r', d => d.type === 'wallet' ? 30 : 25)

// Change colors
const colorMap = {
    wallet: '#YOUR_COLOR',
    // ...
};
```

**Python (Matplotlib):**
```python
# Change figure size
fig, ax = plt.subplots(figsize=(20, 16))

# Change node colors
node_colors = {
    'wallet': '#YOUR_COLOR',
    # ...
}
```

---

## 💡 Best Practices

### For Presentations
1. Use **HTML/D3.js** visualization
2. Open in full-screen browser
3. Demonstrate interactivity
4. Zoom in on specific relationships

### For Reports
1. Use **Python/NetworkX** visualization
2. Export as high-DPI PNG
3. Include legend and statistics
4. Add annotations if needed

### For Quick Analysis
1. Use **ASCII terminal** visualization
2. Pipe output to file for records
3. Use grep to find specific patterns
4. Share via text/email easily

### For Development
1. Use **ASCII** for quick debugging
2. Verify graph structure
3. Check edge relationships
4. Validate data transformation

---

## 🔗 Integration Examples

### Web Application

```html
<iframe src="visualize-graph.html" width="100%" height="600px"></iframe>
```

### CLI Tool

```bash
#!/bin/bash
# analyze-wallet.sh
node examples/visualize-graph-ascii.js > wallet-report.txt
echo "Report saved to wallet-report.txt"
```

### Python Script

```python
from authority_graph_builder import build_authority_graph
from visualize_graph import visualize_authority_graph

def analyze_wallet(events):
    graph = build_authority_graph(events)
    visualize_authority_graph(graph, 'analysis.png')
    return graph
```

---

## 🎓 Understanding Authority Graphs

### What is an Authority Graph?

An authority graph represents the relationships between:
- **Wallets**: Users who own tokens
- **Contracts**: Token/NFT smart contracts
- **Targets**: DEXs/marketplaces with spending approval
- **Edges**: Authority grants (approvals)

### Why Visualize?

1. **Security**: Spot risky unlimited approvals
2. **Clarity**: Understand complex relationships
3. **Audit**: Track approval history
4. **Education**: Help users understand risks

### Real-World Example

**Scenario:** Alice wants to trade on Uniswap

1. Alice owns USDT tokens
2. Alice approves Uniswap to spend USDT
3. Graph shows: Alice → USDT → Uniswap

**Visualization reveals:**
- Amount approved (unlimited? specific?)
- When approval was granted (block number)
- Other approvals Alice has made
- Potential security risks

---

## 📚 Additional Resources

### Documentation
- [Main README](../README.md) - Project overview
- [Examples README](examples/README.md) - Detailed examples
- [Contributing Guide](../CONTRIBUTING.md) - How to contribute

### Tools Used
- [D3.js](https://d3js.org/) - Interactive visualizations
- [NetworkX](https://networkx.org/) - Graph algorithms
- [Matplotlib](https://matplotlib.org/) - Static plots

### Related Projects
- Authority Graph Builder (this project)
- Member A: Event Extractor
- Member B: Risk Analyzer

---

## 🤝 Contributing

Want to add more visualization styles? Ideas:
- 3D visualization with Three.js
- Real-time streaming updates
- Mermaid diagram export
- GraphViz DOT format
- Jupyter notebook widgets

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

---

## ❓ FAQ

**Q: Which visualization should I use?**
A: 
- Quick check → ASCII terminal
- Presentation → HTML/D3.js
- Report/paper → Python/NetworkX

**Q: Can I visualize large graphs (1000+ nodes)?**
A: Yes, but consider:
- HTML: May be slow, increase force distance
- Python: Increase figure size, use hierarchical layout
- ASCII: Filter to specific wallets first

**Q: How do I export the HTML visualization?**
A: Take a screenshot or use browser's "Print to PDF" feature

**Q: Can I customize the colors?**
A: Yes! Edit the `colorMap` in each visualization file

**Q: Does this work with real blockchain data?**
A: Yes! Just pass your events to `buildAuthorityGraph()` first

---

## 📞 Support

- Issues: [GitHub Issues](https://github.com/KeerthanaTV06/Liqufi-Hackathon/issues)
- Discussions: [GitHub Discussions](https://github.com/KeerthanaTV06/Liqufi-Hackathon/discussions)

---

**Happy Visualizing! 🎨📊🔐**
