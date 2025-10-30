import logging
from app.database.connection import PostgreDatabase
from app.data_sources.coingecko import CoingeckoSource
from .load import load_asset_with_prices, load_prices
from .transform import prepare_prices_for_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ETLPipeline:

    def __init__(self):
        self.db = PostgreDatabase()
        self.db.create_tables()

        self.cg_api = CoingeckoSource()

    def run_historical_load(self, coin_configs, days=90):
        """
        Args:
            coin_configs: List of dicts like:
                [{'id': 'bitcoin', 'symbol': 'BTC', 'name': 'Bitcoin'}]
            days: Number of days of history to fetch
        """

        session = self.db.get_session()

        try:
            for config in coin_configs:
                coin_id = config["id"]
                name = config["name"]

                logger.info(f"Processing {name}...")

                # Extract
                api_results = self.cg_api.fetch_historical_prices(symbol=coin_id, days=days)

                # Transform
                transformed_df = prepare_prices_for_db(api_results)

                # Load
                asset, count = load_asset_with_prices(session, coin_id, name, "crypto", transformed_df, "coingecko")
                logger.info(f"  - Loaded {count} price records for {name}")

            logger.info("="*60)
            logger.info("Pipeline completed successfully!")


        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            session.rollback()
            raise Exception(f"Exception: {e}")
        finally:
            session.close()
