import sys
import os

from app.database.connection import PostgreDatabase
from app.database.models import Base
from app.data_sources.coingecko import CoingeckoSource
import pandas as pd

print("Dropping old tables...")
db = PostgreDatabase()
Base.metadata.drop_all(db.engine)
print("✓ Tables dropped")

print("\nCreating new tables...")
Base.metadata.create_all(db.engine)
print("✓ Tables created with new schema")

# Verify
from sqlalchemy import inspect
inspector = inspect(db.engine)

print("\nVerifying 'asset_prices' columns:")
for column in inspector.get_columns('asset_prices'):
    print(f"  {column['name']}: {column['type']}")

cg = CoingeckoSource()
df = cg.fetch_historical_prices('bitcoin', days=7)

print("Raw data from CoinGecko:")
print(df[['date']].head())
print(f"\nData type: {df['date'].dtype}")
print(f"\nSample value: {df['date'].iloc[0]}")
