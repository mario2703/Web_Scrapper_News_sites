import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

now = datetime.datetime.now().strftime('%Y_%m_%d')

engine = create_engine('sqlite:///newspapers_{}.db'.format(now))

Session = sessionmaker(bind=engine)

Base = declarative_base()