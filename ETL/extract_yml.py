import pandas as pd
import yaml
from .database import get_connection, get_cursor, connect, disconnect


def load_people_yaml():
    conn = get_connection()
    cur = get_cursor()

    with open("./data/people.yml", "r") as file:
        people_data = yaml.safe_load(file)

    # clean yaml to dataframe
    people_df = pd.DataFrame(people_data).dropna() 

    # Process each people
    for android, desktop, iphone, location, email, pid, name, telephone in people_df.values:
        try:
            # Insert into the people table
            first_name, last_name = name.split(" ", 1)
            city, country = location.split(", ", 1)
            devices = []
            if android == True:
                devices.append("Android")
            if desktop == True:
                devices.append("Desktop")
            if iphone == True:
                devices.append("Iphone")
            
            cur.execute(
                "INSERT INTO people (pid, first_name, last_name, telephone, email, city, country) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (pid) DO NOTHING;",
                (pid, first_name, last_name, telephone, email, city, country)
            )

            # Insert into the devices table
            for device in devices:
                cur.execute(
                    "INSERT INTO device (pid, device_type) VALUES (%s, %s);",
                    (pid, device)
                )

            # Commit the transaction
            conn.commit()
            print("People data was inserted")
        except Exception as e:
            print("An error occurred while inserting into the database: ", e)
    