import psycopg2

class Database:

    def __init__(self,
                POSTGRES_USER,
                POSTGRES_PASSWORD,
                POSTGRES_DB,
                POSTGRES_HOST,
                POSTGRES_PORT):
        self.POSTGRES_USER=POSTGRES_USER
        self.POSTGRES_PASSWORD=POSTGRES_PASSWORD
        self.POSTGRES_DB=POSTGRES_DB
        self.POSTGRES_HOST=POSTGRES_HOST
        self.POSTGRES_PORT=POSTGRES_PORT
        self.conn=None
    
    def connect(self):
        if self.conn is None: # if conn is open this not going to connect until disconnected
            try:
                self.conn = psycopg2.connect(
                    user=self.POSTGRES_USER,
                    password=self.POSTGRES_PASSWORD,
                    dbname=self.POSTGRES_DB,
                    host=self.POSTGRES_HOST,
                    port=self.POSTGRES_PORT
                )
                print("Connected to the database")
            except psycopg2.DatabaseError as e:
                raise e
        else:
            print("Database is already connected")
    
    def disconnect(self):
        if self.conn is not None:
            self.conn.close()
