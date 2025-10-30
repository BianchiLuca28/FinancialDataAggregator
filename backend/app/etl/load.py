from sqlalchemy.dialects.postgresql import insert
from app.database.models import Asset, AssetPrice
import pandas as pd

def load_or_update_asset(session, symbol, name, asset_type, source):
    """
    Insert or update an asset in the database.

    Args:
        session: SQLAlchemy session
        symbol: Asset symbol (e.g., 'BTC')
        name: Asset name (e.g., 'Bitcoin')
        asset_type: Type of asset ('crypto', 'etf', 'stock')
        source: Source of the asset data

    Returns:
        Asset object
    """
    # Check if asset already exists
    asset = session.query(Asset).filter_by(symbol=symbol).first()

    if asset:
        # Update existing
        asset.name = name
        asset.asset_type = asset_type
        asset.source = source
    else:
        # Create new
        asset = Asset(
            symbol=symbol,
            name=name,
            asset_type=asset_type,
            source=source
        )
        session.add(asset)

    session.commit()
    return asset

def load_prices(session, df, asset_id):
    """
    Load price data into database with upsert logic.

    Args:
        session: SQLAlchemy session
        df: DataFrame with columns [date, price, market_cap, volume, source]
        asset_id: Foreign key to assets table

    Returns:
        Number of records inserted/updated
    """
    # Add asset_id to dataframe
    df['asset_id'] = asset_id

    # Convert DataFrame to list of dicts
    records = df.to_dict('records')

    # Upsert statement (insert or update on conflict)
    stmt = insert(AssetPrice).values(records)
    stmt = stmt.on_conflict_do_update(
        index_elements=['asset_id', 'date', 'source'],
        set_={
            'price': stmt.excluded.price,
            'market_cap': stmt.excluded.market_cap,
            'volume': stmt.excluded.volume
        }
    )

    result = session.execute(stmt)
    session.commit()

    return result.rowcount


def load_asset_with_prices(session, symbol, name, asset_type, price_df, source):
    """
    Convenience function to load both asset and its prices.

    Args:
        session: SQLAlchemy session
        symbol: Asset symbol
        name: Asset name
        asset_type: Asset type
        price_df: DataFrame with price data
        source: Source of the asset data (optional)

    Returns:
        Tuple of (Asset, number of prices loaded)
    """
    # Load or update asset
    asset = load_or_update_asset(session, symbol, name, asset_type, source)

    # Load prices
    count = load_prices(session, price_df, asset.id)

    return asset, count
