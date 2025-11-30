import pandas as pd
import random
import datetime

# Realistic Mock Data for Nigerian Markets
MARKET_DB = {
    "Mile 12": {"lat": 6.6018, "lon": 3.3515, "state": "Lagos"},
    "Bodija": {"lat": 7.4351, "lon": 3.9143, "state": "Oyo"},
    "Wuse": {"lat": 9.0526, "lon": 7.4778, "state": "Abuja"},
    "Ogbete": {"lat": 6.4381, "lon": 7.4943, "state": "Enugu"},
    "Alaba Rago": {"lat": 6.4622, "lon": 3.1910, "state": "Lagos"}
}

COMMODITIES = {
    "Tomato": {"unit": "Basket (Big)", "base_price": 45000, "volatility": 0.2},
    "Rice": {"unit": "Bag (50kg)", "base_price": 75000, "volatility": 0.05},
    "Yam": {"unit": "Tuber (Large)", "base_price": 3500, "volatility": 0.15},
    "Garri": {"unit": "Paint Bucket", "base_price": 2500, "volatility": 0.1},
    "Palm Oil": {"unit": "25L Keg", "base_price": 30000, "volatility": 0.08}
}

class MarketOracle:
    """
    Simulates a real-time market price API.
    """
    def get_market_price(self, market_name, commodity):
        """Returns current price with simulated daily fluctuation."""
        if market_name not in MARKET_DB:
            return None
        if commodity not in COMMODITIES:
            return None
        
        base = COMMODITIES[commodity]["base_price"]
        volatility = COMMODITIES[commodity]["volatility"]
        
        # Simulate price fluctuation based on "market noise"
        fluctuation = random.uniform(1 - volatility, 1 + volatility)
        current_price = int(base * fluctuation)
        
        return {
            "market": market_name,
            "commodity": commodity,
            "unit": COMMODITIES[commodity]["unit"],
            "price": current_price,
            "timestamp": datetime.datetime.now().isoformat()
        }

    def calculate_logistics(self, user_location, market_name):
        """
        Mock logistics calculation. 
        In a real app, this would use Google Maps API for distance matrix.
        Here, we mock it based on 'state' logic for simplicity.
        """
        market_state = MARKET_DB.get(market_name, {}).get("state", "Unknown")
        
        # Simple heuristic: Within state = N5,000, Out of state = N25,000
        # This is a placeholder for the logic agent.
        base_transport = 5000
        return base_transport