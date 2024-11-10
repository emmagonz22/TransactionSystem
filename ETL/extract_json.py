import pandas as pd
from .database import get_connection, get_cursor, connect, disconnect


def load_people_json():
    conn = get_connection()
    cur = get_cursor()

    people_json = pd.read_json("./data/people.json")

    # Location is split in City and Country, devices will be in a new table
    for id, first_name, last_name, telephone, email, devices, location in people_json.values:
        try:
            
            android, ios, desktop = False, False, False
            
            for device in devices:
                if device == "Android":
                    android = True
                if device == "Iphone":
                    ios = True
                if device == "Desktop":
                    desktop = True
                
            cur.execute("""INSERT into people (pid, first_name, last_name, telephone, email, city, country, android, ios, desktop) 
                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (pid) DO NOTHING;""", 
                        (id, first_name, last_name, telephone, email, location["City"], location["Country"], android, ios, desktop))
            
         
            conn.commit()
            print("People data was inserted")
        except Exception as e:
            print("An error occurred while inserting into people: ", e)
    cur.execute("SELECT setval('people_pid_seq', COALESCE(MAX(pid), 1) + 1, false) FROM people;")
    conn.commit()
    conn.close()