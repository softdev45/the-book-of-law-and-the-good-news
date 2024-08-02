from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, create_engine, Boolean, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define database connection details (replace with your own)
DATABASE_URI = 'sqlite:///my_database_replit_1.db'

# Create engine and session maker
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Define database model (optional)
Base = declarative_base()

#TODO: create new field (email) and migrate db
#TODO: load text_data_db.txt into db


class Request(Base):
  __tablename__ = 'requests'
  id = Column(Integer, primary_key=True)
  request_data = Column(Text(1024), nullable=True)
  location = Column(String(128), nullable=True)
  lang = Column(String(128), nullable=True)
  # translation = Column(String(128), nullable=True)
  reply_to = Column(String(128), nullable=True)
  public = Column(Boolean, default=True)
  #burn
  verified = Column(Boolean, default=False)
  created_at = Column(
      DateTime(),
      default=datetime.now,
  )

  # email = Column(String(120), nullable=)

  def __repr__(self):
    return f'{self.request_data}'


class Verse(Base):
  __tablename__ = 'verse'
  id = Column(Integer, primary_key=True)
  location = Column(String(128), nullable=True)
  fire = Column(Integer, default=0)
	# timestamp = Column(Integer, default = 0)	

class Viewed(Base):
  __tablename__ = 'viewed'
  id = Column(Integer, primary_key=True)
  location = Column(String(128), nullable=False)
  created_at = Column(
      DateTime(),
      default=datetime.now,)
  session = Column(Float, nullable=True)

class Tag(Base):
  __tablename__ = 'tag'
  id = Column(Integer, primary_key=True)
  location = Column(String(128), nullable=False)
  tag = Column(String(64), nullable=False)
	

class Edge(Base):
  __tablename__ = 'edge'
  id = Column(Integer, primary_key=True)
  source = Column(String(128), nullable=False)
  dest = Column(String(128), nullable=False)
	


# Create database tables (optional)
Base.metadata.create_all(engine)


def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()
