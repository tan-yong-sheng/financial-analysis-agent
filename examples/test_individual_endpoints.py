"""
Test script for individual API endpoints.
This script allows testing specific API endpoints to diagnose connection issues.
"""

import sys
import os
import json
import requests
import logging
from typing import Dict, Any

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,  # Using DEBUG level to see detailed request information
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import config
try:
    from config import FMP_API_KEY, FMP_BASE_URL
except ImportError:
    logger.error("Could not import config. Please ensure config.py exists with FMP_API_KEY and FMP_BASE_URL defined.")
    sys.exit(1)


def test_endpoint(endpoint_path: str, params: Dict[str, Any] = None) -> None:
    """Test a specific API endpoint."""
    if params is None:
        params = {}
        
    # Add API key to parameters
    params['apikey'] = FMP_API_KEY
    
    # Construct full URL
    full_url = f"{FMP_BASE_URL}/{endpoint_path}"
    
    logger.info(f"Testing endpoint: {full_url}")
    logger.info(f"Parameters: {params}")
    
    try:
        response = requests.get(full_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        logger.info(f"Response status code: {response.status_code}")
        
        # Print a sample of the response
        if isinstance(data, list):
            sample = data[:1] if data else []
            logger.info(f"Response sample (first item of {len(data)}): {json.dumps(sample, indent=2)}")
        else:
            sample = {k: data[k] for k in list(data.keys())[:5]} if data else {}
            logger.info(f"Response sample (first 5 keys): {json.dumps(sample, indent=2)}")
            
        return True, data
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {str(e)}")
        return False, {"error": str(e)}
    except json.JSONDecodeError:
        logger.error("Failed to parse JSON response")
        return False, {"error": "Invalid JSON response"}


def test_technical_indicator_endpoints(ticker: str) -> None:
    """Test various technical indicator endpoints."""
    indicators = ["rsi", "macd", "sma", "ema"]
    
    logger.info("Testing technical indicator endpoints")
    
    for indicator in indicators:
        # Test with 1day period
        endpoint = f"technical_indicator/{ticker}"
        params = {
            "period": "1day",
            "type": indicator,
            "timePeriod": 14
        }
        
        success, _ = test_endpoint(endpoint, params)
        if not success:
            logger.warning(f"Failed to fetch {indicator} data for {ticker}")


def main() -> None:
    """Main function to test individual endpoints."""
    ticker = "AAPL"  # Default ticker
    
    # Allow command line argument for ticker
    if len(sys.argv) > 1:
        ticker = sys.argv[1]
    
    logger.info(f"Testing API endpoints with ticker: {ticker}")
    
    # Test company profile endpoint
    test_endpoint(f"profile/{ticker}")
    
    # Test financial statement endpoints
    test_endpoint(f"income-statement/{ticker}", {"period": "annual", "limit": 5})
    test_endpoint(f"balance-sheet-statement/{ticker}", {"period": "annual", "limit": 5})
    test_endpoint(f"cash-flow-statement/{ticker}", {"period": "annual", "limit": 5})
    
    # Test technical indicator endpoints
    test_technical_indicator_endpoints(ticker)
    
    # Test stock price endpoint
    test_endpoint(f"historical-price-full/{ticker}")


if __name__ == "__main__":
    main()
