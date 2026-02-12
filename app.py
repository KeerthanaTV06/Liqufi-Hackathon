import streamlit as st

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
        # Mock data (replace with Member B later)
        verdict_data = {
            "wallet": wallet,
            "verdict": "TRUST BROKEN",
            "block": 18392012,
            "reason": "Unlimited approval granted"
        }

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

        st.info(
            "This verdict indicates whether the wallet has crossed an irreversible trust boundary."
        )


