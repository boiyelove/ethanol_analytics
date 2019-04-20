import ethanol_analytics.db_info as xdb  # same db_info file that is in the django app; 
import psycopg2
from sqlalchemy import create_engine

url = 'postgresql+psycopg2://{}:{}@{}/{}'.format(xdb.username,xdb.password,xdb.host,xdb.database2)
engine = create_engine(url)
# connection = psycopg2.connect(
#             user=db.username,
#             password =db.password,
#             host=db.host,
#             port = 5432,
#             database=db.database2
#         )




# def sql_query(sql=None):
#     cursor = connection.cursor()
#     cursor.execute(sql)
#     colnames = [desc[0] for desc in cursor.description]

