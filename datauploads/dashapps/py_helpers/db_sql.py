import ethanol_analytics.db_info as xdb  # same db_info file that is in the django app; 
import psycopg2
from sqlalchemy import create_engine

url = 'postgresql+psycopg2://{}:{}@{}/{}'.format(xdb.username,xdb.password,xdb.host,xdb.database2)
engine = create_engine(url)