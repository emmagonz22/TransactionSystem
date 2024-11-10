

import pandas as pd
from .database import get_connection, get_cursor, connect, disconnect


# Extract
def extract_csv(path):
    return pd.read_csv(path).dropna()


# Load
def load_promotions():
    conn = get_connection()
    cur = get_cursor()

    # Load clean csv file 
    promotions_data = extract_csv("./data/promotions.csv").dropna()

    # proccess each promotions
    for id, client_email, telephone, promotion, responded in promotions_data.values:
        try:
            cur.execute("INSERT into promotion (prid, client_email, telephone, promotion, responded) VALUES(%s, %s, %s, %s, %s);", (id, client_email, telephone, promotion, responded))
            conn.commit()
            print("Promotions data was inserted")
        except Exception as e:
            print("An error occurred while inserting into promotion: ", e)
    
    #cur.execute("SELECT setval('promotion_prid_seq', COALESCE(MAX(prid), 1) + 1, false) FROM promotion;")
    #conn.commit()


def load_transfer_csv():
    conn = get_connection()
    cur = get_cursor()

    transfer_data = extract_csv("./data/transfers.csv")

    for sender_id, recipient_id, amount, date in transfer_data.values:
        try:
            cur.execute("INSERT into transfer (sender_id, recipient_id, amount, date) VALUES(%s, %s, %s, %s);", (sender_id, recipient_id, amount, date))
            conn.commit()
            print("Transfer data was inserted")
        except Exception as e:
            print("An error occurred while inserting into transfer table: ", e)
            
    #cur.execute("SELECT setval('transfer_trid_seq', COALESCE(MAX(trid), 1) + 1, false) FROM transfer;")
    #conn.commit()
