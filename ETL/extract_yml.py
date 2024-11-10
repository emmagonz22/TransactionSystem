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
    for android, desktop, ios, location, email, pid, name, telephone in people_df.values:
        try:
            # Insert into the people table
            first_name, last_name = name.split(" ", 1)
            city, country = location.split(", ", 1)
            
            cur.execute(
                "INSERT INTO people (pid, first_name, last_name, telephone, email, city, country, android, ios, desktop) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
                (pid, first_name, last_name, telephone, email, city, country, android == 1, ios == 1, desktop == 1)
            )

            # Commit the transaction
            conn.commit()
            print("People data was inserted")
        except Exception as e:
            print("An error occurred while inserting into the database: ", e)
            