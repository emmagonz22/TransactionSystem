import pandas as pd
from .database import get_connection, get_cursor, connect, disconnect


def load_people_json():
    conn = get_connection()
    cur = get_cursor()

    people_json = pd.read_json("./data/people.json")

    # Location is split in City and Country, devices will be in a new table
    for id, first_name, last_name, telephone, email, devices, location in people_json.values:
        try:
            cur.execute("INSERT into people (pid, first_name, last_name, telephone, email, city, country) VALUES(%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (pid) DO NOTHING;", 
                        (id, first_name, last_name, telephone, email, location["City"], location["Country"]))
            
            # Insert the devices table in the db, this will have two foreign key 
            for device in devices:
                cur.execute("INSERT into device (pid, device_type) VALUES(%s, %s);", 
                        (id, device))
            
            conn.commit()
            print("People data was inserted")
        except Exception as e:
            print("An error occurred while inserting into people: ", e)