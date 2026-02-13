import streamlit as st
import json
import subprocess
import sys
import os

# --- Path setup ---
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
VERDICT_PATH = os.path.join(
    PROJECT_ROOT, "backend", "data", "irreversibility_verdict.json"
)

st.set_page_config(
    page_title="PointZero",
    layout="centered"
)

# Header
st.markdown(
    "<h1 style='text-align: center;'>🔐 PointZero</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center; color: gray;'>Deterministic Wallet Trust Analyzer</p>",
    unsafe_allow_html=True
)

st.divider()

# Input section
wallet = st.text_input(
    "Wallet Address",
    placeholder="0xABC...123"
)

analyze = st.button("🔍 Analyze Wallet", use_container_width=True)

st.divider()

if analyze:
    if wallet == "":
        st.warning("⚠️ Please enter a wallet address")
    else:
        # --- Run backend analysis ---
        with st.spinner("🔄 Running irreversibility analysis..."):
            try:
                result = subprocess.run(
                    [
                        sys.executable,
                        os.path.join(PROJECT_ROOT, "backend", "analyze_wallet.py"),
                        wallet,
                    ],
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    timeout=30,
                    cwd=PROJECT_ROOT,
                )

                if result.returncode != 0:
                    st.error(
                        f"❌ Backend error (exit code {result.returncode}):\n"
                        f"{result.stderr.strip()}"
                    )
                    st.stop()

            except subprocess.TimeoutExpired:
                st.error("❌ Analysis timed out (30s limit).")
                st.stop()
            except FileNotFoundError:
                st.error("❌ Backend not found. Ensure backend/ directory exists.")
                st.stop()

        # --- Read verdict JSON ---
        try:
            with open(VERDICT_PATH, "r", encoding="utf-8") as f:
                verdict_data = json.load(f)
        except FileNotFoundError:
            st.error("❌ Verdict file not found. Backend may not have run correctly.")
            st.stop()
        except json.JSONDecodeError:
            st.error("❌ Verdict file is corrupted. Please re-run analysis.")
            st.stop()

        # --- Display results (original rendering logic preserved) ---
        st.markdown("### 🧾 Analysis Result")

        st.markdown(
            f"""
            **Wallet:**  
            `{verdict_data['wallet']}`
            """
        )

        if verdict_data["verdict"] == "TRUST BROKEN":
            st.error("❌ **TRUST BROKEN**")
        else:
            st.success("✅ **TRUST SAFE**")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Cause**")
            st.write(verdict_data["reason"])

        with col2:
            st.markdown("**Block Number**")
            st.write(verdict_data["block"])

        # --- Extended details (new) ---
        if "details" in verdict_data:
            details = verdict_data["details"]

            with st.expander("📊 Extended Analysis Details"):
                st.write(f"**Events Analyzed:** {details.get('events_analyzed', 'N/A')}")
                st.write(f"**Total Breaches:** {details.get('total_breaches', 0)}")

                if details.get("triggered_rules"):
                    st.markdown("**Triggered Rules:**")
                    for rule in details["triggered_rules"]:
                        severity_icon = {
                            "FATAL": "💀", "CRITICAL": "🔴",
                            "HIGH": "🟠", "MEDIUM": "🟡"
                        }.get(rule["severity"], "⚪")
                        st.write(
                            f"{severity_icon} **[{rule['severity']}]** "
                            f"{rule['rule_name']} — block {rule['block']}"
                        )
                        st.caption(rule.get("description", ""))

        st.info(
            "This verdict indicates whether the wallet has crossed an irreversible trust boundary."
        )
