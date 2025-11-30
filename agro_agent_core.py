import google.generativeai as genai
import json
import logging
import os
import tempfile
from gtts import gTTS
from market_data import MarketOracle

logger = logging.getLogger(__name__)

class AgroAgent:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API Key required")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash-preview-09-2025')
        self.oracle = MarketOracle()

    def _generate_audio_response(self, text: str) -> str:
        """Converts text to audio using gTTS and returns file path."""
        try:
            # Generate speech (English/Pidgin approximation)
            tts = gTTS(text=text, lang='en', tld='com.ng') # Attempting Nigerian accent bias
            
            # Save to temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                tts.save(tmp.name)
                return tmp.name
        except Exception as e:
            logger.error(f"TTS Error: {e}")
            return None

    def process_query(self, user_text_input=None, audio_file=None):
        """
        Executes the full pipeline: Audio/Text -> Intent -> Arbitrage Data -> Insight -> TTS.
        """
        
        # 1. Intent Extraction
        prompt = """
        You are a Nigerian Market Assistant. Extract the 'Commodity' from the user's input.
        Input might be in Pidgin English.
        Known Commodities: Tomato, Rice, Yam, Garri, Palm Oil.
        
        Output JSON: {"commodity": "string", "original_intent": "string"}
        """
        
        try:
            if audio_file:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                    tmp.write(audio_file.getvalue())
                    tmp_path = tmp.name
                
                uploaded_file = genai.upload_file(tmp_path, mime_type="audio/wav")
                response = self.model.generate_content([prompt, uploaded_file])
                os.remove(tmp_path)
            else:
                response = self.model.generate_content([prompt, user_text_input])

            intent = json.loads(response.text.strip('`json').strip('`'))
        except Exception as e:
            return {"error": f"I no understand wetin you talk. Try again. Error: {e}"}

        commodity = intent.get("commodity")
        if not commodity:
            return {"error": "Abeg, which market item you dey find? I know Tomato, Rice, Yam..."}

        # 2. Arbitrage Scan (The "Excellent" Feature)
        arbitrage_data = self.oracle.get_arbitrage_scan(commodity)
        if not arbitrage_data:
            return {"error": f"Data no dey for {commodity}."}

        # 3. Insight Generation (The "Wise Trader")
        cheapest = arbitrage_data['cheapest']
        expensive = arbitrage_data['most_expensive']
        spread = arbitrage_data['spread']
        
        analysis_prompt = f"""
        Act as a smart Nigerian Market Trader giving business advice.
        User asked about: {commodity}
        
        Market Data:
        - Cheapest: {cheapest['market']} at N{cheapest['price']:,}
        - Most Expensive: {expensive['market']} at N{expensive['price']:,}
        - Profit Spread: N{spread:,}
        
        Task:
        1. Summarize the best place to buy.
        2. Give advice in Nigerian Pidgin English. Focus on the PROFIT opportunity.
        (e.g., "Oga! If you buy for {cheapest['market']} carry go {expensive['market']}, you go make serious gain!")
        Keep it short (under 30 words) for audio.
        """
        
        analysis_response = self.model.generate_content(analysis_prompt)
        advice_text = analysis_response.text

        # 4. Generate Audio Response (The "Loveable" Feature)
        audio_path = self._generate_audio_response(advice_text)

        return {
            "intent": intent,
            "data": arbitrage_data,
            "advice": advice_text,
            "audio_path": audio_path
        }