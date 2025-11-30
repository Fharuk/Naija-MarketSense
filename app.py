import streamlit as st
import os
from agro_agent_core import AgroAgent
import pandas as pd
import plotly.express as px

# Config
st.set_page_config(page_title="Naija MarketSense", layout="mobile")

# Secure Init
def get_api_key():
    if "GEMINI_API_KEY" in st.secrets:
        return st.secrets["GEMINI_API_KEY"]
    return os.environ.get("GEMINI_API_KEY")

api_key = get_api_key()

# Session State
if 'history' not in st.session_state:
    st.session_state.history = []

# --- UI ---
st.title("🍅 Naija MarketSense")
st.markdown("**Your Voice-First Market Price Oracle**")

if not api_key:
    st.error("System Offline. Configure GEMINI_API_KEY.")
    st.stop()

agent = AgroAgent(api_key)

# Input Section
st.subheader("Wetin you want check today?")

# Tabs for input method
tab_text, tab_voice = st.tabs(["📝 Text Search", "🎤 Voice Note (Beta)"])

with tab_text:
    user_input = st.text_input("Type here (e.g., 'How much for Tomato inside Mile 12?')")
    if st.button("Check Price"):
        if user_input:
            with st.spinner("Asking Market women..."):
                result = agent.process_query(user_text_input=user_input)
                
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.session_state.history.insert(0, result)

# Display Results
if st.session_state.history:
    latest = st.session_state.history[0]
    
    # 1. The Answer Card
    st.markdown("---")
    st.success("### Market Gist")
    
    # Display Advice (Pidgin)
    st.markdown(f"🗣️ **Oracle:** {latest['advice']}")
    
    # 2. Key Metrics
    col1, col2 = st.columns(2)
    col1.metric("Current Price", f"₦{latest['data']['price']:,}")
    col2.metric("Unit", latest['data']['unit'])
    
    # 3. Trend Chart (Simulated history for visualization)
    st.subheader("Price Movement (Last 7 Days)")
    # Generate mock history for the chart
    base = latest['data']['price']
    mock_trend = pd.DataFrame({
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Today"],
        "Price": [base*0.9, base*0.95, base*0.92, base*0.98, base*1.05, base*1.02, base]
    })
    
    fig = px.line(mock_trend, x="Day", y="Price", title=f"{latest['data']['commodity']} Trend in {latest['data']['market']}", markers=True)
    fig.update_layout(yaxis_tickformat="₦")
    st.plotly_chart(fig, use_container_width=True)

# History
st.markdown("---")
with st.expander("Recent Checks"):
    for item in st.session_state.history[1:]:
        st.write(f"**{item['data']['commodity']} @ {item['data']['market']}**: ₦{item['data']['price']:,}")