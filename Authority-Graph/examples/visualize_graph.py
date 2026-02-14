"""
Authority Graph Visualization using NetworkX and Matplotlib

Generates a visual representation of authority relationships
"""

import sys
import os
import json

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from authority_graph_builder import build_authority_graph

try:
    import networkx as nx
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
except ImportError:
    print("⚠️  This example requires networkx and matplotlib")
    print("Install with: pip install networkx matplotlib")
    sys.exit(1)


def visualize_authority_graph(authority_data, output_file='authority_graph.png'):
    """
    Create a visual representation of the authority graph
    
    Args:
        authority_data: Authority graph data from build_authority_graph()
        output_file: Output filename for the visualization
    """
    
    # Create directed graph
    G = nx.DiGraph()
    
    # Color mapping for different node types
    node_colors = {
        'wallet': '#4CAF50',      # Green
        'token': '#2196F3',       # Blue
        'nft': '#FF9800',         # Orange
        'target': '#F44336'       # Red
    }
    
    # Track node types
    node_types = {}
    edge_labels = {}
    
    # Process each wallet
    for wallet_addr, wallet_data in authority_data.items():
        # Add wallet node
        G.add_node(wallet_addr, node_type='wallet')
        node_types[wallet_addr] = 'wallet'
        
        # Process each authority edge
        for edge in wallet_data['authority_edges']:
            contract = edge['contract']
            target = edge['target_entity']
            
            # Determine contract type
            contract_type = 'nft' if 'nft' in edge['type'] else 'token'
            
            # Add contract node
            if contract not in node_types:
                G.add_node(contract, node_type=contract_type)
                node_types[contract] = contract_type
            
            # Add target node
            if target not in node_types:
                G.add_node(target, node_type='target')
                node_types[target] = 'target'
            
            # Add edges
            G.add_edge(wallet_addr, contract, relationship='owns')
            G.add_edge(contract, target, relationship='approval')
            
            # Store edge label
            edge_labels[(contract, target)] = f"{edge['type']}\n{edge['amount']}"
    
    # Create figure
    fig, ax = plt.subplots(figsize=(16, 12))
    fig.patch.set_facecolor('white')
    
    # Use spring layout for better visualization
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
    
    # Draw nodes by type
    for node_type, color in node_colors.items():
        nodes = [node for node, ntype in node_types.items() if ntype == node_type]
        if nodes:
            node_size = 3000 if node_type == 'wallet' else 2500
            nx.draw_networkx_nodes(
                G, pos, nodelist=nodes,
                node_color=color,
                node_size=node_size,
                alpha=0.9,
                ax=ax
            )
    
    # Draw edges
    # Ownership edges (wallet -> contract)
    ownership_edges = [(u, v) for u, v, d in G.edges(data=True) if d['relationship'] == 'owns']
    nx.draw_networkx_edges(
        G, pos,
        edgelist=ownership_edges,
        edge_color='#999',
        width=2,
        alpha=0.6,
        arrows=True,
        arrowsize=20,
        arrowstyle='->',
        ax=ax
    )
    
    # Approval edges (contract -> target)
    approval_edges = [(u, v) for u, v, d in G.edges(data=True) if d['relationship'] == 'approval']
    nx.draw_networkx_edges(
        G, pos,
        edgelist=approval_edges,
        edge_color='#F44336',
        width=3,
        alpha=0.7,
        arrows=True,
        arrowsize=20,
        arrowstyle='->',
        ax=ax
    )
    
    # Draw labels
    labels = {node: node[:10] + '...' if len(node) > 10 else node for node in G.nodes()}
    nx.draw_networkx_labels(
        G, pos,
        labels,
        font_size=9,
        font_weight='bold',
        font_color='white',
        ax=ax
    )
    
    # Draw edge labels for approvals
    edge_label_pos = {k: v for k, v in edge_labels.items() if k in approval_edges}
    nx.draw_networkx_edge_labels(
        G, pos,
        edge_label_pos,
        font_size=7,
        font_color='#333',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8),
        ax=ax
    )
    
    # Add title
    plt.title('Authority Graph Visualization\nBlockchain Authority Relationships', 
              fontsize=18, fontweight='bold', pad=20)
    
    # Add legend
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=node_colors['wallet'], 
                   markersize=15, label='Wallet'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=node_colors['token'], 
                   markersize=15, label='Token Contract'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=node_colors['nft'], 
                   markersize=15, label='NFT Contract'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=node_colors['target'], 
                   markersize=15, label='Target Entity (DEX/Marketplace)'),
        plt.Line2D([0], [0], color='#999', linewidth=2, label='Ownership'),
        plt.Line2D([0], [0], color='#F44336', linewidth=3, label='Approval')
    ]
    
    ax.legend(handles=legend_elements, loc='upper left', fontsize=10, 
              framealpha=0.9, shadow=True)
    
    # Remove axes
    ax.axis('off')
    
    # Add info box
    info_text = f"Nodes: {G.number_of_nodes()} | Edges: {G.number_of_edges()}"
    plt.text(0.5, 0.02, info_text, transform=fig.transFigure, 
             ha='center', fontsize=10, bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
    
    plt.tight_layout()
    
    # Save figure
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Graph visualization saved to: {output_file}")
    
    # Show plot
    plt.show()


if __name__ == "__main__":
    # Sample data
    sample_events = [
        {
            "wallet": "0xAlice",
            "contract": "0xUSDT",
            "authority_type": "token_approval",
            "target_entity": "0xUniswap",
            "amount": "unlimited",
            "block": 18392000,
            "timestamp": 1712345600
        },
        {
            "wallet": "0xAlice",
            "contract": "0xUSDC",
            "authority_type": "token_approval",
            "target_entity": "0xUniswap",
            "amount": "1000000000000000000",
            "block": 18392005,
            "timestamp": 1712345650
        },
        {
            "wallet": "0xAlice",
            "contract": "0xBAYC_NFT",
            "authority_type": "nft_approval_all",
            "target_entity": "0xOpenSea",
            "amount": "unlimited",
            "block": 18392010,
            "timestamp": 1712345670
        },
        {
            "wallet": "0xBob",
            "contract": "0xUSDT",
            "authority_type": "token_approval",
            "target_entity": "0xSushiSwap",
            "amount": "unlimited",
            "block": 18392008,
            "timestamp": 1712345660
        },
        {
            "wallet": "0xBob",
            "contract": "0xDAI",
            "authority_type": "token_approval",
            "target_entity": "0xUniswap",
            "amount": "500000000000000000",
            "block": 18392012,
            "timestamp": 1712345680
        },
        {
            "wallet": "0xCharlie",
            "contract": "0xCryptoPunks",
            "authority_type": "nft_approval_all",
            "target_entity": "0xOpenSea",
            "amount": "unlimited",
            "block": 18392015,
            "timestamp": 1712345690
        }
    ]
    
    print("🔨 Building authority graph...")
    authority_graph = build_authority_graph(sample_events)
    
    print("\n📊 Authority Graph Data:")
    print(json.dumps(authority_graph, indent=2))
    
    print("\n🎨 Creating visualization...")
    visualize_authority_graph(authority_graph)
