# Naija-MarketSense

🍅 Naija MarketSense: AI-Powered Price Oracle & Arbitrage Engine

Naija MarketSense is a voice-first, multimodal AI agent designed to bridge the information gap in Nigeria's informal food markets. It empowers traders and farmers with real-time price intelligence, arbitrage opportunities, and logistics planning, accessible via natural language (Pidgin English).

🚀 Key Features

1. Voice-First Interface (Accessibility)

Problem: Many market traders prefer voice notes over typing.

Solution: The app accepts audio input (via st.audio_input), transcribes it using Gemini 2.5 Flash, and extracts intent (Commodity + Market) even from thick Pidgin accents.

Audio Response: The AI generates a spoken response (TTS) in a localized accent, advising the user on whether to buy or sell.

2. Arbitrage Engine (Business Intelligence)

Problem: Price disparities between markets (e.g., Mile 12 vs. Wuse) are opaque.

Solution: The backend MarketOracle scans 6 major Nigerian markets simultaneously. It calculates the Spread (Profit Margin) and visualizes the price differences on a color-coded heatmap, instantly spotting buy/sell opportunities.

3. "Wise Trader" Persona (Context)

Problem: Raw data is boring.

Solution: The AI persona is prompted to act as a "Wise Market Trader," delivering advice like "Oga, make you carry go Wuse, gain plenty there!" This cultural layer drives user engagement.

🛠️ Technical Architecture

Tech Stack

Frontend: Streamlit (Python)

AI Core: Google Gemini 2.5 Flash (Multimodal capabilities)

Voice Synthesis: gTTS (Google Text-to-Speech)

Data Visualization: Plotly Express

Deployment: Streamlit Community Cloud

Agent Workflow

Input: User speaks or types: "How much for rice for Bodija?"

Perception Agent: Transcribes audio and extracts entities ({"commodity": "Rice", "market": "Bodija"}).

Market Oracle: Queries the mock database for the requested item and performs a Full Market Scan for arbitrage.

Reasoning Agent: Compares prices, calculates potential profit, and drafts a Pidgin response.

Output: Displays a price chart and plays the TTS audio file.

💻 Installation & Local Setup

Prerequisites

Python 3.10+

A Google Gemini API Key

Step 1: Clone Repository

git clone [https://github.com/Fharuk/Naija-MarketSense.git](https://github.com/Fharuk/Naija-MarketSense.git)
cd Naija-MarketSense


Step 2: Install Dependencies

pip install -r requirements.txt


Step 3: Configure Credentials

Create a .env file or export your key:

export GEMINI_API_KEY="your_api_key_here"


Step 4: Run Application

streamlit run app.py


🔮 Future Roadmap

WhatsApp Integration: Deploy the agent as a WhatsApp bot (using Twilio API) to reach users where they are.

Real Logistics: Integrate Google Maps API to calculate actual transport costs based on traffic.

User Accounts: Allow traders to save their "Watchlist" items.

Built with ❤️ for Nigerian SMEs.