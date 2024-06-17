from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define database connection details (replace with your own)
DATABASE_URI = 'sqlite:///my_database.db'

# Create engine and session maker
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define database model (optional)
Base = declarative_base()


class Request(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  data = Column(String(128), nullable=False)
  created_at = Column(
      DateTime(),
      default=datetime.now,
  )

  # email = Column(String(120), nullable=)

  def __repr__(self):
    return f'<Request at={self.crated_at} data={self.data}>'


# Create database tables (optional)
Base.metadata.create_all(engine)


def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()
