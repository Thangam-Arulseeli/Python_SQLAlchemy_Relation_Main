#### Create DB Connection
import os

from dotenv import load_dotenv

from sqlalchemy import URL, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# Load environment variables from .env
load_dotenv()


# Build the PostgreSQL connection URL safely.
database_url = URL.create(
    drivername="postgresql+psycopg",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST", "127.0.0.1"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=os.getenv("DB_NAME"),
)


# Create the SQLAlchemy engine.
engine = create_engine(
    database_url,
    echo=True,
    pool_pre_ping=True,
)


# Base class for all ORM models.
class Base(DeclarativeBase):
    pass


# Session factory.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=True,
    expire_on_commit=True,
)


def get_session():
    """
    Create a database session and close it
    when the operation finishes.
    """

    with SessionLocal() as session:
        yield session


'''

create_engine() --> Creates the SQLAlchemy engine, which manages connections to PostgreSQL.

echo=True  --> Prints generated SQL statements in the terminal. This is particularly useful when learning JOINs and loading strategies.

NOTE: For production, configure appropriate structured logging instead of printing every SQL statement.

Base --> All our ORM models inherit from this class.

SessionLocal   -->  Creates sessions used to query and modify the database.
                    A session tracks ORM objects and coordinates database transactions.

get_session()   --> Provides a convenient session lifecycle pattern. In this project, our standalone scripts will use SessionLocal() directly.

'''