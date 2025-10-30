import sys
import os

from app.etl.pipeline import ETLPipeline

# Define coins to track
COINS = [
    {'id': 'bitcoin', 'symbol': 'BTC', 'name': 'Bitcoin'},
    {'id': 'ethereum', 'symbol': 'ETH', 'name': 'Ethereum'},
    # Add more if you want
]

if __name__ == "__main__":
    print("="*60)
    print("TESTING ETL PIPELINE")
    print("="*60)

    # Create pipeline instance
    pipeline = ETLPipeline()

    # Run with small dataset first (2 coins, 7 days)
    print("\nLoading historical data...")
    pipeline.run_historical_load(COINS[:2], days=7)

    print("\n✅ Pipeline completed!")
