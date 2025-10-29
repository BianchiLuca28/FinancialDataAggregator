# Test database connection
from connection import PostgreDatabase

def test_database_connection():
    db = PostgreDatabase()
    session = db.get_session()
    db.create_tables()


def __main():
    test_database_connection()
    print("Database connection test passed.")


if __name__ == "__main__":
    __main()
