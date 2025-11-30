import streamlit as st
import os
import pandas as pd
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="Naija MarketSense", layout="wide")

from agro_agent_core import AgroAgent

# Secure Init
def get_api_key():
    if "GEMINI_API_KEY" in st.secrets:
        return st.secrets["GEMINI_API_KEY"]
    return os.environ.get("GEMINI_API_KEY")

api_key = get_api_key()

if 'history' not in st.session_state:
    st.session_state.history = []

# --- UI HEADER ---
st.title("🍅 Naija MarketSense")
st.markdown("**AI-Powered Arbitrage Engine & Price Oracle**")

if not api_key:
    st.error("System Offline. Configure GEMINI_API_KEY.")
    st.stop()

try:
    agent = AgroAgent(api_key)
except Exception as e:
    st.error(f"Failed to initialize AI: {e}")
    st.stop()

# --- INPUT SECTION ---
st.subheader("Market Scanner")
tab_text, tab_voice = st.tabs(["📝 Text Query", "🎤 Voice Command"])

def handle_result(result):
    if "error" in result:
        st.error(result["error"])
    else:
        st.session_state.history.insert(0, result)
        st.rerun() # Force reload to show results at top

with tab_text:
    user_input = st.text_input("Enter Commodity (e.g., 'Tomato', 'Rice')")
    if st.button("Scan Markets", key="text_scan"):
        if user_input:
            with st.spinner("Analyzing market prices nationwide..."):
                result = agent.process_query(user_text_input=user_input)
                handle_result(result)

with tab_voice:
    audio_value = st.audio_input("Ask MarketSense (Pidgin Supported)")
    if audio_value:
        with st.spinner("Processing voice command..."):
            result = agent.process_query(audio_file=audio_value)
            handle_result(result)

# --- RESULTS DISPLAY ---
if st.session_state.history:
    latest = st.session_state.history[0]
    data = latest['data']
    
    # 1. Audio & Advice
    st.markdown("---")
    col_audio, col_text = st.columns([1, 2])
    
    with col_audio:
        st.info("🔊 **Listen to Advice**")
        if latest.get('audio_path'):
            st.audio(latest['audio_path'], format="audio/mp3", autoplay=True)
    
    with col_text:
        st.success(f"🗣️ **Oracle:** {latest['advice']}")

    # 2. Arbitrage Metrics
    st.subheader(f"Arbitrage Analysis: {data['commodity']}")
    m1, m2, m3 = st.columns(3)
    m1.metric("Lowest Price", f"₦{data['cheapest']['price']:,}", data['cheapest']['market'])
    m2.metric("Highest Price", f"₦{data['most_expensive']['price']:,}", data['most_expensive']['market'])
    m3.metric("Potential Spread", f"₦{data['spread']:,}", "Gross Profit/Unit")

    # 3. Market Comparison Chart
    all_prices_df = pd.DataFrame(data['all_prices'])
    
    # Color logic: Green for cheap, Red for expensive
    fig = px.bar(
        all_prices_df, 
        x='market', 
        y='price', 
        color='price',
        title=f"Price Comparison ({data['unit']})",
        color_continuous_scale='RdYlGn_r', # Red (High) to Green (Low) reversed
        text_auto='.2s'
    )
    fig.update_layout(yaxis_tickformat="₦")
    st.plotly_chart(fig, use_container_width=True)

    # History List
    st.markdown("---")
    with st.expander("Previous Scans"):
        for item in st.session_state.history[1:]:
            st.caption(f"{item['data']['commodity']}: {item['advice']}")