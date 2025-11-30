import google.generativeai as genai
import json
import logging
import os
import tempfile
from market_data import MarketOracle

logger = logging.getLogger(__name__)

class AgroAgent:
    def __init__(self, api_key):
        if not api_key:
            raise ValueError("API Key required")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash-preview-09-2025')
        self.oracle = MarketOracle()

    def process_query(self, user_text_input=None, audio_file=None):
        """
        Main pipeline: 
        1. Understand Query (Text or Audio)
        2. Fetch Data (Tools)
        3. Generate Insight (Reasoning)
        """
        
        # Step 1: Intent Extraction
        prompt = """
        You are a Nigerian Market Assistant. Extract the 'Commodity' and 'Market' from the user's input.
        Input might be in Pidgin English.
        
        Known Markets: Mile 12, Bodija, Wuse, Ogbete, Alaba Rago.
        Known Commodities: Tomato, Rice, Yam, Garri, Palm Oil.
        
        Output JSON: {"commodity": "string", "market": "string", "original_intent": "string"}
        """
        
        try:
            if audio_file:
                # 1. Save audio bytes to a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                    tmp.write(audio_file.getvalue())
                    tmp_path = tmp.name

                # 2. Upload to Gemini File API
                uploaded_file = genai.upload_file(tmp_path, mime_type="audio/wav")
                
                # 3. Multimodal Generation
                response = self.model.generate_content([prompt, uploaded_file])
                
                # Clean up temp file
                os.remove(tmp_path)
            else:
                # Text-only Generation
                response = self.model.generate_content([prompt, user_text_input])

            intent = json.loads(response.text.strip('`json').strip('`'))
        except Exception as e:
            return {"error": f"Could not understand request: {e}"}

        # Step 2: Data Retrieval (Tool Use)
        market = intent.get("market")
        commodity = intent.get("commodity")
        
        if not market or not commodity:
            return {"error": "I no hear the market or commodity name well. Abeg talk am again."}

        price_data = self.oracle.get_market_price(market, commodity)
        if not price_data:
            return {"error": f"Sorry, I no get price for {commodity} inside {market}."}

        # Step 3: Logistics (Mocked for now)
        transport_cost = 5000 

        # Step 4: Insight Generation (The "Oracle")
        analysis_prompt = f"""
        Act as a wise Nigerian Market Trader. 
        User asked: "{intent.get('original_intent', 'Price Check')}"
        
        Data:
        - Price: N{price_data['price']:,} per {price_data['unit']}
        - Market: {market}
        - Transport Avg: N{transport_cost:,}
        
        Task:
        1. Give the price clearly.
        2. Give advice in Nigerian Pidgin English. 
        (e.g., "Omo, price don go up o! Make you buy now before e climb again.")
        """
        
        analysis_response = self.model.generate_content(analysis_prompt)
        
        return {
            "intent": intent,
            "data": price_data,
            "transport": transport_cost,
            "advice": analysis_response.text
        }