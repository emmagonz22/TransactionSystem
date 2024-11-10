import sys    
print("In module products sys.path[0], __package__ ==", sys.path[0], __package__)

from ETL import run_etl
from ETL.database import connect, disconnect

# run main routine ot extract and load the data in the database
def start():
    connect()
    run_etl()
    disconnect()