import streamlit as st
import requests
import matplotlib.pyplot as plt


# API URLs
TRANSACTION_API_URL = "http://127.0.0.1:5000/transaction"
PEOPLE_API_URL = "http://127.0.0.1:5000/people"
PROMOTION_API_URL = "http://127.0.0.1:5000/promotion"
TRANSFER_API_URL = "http://127.0.0.1:5000/transfer"

st.title("Stadistics")

# Operation selector
operation = st.sidebar.selectbox("Choose an stadistic to displat", ["Top 5 sold items", "Top 5 stores with most sales (quantity)", "Top 5 stores with most profits", "Top 3 transfers",])

plt.style.use('dark_background')

if operation == "Top 5 sold items":
    st.header("Top 5 Sold Items")

    # Fetch the data for the top 5 sold items
    response = requests.get(f"{TRANSACTION_API_URL}/top-sold-items")
    if response.status_code == 200:
        top_items = response.json()

        item_names = [item["item_name"] for item in top_items]
        quantities = [item["total_quantity"] for item in top_items]

        fig, ax = plt.subplots(figsize=(10, 6)) 
        ax.bar(item_names, quantities, color='green')
        ax.set_xlabel("Item Name")
        ax.set_ylabel("Total Quantity Sold")
        ax.set_title("Top 5 Sold Items")

        st.pyplot(fig)      # show graph

    else:
        st.error("Failed to fetch top sold items from the API.")
        
elif operation == "Top 5 stores with most sales (quantity)":
    st.header("Top 5 Stores with the Most Sales")

    # Fetch data 
    response = requests.get(f"{TRANSACTION_API_URL}/top-five-stores-by-amount")
    if response.status_code == 200:
        top_stores = response.json()

        store_names = [store["store"] for store in top_stores]
        total_sales = [store["total_sales"] for store in top_stores]

        # plot 
        fig, ax = plt.subplots(figsize=(10, 6)) 
        ax.bar(store_names, total_sales,color='green')
        ax.set_xlabel("Store")
        ax.set_ylabel("Total Sales")
        ax.set_title("Top 5 Stores with Most Sales")
        print(store_names, total_sales)
       
        plt.tight_layout()  # fit layout
      
        st.pyplot(fig) # show graph
    else:
        st.error("Failed to fetch top stores data.")
        
elif operation == "Top 5 stores with most profits":
    st.header("Top 5 Stores with the Most Profits")

    # Fetch data 
    response = requests.get(f"{TRANSACTION_API_URL}/top-five-stores-by-profit")
    if response.status_code == 200:
        
        top_stores = response.json()

        store_names = [store["store"] for store in top_stores]
        total_profit = [float(store["total_profit"]) for store in top_stores]
        print(store_names, total_profit)
        # plot 
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(store_names, total_profit, color="green")
        ax.set_xlabel("Store")
        ax.set_ylabel("Total Profit")
        ax.set_title("Top 5 Stores by Total Profit")

        ax.set_ylim(0, max(total_profit) * 1.1)
        
        st.pyplot(fig) # show graph
    else:
        st.error("Failed to fetch top stores data.")

elif operation == "Top 3 transfers":
    pass 