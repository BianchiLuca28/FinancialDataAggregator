from fastapi import FastAPI
from ..database.connection import PostgreDatabase
from ..database.models import Asset, AssetPrice
from ..analytics.metrics import calculate_daily_returns
import pandas as pd

app = FastAPI(title="Financial Data Aggregator API")

db = PostgreDatabase()

@app.get("/")
def root():
    """API health check."""
    return {"status": "ok", "message": "Financial Data Aggregator API"}

@app.get("/assets")
def get_assets():
    """Get all tracked assets."""
    session = db.get_session()
    assets = session.query(Asset).all()
    session.close()

    return [
        {"symbol": a.symbol, "name": a.name, "type": a.asset_type}
        for a in assets
    ]

@app.get("/assets/{symbol}/prices")
def get_prices(symbol: str, limit: int = 30):
    """Get price history for an asset."""
    session = db.get_session()

    asset = session.query(Asset).filter_by(symbol=symbol).first()
    if not asset:
        session.close()
        return {"error": "Asset not found"}

    prices = session.query(AssetPrice).filter_by(asset_id=asset.id) \
        .order_by(AssetPrice.date.desc()).limit(limit).all()

    session.close()

    return [
        {
            "date": str(p.date),
            "price": float(p.price),
            "volume": float(p.volume) if p.volume else None
        }
        for p in prices
    ]

@app.get("/assets/{symbol}/metrics")
def get_metrics(symbol: str):
    """Get calculated metrics for an asset."""
    session = db.get_session()

    asset = session.query(Asset).filter_by(symbol=symbol).first()
    if not asset:
        session.close()
        return {"error": "Asset not found"}

    # Get last 90 days
    prices = session.query(AssetPrice).filter_by(asset_id=asset.id) \
        .order_by(AssetPrice.date).limit(90).all()

    session.close()

    # Convert to DataFrame
    data = [{
        'symbol': symbol,
        'date': p.date,
        'price': float(p.price),
        'volume': float(p.volume) if p.volume else None
    } for p in prices]

    df = pd.DataFrame(data)

    # Calculate metrics
    df_metrics = calculate_daily_returns(df)

    # Return latest metrics
    latest = df_metrics.iloc[-1]

    return {
        "symbol": symbol,
        "current_price": float(latest['price']),
        "daily_return": float(latest['daily_return']) if pd.notna(latest['daily_return']) else None,
        "ma_7d": float(latest['ma_7d']) if pd.notna(latest['ma_7d']) else None,
        "ma_30d": float(latest['ma_30d']) if pd.notna(latest['ma_30d']) else None,
        "volatility_30d": float(latest['volatility_30d']) if pd.notna(latest['volatility_30d']) else None
    }
