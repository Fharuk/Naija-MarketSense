import pandas as pd
import random
import datetime
from typing import Dict, List, Optional

# Realistic Mock Data for Nigerian Markets
MARKET_DB = {
    "Mile 12": {"state": "Lagos", "region": "SW"},
    "Bodija": {"state": "Oyo", "region": "SW"},
    "Wuse": {"state": "Abuja", "region": "NC"},
    "Ogbete": {"state": "Enugu", "region": "SE"},
    "Alaba Rago": {"state": "Lagos", "region": "SW"},
    "Dawanau": {"state": "Kano", "region": "NW"}
}

COMMODITIES = {
    "Tomato": {"unit": "Basket (Big)", "base_price": 45000, "volatility": 0.25},
    "Rice": {"unit": "Bag (50kg)", "base_price": 75000, "volatility": 0.05},
    "Yam": {"unit": "Tuber (Large)", "base_price": 3500, "volatility": 0.15},
    "Garri": {"unit": "Paint Bucket", "base_price": 2500, "volatility": 0.1},
    "Palm Oil": {"unit": "25L Keg", "base_price": 30000, "volatility": 0.08}
}

class MarketOracle:
    """
    Simulates a real-time market price API with Arbitrage capabilities.
    """
    def _simulate_price(self, market_name: str, commodity: str) -> int:
        """Generates a realistic price based on base price and regional volatility."""
        base = COMMODITIES[commodity]["base_price"]
        volatility = COMMODITIES[commodity]["volatility"]
        
        # Simulate regional price differences
        # e.g., Tomatoes cheaper in North (Kano), expensive in Lagos
        region = MARKET_DB[market_name]["region"]
        regional_modifier = 1.0
        
        if commodity == "Tomato":
            if region == "NW": regional_modifier = 0.7  # Cheaper in North
            if region == "SW": regional_modifier = 1.2  # Expensive in Lagos
            
        fluctuation = random.uniform(1 - volatility, 1 + volatility)
        return int(base * fluctuation * regional_modifier)

    def get_market_price(self, market_name: str, commodity: str) -> Optional[Dict]:
        """Returns price for a specific market."""
        if market_name not in MARKET_DB or commodity not in COMMODITIES:
            return None
        
        current_price = self._simulate_price(market_name, commodity)
        
        return {
            "market": market_name,
            "commodity": commodity,
            "unit": COMMODITIES[commodity]["unit"],
            "price": current_price,
            "timestamp": datetime.datetime.now().isoformat()
        }

    def get_arbitrage_scan(self, commodity: str) -> Dict:
        """
        Scans ALL markets for a commodity to find buy/sell opportunities.
        Returns the full dataset sorted by price.
        """
        if commodity not in COMMODITIES:
            return {}

        scan_results = []
        for market in MARKET_DB:
            price = self._simulate_price(market, commodity)
            scan_results.append({
                "market": market,
                "price": price,
                "state": MARKET_DB[market]["state"]
            })
        
        # Sort by price ascending (Cheapest first)
        scan_results.sort(key=lambda x: x["price"])
        
        return {
            "commodity": commodity,
            "unit": COMMODITIES[commodity]["unit"],
            "cheapest": scan_results[0],
            "most_expensive": scan_results[-1],
            "all_prices": scan_results,
            "spread": scan_results[-1]["price"] - scan_results[0]["price"]
        }