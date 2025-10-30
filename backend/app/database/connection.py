from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
import os

load_dotenv()

class PostgreDatabase:

    def __init__(self):
        url = URL.create(
            drivername="postgresql",
            username=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            host=os.getenv('POSTGRES_HOST'),
            database=os.getenv('POSTGRES_DB')
        )

        self.engine = create_engine(url)
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        from .models import Base
        Base.metadata.create_all(self.engine)

    def drop_tables(self):
        from .models import Base
        Base.metadata.drop_all(self.engine)

    def get_session(self):
        return self.Session()
