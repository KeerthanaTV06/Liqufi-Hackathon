import sys
import io
import os

# Force UTF-8 encoding for stdout and stderr to prevent Windows console issues with emojis
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

"""
PointZero Wallet Analyzer — CLI Entry Point
=============================================
Orchestrates the full dynamic analysis pipeline:
1. Validate Wallet
2. Fetch Events (LiquifyClient)
3. Build Graph (GraphBuilder)
4. Analyze Graph (IrreversibilityEngine)
5. Generate Verdict

Usage:
    python backend/analyze_wallet.py <wallet_address>
"""

# Ensure the project root is on the path so imports resolve correctly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.irreversibility_engine import IrreversibilityEngine
from backend.generate_verdict import write_verdict
from backend.liquify_client import LiquifyClient
from backend.graph_builder import GraphBuilder, save_graph_to_file
from backend.security import validate_wallet_address

def main():
    """Run the full PointZero dynamic analysis pipeline."""

    # --- Parse CLI argument ---
    if len(sys.argv) < 2:
        print("Usage: python backend/analyze_wallet.py <wallet_address>")
        sys.exit(1)

    raw_wallet = sys.argv[1]

    try:
        print(f"🔍 PointZero — Starting Dynamic Analysis for: {raw_wallet}")
        print("=" * 60)

        # 1. Validate Wallet
        wallet_address = validate_wallet_address(raw_wallet)
        print(f"✅ Wallet validated: {wallet_address}")

        # 2. Fetch Events (LiquifyClient)
        print("⏳ Fetching authority events form Liquify (Mock)...")
        client = LiquifyClient()
        events = client.fetch_authority_events(wallet_address)
        print(f"✅ Fetched {len(events)} raw events.")

        # 3. Build Graph (GraphBuilder)
        print("⚙️ Building Authority Graph...")
        builder = GraphBuilder()
        graph = builder.build_authority_graph(wallet_address, events)
        
        # Save graph for frontend reference / debugging
        graph_path = save_graph_to_file(graph)
        print(f"💾 Authority Graph saved to: {graph_path}")

        # 4. Analyze Graph (IrreversibilityEngine)
        print("🧠 Running Irreversibility Engine...")
        engine = IrreversibilityEngine()
        # Note: We pass the in-memory graph directly
        verdict = engine.analyze_graph(wallet_address, graph)

        # 5. Write Verdict
        output_path = write_verdict(verdict)
        print(f"\n📄 Verdict written to: {output_path}")

        # --- Print Summary ---
        print(f"\n{'=' * 60}")
        print(f"  Wallet:   {verdict['wallet']}")
        print(f"  Verdict:  {verdict['verdict']}")
        print(f"  Block:    {verdict['block']}")
        print(f"  Reason:   {verdict['reason']}")

        if verdict.get("details"):
            details = verdict["details"]
            print(f"  Breaches: {details.get('total_breaches', 0)}")
            print(f"  Edges:    {details.get('edges_analyzed', 0)}")

            if details.get("triggered_rules"):
                print(f"\n  Triggered Rules:")
                for rule in details["triggered_rules"]:
                    print(f"    • [{rule['severity']}] {rule['rule_name']} "
                          f"(block {rule['block']})")

        print(f"{'=' * 60}")

        if verdict["verdict"] == "TRUST BROKEN":
            print("❌ TRUST BROKEN — Irreversible authority event detected.")
        else:
            print("✅ TRUST SAFE — No irreversible events found.")

        sys.exit(0)

    except ValueError as e:
        print(f"\n❌ Validation Error: {e}", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ Analysis Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(2)


if __name__ == "__main__":
    main()
