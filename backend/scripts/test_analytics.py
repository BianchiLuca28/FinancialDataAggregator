import sys
import os

from app.database.connection import PostgreDatabase
from app.database.models import Asset, AssetPrice
from app.analytics.metrics import calculate_daily_returns
import pandas as pd

print("="*60)
print("TESTING PYSPARK ANALYTICS")
print("="*60)

# Fetch data from database
db = PostgreDatabase()
session = db.get_session()

print("\nFetching data from database...")
prices = session.query(AssetPrice).join(Asset).all()

# Convert to DataFrame
data = []
for price in prices:
    asset = session.query(Asset).filter_by(id=price.asset_id).first()
    data.append({
        'symbol': asset.symbol,
        'date': price.date,
        'price': float(price.price),
        'volume': float(price.volume) if price.volume else None
    })

df = pd.DataFrame(data)
print(f"Loaded {len(df)} price records")

# Calculate metrics
print("\nCalculating metrics with PySpark...")
df_metrics = calculate_daily_returns(df)

print("\nResults:")
print(df_metrics[['symbol', 'date', 'price', 'daily_return', 'ma_7d']].tail(10))

print("\n✅ Analytics test complete!")
session.close()
