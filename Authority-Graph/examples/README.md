# Authority Graph Visualization Examples

This directory contains various visualization examples for the Authority Graph Builder.

## Available Visualizations

### 1. Interactive Web Visualization (HTML + D3.js)
**File:** `visualize-graph.html`

A beautiful, interactive web-based visualization using D3.js force-directed graph.

**Features:**
- Drag and drop nodes
- Hover tooltips with detailed information
- Color-coded node types (Wallets, Tokens, NFTs, Targets)
- Animated force simulation
- Responsive design

**How to use:**
```bash
# Simply open in your browser
open visualize-graph.html
# or
start visualize-graph.html  # Windows
```

**Screenshot:**
- Green nodes: Wallets
- Blue nodes: Token contracts
- Orange nodes: NFT contracts
- Red nodes: Target entities (DEX/Marketplace)
- Gray arrows: Ownership relationships
- Red arrows: Approval relationships

---

### 2. Python Visualization (NetworkX + Matplotlib)
**File:** `visualize_graph.py`

Creates high-quality static graph images using NetworkX and Matplotlib.

**Requirements:**
```bash
pip install networkx matplotlib
```

**How to use:**
```bash
python visualize_graph.py
```

**Output:**
- Generates `authority_graph.png` with 300 DPI resolution
- Professional layout with legend
- Color-coded nodes and edges
- Edge labels showing approval types and amounts

---

### 3. ASCII Terminal Visualization (Node.js)
**File:** `visualize-graph-ascii.js`

Beautiful text-based visualizations that work in any terminal.

**Features:**
- Three different visualization styles:
  1. **ASCII View**: Detailed box-style layout
  2. **Tree View**: Hierarchical tree structure with statistics
  3. **Matrix View**: Relationship matrix format
- Unicode box-drawing characters
- Emoji icons for visual clarity
- No external dependencies

**How to use:**
```bash
node visualize-graph-ascii.js
```

**Example Output:**
```
┌────────────────────────────────────────────────────────┐
│ 👤 WALLET: 0xAlice                                     │
└────────────────────────────────────────────────────────┘
  ├──💰 CONTRACT: 0xUSDT
  │     │
  │     ├─ Type: token_approval
  │     ├─ Amount: unlimited
  │     └──▶ 🔄 TARGET: 0xUniswap
```

---

### 4. Basic Usage Examples

**JavaScript:** `example-usage.js`
```bash
node example-usage.js
```

**Python:** `example_usage.py`
```bash
python example_usage.py
```

These demonstrate the core functionality with various input scenarios.

---

## Visualization Comparison

| Feature | HTML/D3.js | Python/NetworkX | ASCII Terminal |
|---------|------------|-----------------|----------------|
| Interactive | ✅ Yes | ❌ No | ❌ No |
| High Quality | ✅ Yes | ✅ Yes | ⚠️ Text-based |
| Dependencies | Browser only | networkx, matplotlib | None |
| Export | Screenshot | PNG/PDF | Copy text |
| Best For | Presentations | Reports/Papers | Quick checks |

---

## Understanding the Graph Structure

### Node Types
- **Wallet (Green/👤)**: User wallet addresses that own tokens/NFTs
- **Token Contract (Blue/💰)**: ERC-20 token contracts
- **NFT Contract (Orange/🎨)**: ERC-721/1155 NFT contracts
- **Target Entity (Red/🔄🏪)**: DEX or marketplace that receives approval

### Edge Types
- **Ownership (Gray)**: Wallet → Contract (implicit ownership)
- **Approval (Red)**: Contract → Target (explicit authority grant)

### Example Flow
```
Wallet (0xAlice)
    │
    ├─ owns → Token (USDT)
    │           │
    │           └─ approves → DEX (Uniswap) [unlimited]
    │
    └─ owns → NFT (BAYC)
                │
                └─ approves → Marketplace (OpenSea) [all]
```

---

## Customization

### Modify Sample Data

Edit the `sample_events` array in any example file:

```javascript
const sample_events = [
    {
        wallet: "0xYourWallet",
        contract: "0xYourContract",
        authority_type: "token_approval",
        target_entity: "0xYourTarget",
        amount: "unlimited",
        block: 18392000,
        timestamp: 1712345600
    }
];
```

### Change Colors (HTML)

Edit the `colorMap` in `visualize-graph.html`:

```javascript
const colorMap = {
    wallet: '#4CAF50',   // Green
    token: '#2196F3',    // Blue
    nft: '#FF9800',      // Orange
    target: '#F44336'    // Red
};
```

### Adjust Layout (Python)

Modify the layout algorithm in `visualize_graph.py`:

```python
# Try different layouts
pos = nx.spring_layout(G, k=2, iterations=50)  # Current
pos = nx.circular_layout(G)                     # Circular
pos = nx.kamada_kawai_layout(G)                # Kamada-Kawai
```

---

## Tips for Large Graphs

1. **HTML/D3.js**: Increase force simulation distance
   ```javascript
   .force('link', d3.forceLink().distance(200))
   ```

2. **Python**: Increase figure size
   ```python
   fig, ax = plt.subplots(figsize=(20, 16))
   ```

3. **ASCII**: Filter to specific wallets
   ```javascript
   const filteredData = Object.fromEntries(
       Object.entries(authorityGraph).slice(0, 5)
   );
   ```

---

## Integration with Your Application

### JavaScript/Node.js
```javascript
const { buildAuthorityGraph } = require('../src/authority-graph-builder');
const { visualizeGraphASCII } = require('./visualize-graph-ascii');

const events = [...]; // Your events
const graph = buildAuthorityGraph(events);
visualizeGraphASCII(graph);
```

### Python
```python
from authority_graph_builder import build_authority_graph
from visualize_graph import visualize_authority_graph

events = [...]  # Your events
graph = build_authority_graph(events)
visualize_authority_graph(graph, 'output.png')
```

---

## Troubleshooting

**HTML not displaying?**
- Make sure you're opening it in a modern browser
- Check browser console for errors
- Ensure D3.js CDN is accessible

**Python visualization fails?**
- Install dependencies: `pip install networkx matplotlib`
- Check Python version (3.7+)
- Try updating matplotlib: `pip install --upgrade matplotlib`

**ASCII characters not displaying?**
- Use a terminal with Unicode support
- On Windows, use Windows Terminal or PowerShell
- Set terminal encoding to UTF-8

---

## Contributing

Feel free to add more visualization styles! Some ideas:
- Mermaid diagram generator
- GraphViz DOT format export
- 3D visualization with Three.js
- Real-time streaming visualization
- Jupyter notebook integration

---

## License

MIT - Same as the main project
