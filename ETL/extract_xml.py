

import pandas as pd
import xml.etree.ElementTree as ET
import io
from .database import get_connection, get_cursor, connect, disconnect

#XML python doc https://docs.python.org/3/library/xml.etree.elementtree.html#module-xml.etree.ElementTree
# Extract and transform the data
def extract_xml(path):
    
    # Parse the XML file
    tree = ET.parse("./data/transactions.xml")
    root = tree.getroot()

    data = []
    for transaction in root.findall("transaction"):
        tid = transaction.get("id")
        phone = transaction.find("phone").text
        store = transaction.find("store").text
        
        for item in transaction.find("items").findall("item"):
            item_name = item.find("item").text
            price = float(item.find("price").text)
            price_per_item = float(item.find("price_per_item").text)
            quantity = int(item.find("quantity").text)
            
            data.append({
                "tid": tid,
                "item_name": item_name,
                "price": price,
                "price_per_item": price_per_item,
                "quantity": quantity,
                "phone": phone,
                "store": store
            })
            
    print(pd.DataFrame(data))
    print(len(data))
    return pd.DataFrame(data)


# Load
def load_transactions():
    conn = get_connection()
    cur = get_cursor()

    # Load clean XML data
    transactions_data = extract_xml("./data/transactions.xml")

    # Process each transactionn
    for tid, item_name, price, price_per_item, quantity, phone, store in transactions_data.values:
        try:
            cur.execute("""
                INSERT INTO transaction (tid, item_name, price, price_per_item, quantity, phone, store) 
                VALUES (%s, %s, %s, %s, %s, %s, %s);
                """, (tid, item_name, price, price_per_item, quantity, phone, store))
            conn.commit()
            print("Transaction data was inserted")
        
        except Exception as e:
            print("An error occurred while inserting into transaction: ", e)