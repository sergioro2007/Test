import sys
import os
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from portfolio_suite.options_trading.core import OptionsTracker

class TestDynamicWatchlist(unittest.TestCase):
    """Test the dynamic watchlist generation functionality"""

    def setUp(self):
        """Set up the test environment"""
        self.tracker = OptionsTracker()

    def test_watchlist_generation(self):
        """Test that the watchlist is properly generated"""
        # Check if watchlist was generated
        self.assertGreater(len(self.tracker.watchlist), 0, "Watchlist should contain tickers")
    
    def test_watchlist_parameter_structure(self):
        """Test that all tickers have the required parameters"""
        # Verify all expected parameters exist
        for ticker, data in self.tracker.watchlist.items():
            for param in ['current_price', 'range_low', 'range_high', 'target_price', 'bullish_probability']:
                self.assertIn(param, data, f"Ticker {ticker} is missing parameter '{param}'")

    def test_watchlist_parameter_values(self):
        """Test that parameter values are within expected ranges"""
        # Check a sample of tickers (up to 10)
        sample_tickers = list(self.tracker.watchlist.items())[:10]
        
        for ticker, data in sample_tickers:
            # Check price is positive
            self.assertGreater(
                data['current_price'], 
                0, 
                f"Ticker {ticker} has invalid price: {data['current_price']}"
            )
            
            # Check range makes sense (low < high)
            low = data['range_low']
            high = data['range_high']
            self.assertLess(
                low, 
                high, 
                f"Ticker {ticker} has invalid range: low={low}, high={high}"
            )
            
            # Check bias probability is between 0 and 1
            self.assertGreaterEqual(
                data['bullish_probability'], 
                0, 
                f"Ticker {ticker} has bias probability < 0: {data['bullish_probability']}"
            )
            self.assertLessEqual(
                data['bullish_probability'], 
                1, 
                f"Ticker {ticker} has bias probability > 1: {data['bullish_probability']}"
            )
    
    def test_watchlist_diversity(self):
        """Test that the watchlist includes a diverse set of tickers"""
        # Ensure we have a reasonable number of tickers
        self.assertGreaterEqual(
            len(self.tracker.watchlist), 
            10, 
            "Watchlist should include at least 10 tickers"
        )

if __name__ == "__main__":
    unittest.main()
